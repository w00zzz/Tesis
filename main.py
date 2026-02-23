import pandas as pd
from utils import (
    cargar_variables_prototipo, 
    printdf, 
    generar_informe_calidad, 
    validar_rangos_operativos
)

def main():
    # 1. Cargar catálogo (Rangos Esperados)
    catalogo = cargar_variables_prototipo()

    # 2. Simular datos de una muestra (Estadísticos observados)
    # En un caso real, esto vendría de calcular min/max sobre un archivo de datos reales
    datos_muestra = pd.DataFrame([
        {"ID_Tecnico": "1GEV007CE", "Min_Muestra": 260.00, "Max_Muestra": 275.00}, # Fuera de rango
        {"ID_Tecnico": "1FSRFTB504", "Min_Muestra": 775.00, "Max_Muestra": 785.00}, # Dentro de rango
        {"ID_Tecnico": "1FSRTE502C", "Min_Muestra": 390.00, "Max_Muestra": 405.00}, # Fuera de rango
    ])

    # 3. Validar rangos
    reporte_rangos = validar_rangos_operativos(catalogo, datos_muestra)

    # 4. Mostrar resultados
    printdf(catalogo, "Catálogo de Variables (Rangos Técnicos)")
    printdf(reporte_rangos, "Validación: Rangos Esperados vs Observados")

    # 5. Informe de calidad adicional
    informe_calidad = generar_informe_calidad(catalogo, "Análisis de Catálogo")
    printdf(informe_calidad, "Informe de Calidad")

if __name__ == "__main__":
    main()
