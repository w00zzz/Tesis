import pandas as pd
import os

def cargar_csv(ruta_archivo):
    """
    Carga un archivo CSV y devuelve un DataFrame de pandas.
    
    Args:
        ruta_archivo (str): La ruta al archivo CSV.
        
    Returns:
        pd.DataFrame: El DataFrame con los datos cargados.
        
    Raises:
        FileNotFoundError: Si el archivo no existe en la ruta especificada.
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo no se encontró en la ruta: {ruta_archivo}")
    
    try:
        df = pd.read_csv(ruta_archivo)
        return df
    except Exception as e:
        print(f"Error al cargar el archivo CSV: {e}")
        return None
