"""Genera el catalogo de variables en formato Excel como entregable de la Tarea 1."""
import pandas as pd
import os


def generar_excel_catalogo():
    csv_path = "output/catalogo_variables.csv"
    output_path = "output/catalogo_variables.xlsx"

    if not os.path.exists(csv_path):
        print(f"ERROR: No se encontro {csv_path}")
        return

    df = pd.read_csv(csv_path)

    columnas_tutor = [
        "ID_Tecnico",
        "Nombre_amigable",
        "Unidad",
        "Tipo_dato",
        "Tipo_en_modelo",
        "Mecanismos_asociados",
        "Ecuacion",
        "Rol_en_ecuacion",
        "Rango_min",
        "Rango_max",
        "Distribucion_observada",
        "Pregunta_planta",
    ]

    columnas_existentes = [c for c in columnas_tutor if c in df.columns]
    df_export = df[columnas_existentes]

    df_export.to_excel(output_path, index=False, engine="openpyxl")
    print(f"Catalogo Excel generado: {output_path}")
    print(f"  Filas: {len(df_export)}")
    print(f"  Columnas: {len(columnas_existentes)}")


if __name__ == "__main__":
    generar_excel_catalogo()
