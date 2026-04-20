import pandas as pd
import numpy as np


def generar_informe_calidad(df, nombre_dataset="Dataset"):
    informe = []

    total_filas = len(df)
    duplicados = df.duplicated().sum()

    for col in df.columns:
        nulos = df[col].isnull().sum()
        porcentaje_nulos = (nulos / total_filas) * 100 if total_filas > 0 else 0
        tipo_dato = str(df[col].dtype)
        unicos = df[col].nunique()

        completitud = 100 - porcentaje_nulos

        if df[col].dtype in ["float64", "int64"]:
            max_val = df[col].max()
            if pd.notna(max_val) and abs(max_val) > 1e10:
                validez = "Verificar valores extremos"
            else:
                validez = "OK"
        elif df[col].dtype == "object":
            if nulos > 0 or unicos == 0:
                validez = "Verificar campo vacío"
            else:
                validez = "OK"
        else:
            validez = "OK"

        if col == "Rango_min" and "Rango_max" in df.columns:
            rango_min = df["Rango_min"]
            rango_max = df["Rango_max"]
            if (rango_min > rango_max).any():
                consistencia = "Verificar rango (min > max)"
            else:
                consistencia = "OK"
        elif col in ["Rango_min", "Rango_max", "Rango_operativo"]:
            consistencia = "OK"
        elif col == "Unidad" and "Tipo_dato" in df.columns:
            consistencia = "OK"
        elif df[col].dtype == "object":
            if unicos == 1 and nombre_dataset == "Dataset":
                consistencia = "Verificar valor único"
            else:
                consistencia = "OK"
        else:
            consistencia = "OK"

        informe.append(
            {
                "Columna": col,
                "Tipo": tipo_dato,
                "Nulos": nulos,
                "% Nulos": round(porcentaje_nulos, 2),
                "Unicos": unicos,
                "Completitud %": round(completitud, 2),
                "Consistencia": consistencia,
                "Validez": validez,
            }
        )

    resumen_df = pd.DataFrame(informe)

    print(f"\n--- Resumen de Calidad: {nombre_dataset} ---")
    print(f"Total de registros: {total_filas}")
    print(f"Filas duplicadas: {duplicados}")
    print("-" * (30 + len(nombre_dataset)))

    return resumen_df
