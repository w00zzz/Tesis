import pandas as pd
import os

def cargar_excel(ruta_archivo, nombre_hoja=0):
    """
    Carga un archivo Excel y devuelve un DataFrame de pandas.
    
    Args:
        ruta_archivo (str): La ruta al archivo Excel (.xlsx o .xls).
        nombre_hoja (str o int): El nombre o índice de la hoja a cargar. Por defecto la primera.
        
    Returns:
        pd.DataFrame: El DataFrame con los datos cargados.
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo no se encontró: {ruta_archivo}")
    
    try:
        df = pd.read_excel(ruta_archivo, sheet_name=nombre_hoja)
        return df
    except Exception as e:
        print(f"Error al cargar el archivo Excel: {e}")
        return None

def guardar_excel(df, ruta_archivo, nombre_hoja="Datos"):
    """
    Guarda un DataFrame de pandas en un archivo Excel.
    
    Args:
        df (pd.DataFrame): El DataFrame a guardar.
        ruta_archivo (str): La ruta donde se guardará el archivo.
        nombre_hoja (str): El nombre de la hoja en el Excel.
        
    Returns:
        bool: True si se guardó correctamente, False de lo contrario.
    """
    try:
        directorio = os.path.dirname(ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
            
        df.to_excel(ruta_archivo, index=False, sheet_name=nombre_hoja)
        return True
    except Exception as e:
        print(f"Error al guardar el archivo Excel: {e}")
        return False
