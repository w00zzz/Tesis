import pandas as pd
import numpy as np


def validar_rangos_operativos(df_catalogo, df_muestra_stats=None):
    validaciones = []

    for _, row in df_catalogo.iterrows():
        id_tec = row["ID_Tecnico"]
        r_min_esp = row["Rango_min"]
        r_max_esp = row["Rango_max"]

        min_obs = "N/A"
        max_obs = "N/A"
        estado = "Sin datos de muestra"
        desviacion = "N/A (dato puntual)"
        pct_desviacion = 0.0

        if (
            df_muestra_stats is not None
            and id_tec in df_muestra_stats["ID_Tecnico"].values
        ):
            stats = df_muestra_stats[df_muestra_stats["ID_Tecnico"] == id_tec].iloc[0]
            min_obs = stats["Min_Muestra"]
            max_obs = stats["Max_Muestra"]

            rango_permitido = r_max_esp - r_min_esp
            if rango_permitido <= 0:
                rango_permitido = 1

            if min_obs < r_min_esp:
                pct_bajo = ((r_min_esp - min_obs) / rango_permitido) * 100
            else:
                pct_bajo = 0

            if max_obs > r_max_esp:
                pct_alto = ((max_obs - r_max_esp) / rango_permitido) * 100
            else:
                pct_alto = 0

            pct_desviacion = max(pct_bajo, pct_alto)

            if pct_bajo > 0 and pct_alto > 0:
                estado = "FUERA: Rango (ambos)"
            elif pct_bajo > 0:
                estado = "BAJO: Bajo mínimo"
            elif pct_alto > 0:
                estado = "ALTO: Sobre máximo"
            else:
                estado = "OK: Dentro de rango"

            if pct_desviacion == 0:
                desviacion = f"OK (0%)"
            elif pct_desviacion <= 10:
                desviacion = f"Normal ({pct_desviacion:.1f}%)"
            elif pct_desviacion <= 25:
                desviacion = f"Advertencia ({pct_desviacion:.1f}%)"
            else:
                desviacion = f"CRÍTICO ({pct_desviacion:.1f}%)"

        validaciones.append(
            {
                "ID_Tecnico": id_tec,
                "Min_Esperado": r_min_esp,
                "Max_Esperado": r_max_esp,
                "Min_Observado": min_obs,
                "Max_Observado": max_obs,
                "Estado_Rango": estado,
                "Analisis_Severidad": desviacion,
            }
        )

    return pd.DataFrame(validaciones)
