import numpy as np
import pandas as pd
from typing import Dict, Optional, List
from datetime import datetime, timedelta

from utils.distribuciones import (
    DistribucionEstadistica,
    crear_distribucion,
    FABRICA_DISTRIBUCIONES,
)


class ModeloAR1:

    def __init__(self, mu: float, sigma: float, phi: float = 0.7):
        if not (0 < phi < 1):
            raise ValueError(f"phi debe estar en (0, 1), recibido: {phi}")
        self.mu = mu
        self.sigma = sigma
        self.phi = phi
        self.sigma_epsilon = sigma * np.sqrt(1 - phi**2)

    def generar_serie(self, n_puntos: int, x0: Optional[float] = None) -> np.ndarray:
        serie = np.zeros(n_puntos)
        serie[0] = x0 if x0 is not None else self.mu
        for t in range(1, n_puntos):
            epsilon = np.random.normal(0, self.sigma_epsilon)
            serie[t] = self.mu + self.phi * (serie[t - 1] - self.mu) + epsilon
        return serie

    def get_parametros(self) -> Dict:
        return {
            "mu": self.mu,
            "sigma": self.sigma,
            "phi": self.phi,
            "sigma_epsilon": self.sigma_epsilon,
        }


class SimuladorTurbina:

    def __init__(
        self,
        catalogo_variables_path: Optional[str] = None,
        catalogo_df: Optional[pd.DataFrame] = None,
        phi_default: float = 0.7,
    ):
        self.phi_default = phi_default
        self.catalogo_variables: pd.DataFrame = None
        self.distribuciones: Dict[str, DistribucionEstadistica] = {}
        self.modelos_ar1: Dict[str, ModeloAR1] = {}
        self.parametros_distribuciones: Dict[str, Dict] = {}

        if catalogo_df is not None:
            self.catalogo_variables = catalogo_df
        elif catalogo_variables_path is not None:
            self._cargar_catalogo(catalogo_variables_path)
        else:
            from utils.cargar_variables_prototipo import cargar_variables_prototipo
            self.catalogo_variables = cargar_variables_prototipo()

        print(f"Simulador inicializado con {len(self.catalogo_variables)} variables")

    def _cargar_catalogo(self, ruta: str):
        if ruta.endswith('.csv'):
            self.catalogo_variables = pd.read_csv(ruta)
        elif ruta.endswith(('.xlsx', '.xls')):
            self.catalogo_variables = pd.read_excel(ruta)
        else:
            raise ValueError(f"Formato no soportado: {ruta}")

    def ajustar_distribuciones(
        self,
        datos_historicos: pd.DataFrame,
        distribucion_default: str = "Normal",
    ) -> Dict[str, Dict]:

        if 'ID_Tecnico' in datos_historicos.columns:
            variables_datos = {
                col: datos_historicos[datos_historicos['ID_Tecnico'] == col]['Valor'].dropna()
                for col in datos_historicos['ID_Tecnico'].unique()
            }
        else:
            variables_datos = {
                col: datos_historicos[col].dropna()
                for col in datos_historicos.columns
            }

        for id_tecnico, datos in variables_datos.items():
            if len(datos) < 5:
                continue

            candidatos = {}
            for nombre_dist in ["Normal", "Weibull", "LogNormal", "Gamma"]:
                try:
                    dist = crear_distribucion(nombre_dist)
                    params = dist.ajustar(datos)
                    candidatos[nombre_dist] = {
                        "distribucion": dist,
                        "parametros": params,
                        "gof_value": params.get("gof_value", 0),
                    }
                except Exception:
                    continue

            if not candidatos:
                continue

            mejor_nombre = max(candidatos, key=lambda x: candidatos[x]["gof_value"])
            mejor = candidatos[mejor_nombre]

            self.distribuciones[id_tecnico] = mejor["distribucion"]
            self.parametros_distribuciones[id_tecnico] = mejor["parametros"]

            mu = mejor["parametros"]["param1"]
            sigma = mejor["parametros"]["param2"]
            self.modelos_ar1[id_tecnico] = ModeloAR1(
                mu=mu, sigma=sigma, phi=self.phi_default
            )

        return self.parametros_distribuciones

    def generar_valor_estatico(self, id_variable: str) -> float:
        if id_variable not in self.distribuciones:
            raise ValueError(f"Variable '{id_variable}' sin distribucion ajustada")
        return self.distribuciones[id_variable].generar(n=1)

    def generar_serie_temporal(
        self,
        id_variable: str,
        n_puntos: int,
        phi: Optional[float] = None,
        x0: Optional[float] = None,
    ) -> np.ndarray:
        if id_variable not in self.modelos_ar1:
            raise ValueError(f"Variable '{id_variable}' sin modelo AR(1)")

        modelo = self.modelos_ar1[id_variable]
        if phi is not None and phi != modelo.phi:
            modelo = ModeloAR1(mu=modelo.mu, sigma=modelo.sigma, phi=phi)
        return modelo.generar_serie(n_puntos, x0)

    def generar_simulacion(
        self,
        n_dias: int,
        freq_minutos: int = 60,
        phi: Optional[float] = None,
        solo_carga: bool = True,
    ) -> pd.DataFrame:
        n_puntos = int(n_dias * 24 * 60 / freq_minutos)
        timestamp_inicio = datetime.now()

        catalogo = self.catalogo_variables
        if solo_carga and 'Tipo_en_modelo' in catalogo.columns:
            variables_a_simular = catalogo[
                catalogo['Tipo_en_modelo'] == 'Carga'
            ]['ID_Tecnico'].tolist()
        else:
            variables_a_simular = catalogo['ID_Tecnico'].tolist()

        datos_simulacion = []
        for id_variable in variables_a_simular:
            if id_variable not in self.modelos_ar1:
                continue
            try:
                serie = self.generar_serie_temporal(id_variable, n_puntos, phi)
                tipo = 'Desconocido'
                if 'Tipo_en_modelo' in catalogo.columns:
                    fila = catalogo[catalogo['ID_Tecnico'] == id_variable]
                    if not fila.empty:
                        tipo = fila.iloc[0].get('Tipo_en_modelo', 'Desconocido')

                for i, valor in enumerate(serie):
                    timestamp = timestamp_inicio + timedelta(minutes=i * freq_minutos)
                    datos_simulacion.append({
                        "timestamp": timestamp,
                        "ID_Tecnico": id_variable,
                        "valor": valor,
                        "tipo_en_modelo": tipo,
                    })
            except Exception:
                continue

        return pd.DataFrame(datos_simulacion)

    def resumen_parametros(self) -> pd.DataFrame:
        resumen = []
        for id_tecnico, params in self.parametros_distribuciones.items():
            fila = {
                "ID_Tecnico": id_tecnico,
                "Distribucion": params.get("distribucion", "N/A"),
                "Param1": params.get("param1", None),
                "Param2": params.get("param2", None),
                "Param3": params.get("param3", None),
                "GOF_Metric": params.get("gof_metric", "N/A"),
                "GOF_Value": params.get("gof_value", None),
                "Notas": params.get("notas", ""),
            }
            if self.catalogo_variables is not None:
                cat_row = self.catalogo_variables[
                    self.catalogo_variables['ID_Tecnico'] == id_tecnico
                ]
                if not cat_row.empty:
                    fila['Nombre'] = cat_row.iloc[0].get('Nombre_amigable', '')
                    fila['Unidad'] = cat_row.iloc[0].get('Unidad', '')
                    fila['Tipo_en_modelo'] = cat_row.iloc[0].get('Tipo_en_modelo', '')
                    fila['Mecanismos'] = cat_row.iloc[0].get('Mecanismos_asociados', '')
            resumen.append(fila)
        return pd.DataFrame(resumen)
