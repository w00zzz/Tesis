import pandas as pd
import os

def calcular_estadisticos_reales(ruta_csv, chunksize=100000):
    """
    Lee un archivo CSV grande por trozos (chunks) y calcula min/max agrupado por ID_Tecnico.
    
    Args:
        ruta_csv (str): Ruta al archivo de datos reales.
        chunksize (int): Cantidad de filas a leer por vez para no saturar la RAM.
        
    Returns:
        pd.DataFrame: Estadísticos calculados [ID_Tecnico, Min_Muestra, Max_Muestra].
    """
    if not os.path.exists(ruta_csv):
        print(f"WARN: Archivo de datos reales no encontrado: {ruta_csv}")
        return None

    print(f"INFO: Procesando datos reales en trozos de {chunksize} filas...")
    
    # Usaremos un diccionario para ir acumulando los mínimos y máximos globales
    global_min = {}
    global_max = {}

    try:
        # Iterar sobre el CSV por partes
        for chunk in pd.read_csv(ruta_csv, chunksize=chunksize):
            # Asumimos que el archivo real tiene columnas: ID_Tecnico, Valor
            # Si tiene un formato diferente (columnas como variables), se debe pivotar
            if 'ID_Tecnico' in chunk.columns and 'Valor' in chunk.columns:
                stats = chunk.groupby('ID_Tecnico')['Valor'].agg(['min', 'max'])
                
                for id_tec, row in stats.iterrows():
                    global_min[id_tec] = min(global_min.get(id_tec, row['min']), row['min'])
                    global_max[id_tec] = max(global_max.get(id_tec, row['max']), row['max'])
            else:
                # Caso alternativo: Columnas son los IDs Técnicos directamente
                # Calculamos min/max para cada columna numérica
                for col in chunk.select_dtypes(include=['number']).columns:
                    c_min, c_max = chunk[col].min(), chunk[col].max()
                    global_min[col] = min(global_min.get(col, c_min), c_min)
                    global_max[col] = max(global_max.get(col, c_max), c_max)

        # Convertir a DataFrame final con el formato que espera el validador
        resumen = pd.DataFrame([
            {"ID_Tecnico": k, "Min_Muestra": global_min[k], "Max_Muestra": global_max[k]}
            for k in global_min.keys()
        ])
        
        return resumen

    except Exception as e:
        print(f"ERROR: No se pudieron procesar estadísticos dinámicos: {e}")
        return None
