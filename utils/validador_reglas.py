import pandas as pd
import json
import os

def cargar_reglas(ruta_json):
    """Carga las reglas desde el archivo JSON."""
    if not os.path.exists(ruta_json):
        return {"reglas_validez": [], "reglas_consistencia": []}
    with open(ruta_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def validar_reglas_dinamicas(df_datos, ruta_reglas):
    """
    Aplica las reglas de validez y consistencia definidas en el JSON sobre un DataFrame.
    """
    reglas = cargar_reglas(ruta_reglas)
    resultados = []

    for regla in reglas.get("reglas_validez", []):
        columnas_afectadas = [c for c in regla["columnas"] if c in df_datos['ID_Tecnico'].values]
        
        for col in columnas_afectadas:
            stats = df_datos[df_datos['ID_Tecnico'] == col].iloc[0]
            
            valido_min = eval(f"{stats['Min_Muestra']} {regla['condicion']}")
            valido_max = eval(f"{stats['Max_Muestra']} {regla['condicion']}")
            
            if not valido_min or not valido_max:
                resultados.append({
                    "Regla": regla["nombre"],
                    "Variable": col,
                    "Estado": "Error de Validez",
                    "Detalle": regla["mensaje"]
                })
            else:
                resultados.append({
                    "Regla": regla["nombre"],
                    "Variable": col,
                    "Estado": "Valido",
                    "Detalle": "Cumple condicion"
                })

    return pd.DataFrame(resultados)
