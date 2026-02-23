from utils import cargar_variables_prototipo, printdf, guardar_excel, cargar_excel

def main():
    # 1. Cargar variables del prototipo (diccionario interno)
    catalogo = cargar_variables_prototipo()

    # 2. Guardar en Excel
    ruta_excel = "output/catalogo_variables.xlsx"
    if guardar_excel(catalogo, ruta_excel):
        print(f"✅ Archivo guardado correctamente en: {ruta_excel}")

    # 3. Cargar desde Excel
    df_excel = cargar_excel(ruta_excel)
    
    # 4. Mostrar usando la tabla bonita
    if df_excel is not None:
        printdf(df_excel, "Catálogo cargado desde Excel")

if __name__ == "__main__":
    main()
