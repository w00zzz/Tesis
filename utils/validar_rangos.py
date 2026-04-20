import pandas as pd

def validar_rangos_operativos(df_catalogo, df_muestra_stats=None):
    validaciones = []
    
    for _, row in df_catalogo.iterrows():
        id_tec = row['ID_Tecnico']
        r_min_esp = row['Rango_min']
        r_max_esp = row['Rango_max']
        
        min_obs = "N/A"
        max_obs = "N/A"
        estado = "Sin datos de muestra"
        desviacion = "Pendiente"
        
        if df_muestra_stats is not None and id_tec in df_muestra_stats['ID_Tecnico'].values:
            stats = df_muestra_stats[df_muestra_stats['ID_Tecnico'] == id_tec].iloc[0]
            min_obs = stats['Min_Muestra']
            max_obs = stats['Max_Muestra']
            
            fuera_bajo = min_obs < r_min_esp
            fuera_alto = max_obs > r_max_esp
            
            if fuera_bajo and fuera_alto:
                estado = "FUERA: Fuera de rango (Ambos extremos)"
            elif fuera_bajo:
                estado = "BAJO: Bajo el minimo esperado"
            elif fuera_alto:
                estado = "ALTO: Sobre el maximo esperado"
            else:
                estado = "OK: Dentro de rango"
                
            desviacion = "Cálculo pendiente (Métrica de severidad)"
            
        validaciones.append({
            "ID_Tecnico": id_tec,
            "Min_Esperado": r_min_esp,
            "Max_Esperado": r_max_esp,
            "Min_Observado": min_obs,
            "Max_Observado": max_obs,
            "Estado_Rango": estado,
            "Analisis_Severidad": desviacion
        })
        
    return pd.DataFrame(validaciones)
