import pandas as pd

def generar_informe_calidad(df, nombre_dataset="Dataset"):
    """
    Genera un informe básico de calidad de datos con placeholders para métricas avanzadas.
    
    Args:
        df (pd.DataFrame): El DataFrame a analizar.
        nombre_dataset (str): Nombre descriptivo para el informe.
        
    Returns:
        pd.DataFrame: Un resumen de calidad por columna.
    """
    informe = []
    
    total_filas = len(df)
    duplicados = df.duplicated().sum()
    
    for col in df.columns:
        nulos = df[col].isnull().sum()
        porcentaje_nulos = (nulos / total_filas) * 100 if total_filas > 0 else 0
        tipo_dato = df[col].dtype
        unicos = df[col].nunique()
        
        completitud = 100 - porcentaje_nulos
        consistencia = "Pendiente de implementar"
        validez = "Pendiente de implementar"
        
        informe.append({
            "Columna": col,
            "Tipo": str(tipo_dato),
            "Nulos": nulos,
            "% Nulos": round(porcentaje_nulos, 2),
            "Unicos": unicos,
            "Completitud %": round(completitud, 2),
            "Consistencia": consistencia,
            "Validez": validez
        })
    
    resumen_df = pd.DataFrame(informe)
    
    print(f"\n--- Resumen de Calidad: {nombre_dataset} ---")
    print(f"Total de registros: {total_filas}")
    print(f"Filas duplicadas: {duplicados}")
    print("-" * (30 + len(nombre_dataset)))
    
    return resumen_df
