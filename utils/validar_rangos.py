import pandas as pd

def validar_rangos_operativos(df_catalogo, df_muestra_stats=None):
    """
    Compara los rangos técnicos/esperados del catálogo con los rangos observados en una muestra.
    
    Args:
        df_catalogo (pd.DataFrame): El catálogo con 'Rango_min' y 'Rango_max'.
        df_muestra_stats (pd.DataFrame, opcional): Estadísticas de la muestra 
                                                 (debe tener 'ID_Tecnico', 'Min_Muestra', 'Max_Muestra').
        
    Returns:
        pd.DataFrame: Un reporte de validación de rangos.
    """
    validaciones = []
    
    for _, row in df_catalogo.iterrows():
        id_tec = row['ID_Tecnico']
        r_min_esp = row['Rango_min']
        r_max_esp = row['Rango_max']
        
        # Placeholder para datos de muestra si no se proporcionan
        min_obs = "N/A"
        max_obs = "N/A"
        estado = "Sin datos de muestra"
        desviacion = "Pendiente" # Placeholder para cálculo de % fuera de rango
        
        if df_muestra_stats is not None and id_tec in df_muestra_stats['ID_Tecnico'].values:
            stats = df_muestra_stats[df_muestra_stats['ID_Tecnico'] == id_tec].iloc[0]
            min_obs = stats['Min_Muestra']
            max_obs = stats['Max_Muestra']
            
            # Lógica de validación básica
            fuera_bajo = min_obs < r_min_esp
            fuera_alto = max_obs > r_max_esp
            
            if fuera_bajo and fuera_alto:
                estado = "⚠️ Fuera de rango (Ambos extremos)"
            elif fuera_bajo:
                estado = "⚠️ Bajo el mínimo esperado"
            elif fuera_alto:
                estado = "⚠️ Sobre el máximo esperado"
            else:
                estado = "✅ Dentro de rango"
                
            # Placeholder para métrica de severidad
            desviacion = "Cálculo pendiente (Métrica de severidad)"
            
        validaciones.append({
            "ID_Tecnico": id_tec,
            "Min_Esperado": r_min_esp,
            "Max_Esperado": r_max_esp,
            "Min_Observado": min_obs,
            "Max_Observado": max_obs,
            "Estado_Rango": estado,
            "Analisis_Severidad": desviacion # Placeholder
        })
        
    return pd.DataFrame(validaciones)
