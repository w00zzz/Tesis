from pandas import DataFrame

def validar_catalogo(df):
    columnas_obligatorias = [
        "ID_Tecnico",
        "Nombre_amigable",
        "Unidad",
        "Tipo_Dato"
    ]

    for col in columnas_obligatorias:
        if col not in df.columns:
            raise ValueError(f"Falta la comuna obligatoria: {col}")

    print("Catalogo validado correctamente.")