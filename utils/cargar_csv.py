import pandas as pd
import os

def cargar_csv(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo no se encontró en la ruta: {ruta_archivo}")
    
    try:
        df = pd.read_csv(ruta_archivo)
        return df
    except Exception as e:
        print(f"Error al cargar el archivo CSV: {e}")
        return None
