import os
import argparse
import pandas as pd
import numpy as np
from dotenv import load_dotenv

from utils import (
    cargar_variables_prototipo,
    SimuladorTurbina,
    validar_rangos_operativos,
    printdf,
)
from utils.analisis_distribuciones import ejecutar_analisis as ejecutar_analisis_distribuciones

load_dotenv()


def prueba_rapida():
    catalogo = cargar_variables_prototipo()
    simulador = SimuladorTurbina(catalogo_df=catalogo, phi_default=0.7)
    datos = pd.read_csv("input/datos_ejemplo.csv")

    params = simulador.ajustar_distribuciones(datos)
    df_resumen = simulador.resumen_parametros()
    printdf(df_resumen, "Parametros de Distribuciones")

    for id_var in ["1GEV007CE", "1FSRFTB504", "1FSRTE502C"]:
        if id_var in simulador.distribuciones:
            valor = simulador.generar_valor_estatico(id_var)
            print(f"  {id_var}: {valor:.4f}")

    for id_var in ["1GEV007CE", "1FSRFTB504"]:
        if id_var in simulador.modelos_ar1:
            serie = simulador.generar_serie_temporal(id_var, n_puntos=10)
            print(f"  {id_var}: media={serie.mean():.2f}, std={serie.std():.2f}")

    stats = pd.DataFrame([
        {"ID_Tecnico": k, "Min_Muestra": v["param1"] - 2*v["param2"], "Max_Muestra": v["param1"] + 2*v["param2"]}
        for k, v in params.items()
    ])
    reporte = validar_rangos_operativos(catalogo, stats)
    printdf(reporte, "Validacion de Rangos")


def prueba_distribuciones():
    catalogo = cargar_variables_prototipo()
    simulador = SimuladorTurbina(catalogo_df=catalogo)
    datos = pd.read_csv("input/datos_ejemplo.csv")
    simulador.ajustar_distribuciones(datos)
    df_resumen = simulador.resumen_parametros()
    printdf(df_resumen, "Parametros")


def prueba_simulacion():
    catalogo = cargar_variables_prototipo()
    simulador = SimuladorTurbina(catalogo_df=catalogo)
    datos = pd.read_csv("input/datos_ejemplo.csv")
    simulador.ajustar_distribuciones(datos)
    df_sim = simulador.generar_simulacion(n_dias=1, freq_minutos=60)
    df_sim.to_csv("output/simulacion_prueba.csv", index=False)
    print(f"Simulacion guardada: {len(df_sim)} registros")


def prueba_histogramas():
    ejecutar_analisis_distribuciones()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--distribuciones", action="store_true")
    parser.add_argument("--simulacion", action="store_true")
    parser.add_argument("--histogramas", action="store_true")
    args = parser.parse_args()

    if args.distribuciones:
        prueba_distribuciones()
    elif args.simulacion:
        prueba_simulacion()
    elif args.histogramas:
        prueba_histogramas()
    else:
        prueba_rapida()


if __name__ == "__main__":
    main()
