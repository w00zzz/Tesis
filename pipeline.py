import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

from utils import (
    cargar_variables_prototipo,
    SimuladorTurbina,
    validar_rangos_operativos,
    validar_reglas_dinamicas,
    generar_informe_calidad,
    printdf,
)
from utils.analisis_distribuciones import (
    ejecutar_analisis as ejecutar_analisis_distribuciones,
)

load_dotenv()

CATALOGO_PATH = os.getenv("CATALOGO_PATH", "output/catalogo_variables.csv")
DATOS_REALES_PATH = os.getenv("DATOS_REALES_PATH", "input/datos_planta.csv")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output/")
REGLAS_VALIDEZ_PATH = os.getenv("REGLAS_VALIDEZ_PATH", "config/reglas_validacion.json")


def run_pipeline(usar_datos_reales=True, generar_simulacion=False):
    print("=" * 70)
    print("Pipeline: Simulador de Turbina de Vapor")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    if os.path.exists(CATALOGO_PATH):
        catalogo = pd.read_csv(CATALOGO_PATH)
    else:
        catalogo = cargar_variables_prototipo()

    simulador = SimuladorTurbina(catalogo_df=catalogo, phi_default=0.7)

    if DATOS_REALES_PATH and os.path.exists(DATOS_REALES_PATH):
        datos_historicos = pd.read_csv(DATOS_REALES_PATH)
        print(f"Datos cargados: {DATOS_REALES_PATH} ({len(datos_historicos)} filas)")
    else:
        datos_historicos = pd.read_csv("input/datos_ejemplo.csv")
        print(f"Usando datos ejemplo por defecto ({len(datos_historicos)} filas)")

    params = simulador.ajustar_distribuciones(datos_historicos)
    df_resumen = simulador.resumen_parametros()
    printdf(df_resumen, "Resumen de Distribuciones")

    ejecutar_analisis_distribuciones()

    if usar_datos_reales:
        print("\n--- VALIDACION CON DATOS REALES DEL ANEXO 1 ---")
        stats = get_stats_from_csv(datos_historicos)
    elif generar_simulacion:
        print("\n--- GENERANDO SIMULACION ---")
        df_simulacion = simulador.generar_simulacion(n_dias=1, freq_minutos=60, phi=0.7)
        ruta_sim = os.path.join(OUTPUT_DIR, "simulacion_completa.csv")
        df_simulacion.to_csv(ruta_sim, index=False)
        print(f"Simulacion guardada: {len(df_simulacion)} registros")
        stats = (
            df_simulacion.groupby("ID_Tecnico")["valor"]
            .agg(Min_Muestra="min", Max_Muestra="max", Media="mean", Std="std")
            .reset_index()
        )
    else:
        print("\n--- GENERANDO DATOS SIMULADOS ---")
        df_simulacion = simulador.generar_simulacion(n_dias=1, freq_minutos=60, phi=0.7)
        ruta_sim = os.path.join(OUTPUT_DIR, "simulacion_completa.csv")
        df_simulacion.to_csv(ruta_sim, index=False)
        stats = (
            df_simulacion.groupby("ID_Tecnico")["valor"]
            .agg(Min_Muestra="min", Max_Muestra="max", Media="mean", Std="std")
            .reset_index()
        )

    reporte_rangos = validar_rangos_operativos(catalogo, stats)
    printdf(reporte_rangos, "Validacion de Rangos")

    reporte_reglas = validar_reglas_dinamicas(stats, REGLAS_VALIDEZ_PATH)
    printdf(reporte_reglas, "Validacion de Reglas")

    calidad = generar_informe_calidad(catalogo, "Pipeline Final")
    printdf(calidad, "Resumen de Calidad")

    output_excel = os.path.join(OUTPUT_DIR, "resultados_pipeline.xlsx")
    with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
        reporte_rangos.to_excel(writer, sheet_name="Validacion_Rangos", index=False)
        reporte_reglas.to_excel(writer, sheet_name="Validacion_Reglas", index=False)
        df_resumen.to_excel(writer, sheet_name="Distribuciones", index=False)
        datos_historicos.to_excel(writer, sheet_name="Datos_Reales", index=False)

    print(f"Resultados exportados a {output_excel}")


def get_stats_from_csv(datos_df):
    """Calcula estadísticas de un DataFrame de datos reales."""
    stats_list = []
    for col in datos_df.columns:
        if col == "ID_Tecnico":
            continue
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


if __name__ == "__main__":
    run_pipeline(usar_datos_reales=True, generar_simulacion=False)
