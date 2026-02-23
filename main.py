import pandas as pd
from utils import (
    cargar_variables_prototipo, 
    printdf, 
    generar_informe_calidad, 
    validar_rangos_operativos
)

def main():
    catalogo = cargar_variables_prototipo()

    datos_muestra = pd.DataFrame([
        {"ID_Tecnico": "1GEV007CE", "Min_Muestra": 260.00, "Max_Muestra": 275.00},
        {"ID_Tecnico": "1FSRFTB504", "Min_Muestra": 775.00, "Max_Muestra": 785.00},
        {"ID_Tecnico": "1FSRTE502C", "Min_Muestra": 390.00, "Max_Muestra": 405.00},
    ])

    reporte_rangos = validar_rangos_operativos(catalogo, datos_muestra)

    printdf(catalogo, "Catálogo de Variables (Rangos Técnicos)")
    printdf(reporte_rangos, "Validación: Rangos Esperados vs Observados")

    informe_calidad = generar_informe_calidad(catalogo, "Análisis de Catálogo")
    printdf(informe_calidad, "Informe de Calidad")

if __name__ == "__main__":
    main()
