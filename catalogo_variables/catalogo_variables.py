import pandas as pd

def crear_catalogo_base():
    columnas = [
        "ID_Tecnico",
        "Nombre_amigable",
        "Descripcion_funcional",
        "Unidad",
        "Tipo_dato",
        "Rango_min",
        "Rango_max",
        "Distribucion_observada",
        "Pregunta_planta"
    ]

    df_catalogo = pd.DataFrame(columns=columnas)
    
    return df_catalogo

