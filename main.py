from utils import cargar_variables_prototipo, printdf, generar_informe_calidad

def main():
    # 1. Cargar datos
    catalogo = cargar_variables_prototipo()

    # 2. Mostrar datos originales
    printdf(catalogo, "Catálogo de Variables")

    # 3. Generar informe de calidad
    informe = generar_informe_calidad(catalogo, "Control de Calidad - Prototipo")
    
    # 4. Mostrar el informe resultante usando la tabla bonita
    printdf(informe, "Informe de Calidad de Datos")

if __name__ == "__main__":
    main()
