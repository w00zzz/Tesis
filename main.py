import os
import argparse
import pandas as pd
import numpy as np
from dotenv import load_dotenv

from utils import (
    cargar_variables_prototipo,
    SimuladorTurbina,
    validar_rangos_operativos,
    printdf,
)
from utils.analisis_distribuciones import (
    ejecutar_analisis as ejecutar_analisis_distribuciones,
)

load_dotenv()

DATOS_DEFAULT = "input/datos_planta.csv"


def get_stats_from_csv(datos_df):
    """Calcula estadísticas de un DataFrame de datos reales."""
    stats_list = []
    for col in datos_df.columns:
        valores = datos_df[col].dropna()
        if len(valores) > 0:
            stats_list.append(
                {
                    "ID_Tecnico": col,
                    "Min_Muestra": valores.min(),
                    "Max_Muestra": valores.max(),
                    "Media": valores.mean(),
                    "Std": valores.std() if len(valores) > 1 else 0,
                }
            )
    return pd.DataFrame(stats_list)


def prueba_rapida():
    """Prueba rápida con datos reales del CSV."""
    catalogo = cargar_variables_prototipo()
    simulador = SimuladorTurbina(catalogo_df=catalogo, phi_default=0.7)
    datos = pd.read_csv(DATOS_DEFAULT)
    print(f"Datos reales cargados: {len(datos)} filas x {len(datos.columns)} columnas")

    params = simulador.ajustar_distribuciones(datos)
    df_resumen = simulador.resumen_parametros()
    printdf(df_resumen, "Parametros de Distribuciones")

    stats = get_stats_from_csv(datos)
    reporte = validar_rangos_operativos(catalogo, stats)
    printdf(reporte, "Validacion de Rangos (Datos Reales)")


def prueba_distribuciones():
    """Ajusta distribuciones con datos reales."""
    catalogo = cargar_variables_prototipo()
    simulador = SimuladorTurbina(catalogo_df=catalogo)
    datos = pd.read_csv(DATOS_DEFAULT)
    print(f"Ajustando distribuciones con {len(datos)} observaciones reales...")
    simulador.ajustar_distribuciones(datos)
    df_resumen = simulador.resumen_parametros()
    printdf(df_resumen, "Parametros de Distribuciones Ajustadas")


def prueba_simulacion(generar_nuevos=False):
    """Genera simulación o muestra stats de datos reales."""
    catalogo = cargar_variables_prototipo()
    simulador = SimuladorTurbina(catalogo_df=catalogo)
    datos = pd.read_csv(DATOS_DEFAULT)

    if generar_nuevos:
        print("Generando datos simulados...")
        simulador.ajustar_distribuciones(datos)
        df_sim = simulador.generar_simulacion(n_dias=1, freq_minutos=60)
        df_sim.to_csv("output/simulacion_prueba.csv", index=False)
        print(f"Simulacion guardada: {len(df_sim)} registros")
    else:
        print("Stats de datos reales del Anexo 1:")
        stats = get_stats_from_csv(datos)
        printdf(stats, "Estadísticas de Datos Reales")


def prueba_histogramas():
    """Genera histogramas con datos reales."""
    print(f"Generando histogramas con datos de: {DATOS_DEFAULT}")
    ejecutar_analisis_distribuciones()


def main():
    parser = argparse.ArgumentParser(description="Simulador de Turbina de Vapor")
    parser.add_argument(
        "--distribuciones", action="store_true", help="Ajustar distribuciones"
    )
    parser.add_argument(
        "--simulacion",
        action="store_true",
        help="Generar simulacion (sin datos reales)",
    )
    parser.add_argument(
        "--histogramas", action="store_true", help="Generar histogramas"
    )
    parser.add_argument("--datos", action="store_true", help="Ver datos reales y stats")
    args = parser.parse_args()

    if args.histogramas:
        prueba_histogramas()
    elif args.simulacion:
        prueba_simulacion(generar_nuevos=True)
    elif args.distribuciones:
        prueba_distribuciones()
    elif args.datos:
        datos = pd.read_csv(DATOS_DEFAULT)
        print(f"Datos reales ({len(datos)} filas):")
        stats = get_stats_from_csv(datos)
        printdf(stats, "Estadísticas")
    else:
        prueba_rapida()


if __name__ == "__main__":
    main()
