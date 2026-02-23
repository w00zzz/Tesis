import os
import pandas as pd
from dotenv import load_dotenv
from utils import (
    cargar_variables_prototipo,
    calcular_estadisticos_reales,
    validar_rangos_operativos,
    validar_reglas_dinamicas,
    generar_informe_calidad,
    printdf,
    guardar_excel
)

# 1. Cargar configuración desde .env
load_dotenv()

CATALOGO_PATH = os.getenv("CATALOGO_PATH", "output/catalogo_variables.csv")
DATOS_REALES_PATH = os.getenv("DATOS_REALES_PATH")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output/")
REGLAS_VALIDEZ_PATH = os.getenv("REGLAS_VALIDEZ_PATH", "config/reglas_validacion.json")

def run_pipeline():
    print("START: Iniciando Pipeline Automatizado...")

    # A. Cargar o crear catálogo
    if os.path.exists(CATALOGO_PATH):
        print(f"INFO: Cargando catálogo desde: {CATALOGO_PATH}")
        catalogo = pd.read_csv(CATALOGO_PATH)
    else:
        print("INFO: Catálogo no encontrado, cargando prototipo por defecto.")
        catalogo = cargar_variables_prototipo()

    # B. Procesar estadísticas de datos reales (si la ruta existe)
    stats_reales = None
    if DATOS_REALES_PATH and os.path.exists(DATOS_REALES_PATH):
        print(f"STATS: Procesando datos reales: {DATOS_REALES_PATH}")
        stats_reales = calcular_estadisticos_reales(DATOS_REALES_PATH)
    else:
        print("WARN: No se proporcionó ruta de datos reales o el archivo no existe. Usando simulación para demostración.")
        # Simulación si no hay archivo real para que el pipeline no falle al probarlo
        stats_reales = pd.DataFrame([
            {"ID_Tecnico": "1GEV007CE", "Min_Muestra": -5.0, "Max_Muestra": 275.0}, # Activará regla de presión no negativa
            {"ID_Tecnico": "1FSRFTB504", "Min_Muestra": 775.0, "Max_Muestra": 785.0}
        ])

    # C. Validar Rangos Técnicos
    reporte_rangos = validar_rangos_operativos(catalogo, stats_reales)
    printdf(reporte_rangos, "Resultado: Validación de Rangos Técnicos")

    # D. Aplicar Reglas de Validación (JSON)
    reporte_reglas = validar_reglas_dinamicas(stats_reales, REGLAS_VALIDEZ_PATH)
    printdf(reporte_reglas, "Resultado: Validación de Reglas de Negocio")

    # E. Informe de Calidad General
    calidad = generar_informe_calidad(catalogo, "Pipeline Final")
    printdf(calidad, "Resumen de Calidad")

    # F. Exportar resultados finales
    output_excel = os.path.join(OUTPUT_DIR, "resultados_pipeline.xlsx")
    guardar_excel(reporte_rangos, output_excel, "Validacion_Rangos")
    print(f"OK: Resultados exportados a: {output_excel}")

if __name__ == "__main__":
    run_pipeline()
