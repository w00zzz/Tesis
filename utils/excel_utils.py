import pandas as pd
import os

def cargar_excel(ruta_archivo, nombre_hoja=0):
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo no se encontró: {ruta_archivo}")
    
    try:
        df = pd.read_excel(ruta_archivo, sheet_name=nombre_hoja)
        return df
    except Exception as e:
        print(f"Error al cargar el archivo Excel: {e}")
        return None

def guardar_excel(df, ruta_archivo, nombre_hoja="Datos"):
    try:
        directorio = os.path.dirname(ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
            
        df.to_excel(ruta_archivo, index=False, sheet_name=nombre_hoja)
        return True
    except Exception as e:
        print(f"Error al guardar el archivo Excel: {e}")
        return False
