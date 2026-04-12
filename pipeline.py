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
from utils.analisis_distribuciones import ejecutar_analisis as ejecutar_analisis_distribuciones

load_dotenv()

CATALOGO_PATH = os.getenv("CATALOGO_PATH", "output/catalogo_variables.csv")
DATOS_REALES_PATH = os.getenv("DATOS_REALES_PATH")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output/")
REGLAS_VALIDEZ_PATH = os.getenv("REGLAS_VALIDEZ_PATH", "config/reglas_validacion.json")


def run_pipeline():
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
    else:
        datos_historicos = pd.read_csv("input/datos_ejemplo.csv")

    params = simulador.ajustar_distribuciones(datos_historicos)
    df_resumen = simulador.resumen_parametros()
    printdf(df_resumen, "Resumen de Distribuciones")

    ejecutar_analisis_distribuciones()

    df_simulacion = simulador.generar_simulacion(n_dias=1, freq_minutos=60, phi=0.7)
    ruta_sim = os.path.join(OUTPUT_DIR, "simulacion_completa.csv")
    df_simulacion.to_csv(ruta_sim, index=False)

    stats = df_simulacion.groupby("ID_Tecnico")["valor"].agg(
        Min_Muestra="min", Max_Muestra="max", Media="mean", Std="std"
    ).reset_index()

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
        df_simulacion.to_excel(writer, sheet_name="Simulacion", index=False)

    print(f"Resultados exportados a {output_excel}")


if __name__ == "__main__":
    run_pipeline()
