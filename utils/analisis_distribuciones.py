import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats as scipy_stats

from utils.distribuciones import crear_distribucion
from utils.cargar_variables_prototipo import cargar_variables_prototipo


OUTPUT_DIR = "output/analisis_distribuciones/"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def cargar_datos():
    ruta = "input/datos_ejemplo.csv"
    if os.path.exists(ruta):
        return pd.read_csv(ruta)
    return _generar_datos_sinteticos()


def _generar_datos_sinteticos(n_filas=22, semilla=42):
    np.random.seed(semilla)
    return pd.DataFrame({
        "1GEV007CE": np.random.normal(267.8, 2.5, n_filas),
        "1FSRFTB504": np.random.normal(782.5, 4.0, n_filas),
        "1FSRTE502C": np.random.normal(402.3, 0.6, n_filas),
        "1FRSTE503A": np.random.normal(537.0, 1.2, n_filas),
        "1FSRPT501": np.random.normal(173.0, 0.8, n_filas),
        "1FSRPT504": np.random.normal(166.0, 0.5, n_filas),
        "1FRSPT526": np.random.normal(30.0, 0.25, n_filas),
    })


def ajustar_distribuciones(datos: pd.Series):
    candidatos = {}
    for nombre_dist in ["Normal", "Weibull", "LogNormal", "Gamma"]:
        try:
            dist = crear_distribucion(nombre_dist)
            params = dist.ajustar(datos)
            candidatos[nombre_dist] = {
                "dist": dist,
                "params": params,
                "ks_pvalue": params["gof_value"],
            }
        except Exception:
            continue

    if not candidatos:
        return None

    mejor_nombre = max(candidatos, key=lambda x: candidatos[x]["ks_pvalue"])
    return {
        "candidatos": candidatos,
        "mejor_nombre": mejor_nombre,
        "mejor": candidatos[mejor_nombre],
    }


def generar_histograma(id_variable, datos, resultados, nombre_amigable=""):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"Distribucion de {nombre_amigable or id_variable}", fontsize=16, fontweight="bold")

    colores = {"Normal": "#2E86AB", "Weibull": "#E76F51", "LogNormal": "#2A9D8F", "Gamma": "#8338EC"}
    x = np.linspace(datos.min(), datos.max(), 200)

    ax = axes[0, 0]
    ax.hist(datos, bins="auto", density=True, alpha=0.6, color="gray", edgecolor="black", label="Datos")
    for nombre, cand in resultados["candidatos"].items():
        y = cand["dist"].pdf(x)
        estilo = "-" if nombre == resultados["mejor_nombre"] else "--"
        lw = 3 if nombre == resultados["mejor_nombre"] else 1.5
        ax.plot(x, y, color=colores.get(nombre, "black"), linestyle=estilo, linewidth=lw,
                label=f"{nombre} (p={cand['ks_pvalue']:.3f})")
    ax.set_xlabel("Valor")
    ax.set_ylabel("Densidad")
    ax.set_title("Distribuciones ajustadas")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    ax = axes[0, 1]
    ax.hist(datos, bins="auto", density=True, alpha=0.6, color="gray", edgecolor="black")
    mejor = resultados["mejor"]
    ax.plot(x, mejor["dist"].pdf(x), color=colores.get(resultados["mejor_nombre"], "red"), linewidth=2.5)
    ax2 = ax.twinx()
    ax2.plot(x, mejor["dist"].cdf(x), color="red", linestyle="--", linewidth=1.5, alpha=0.7, label="CDF")
    ax.set_xlabel("Valor")
    ax.set_title(f"Mejor: {resultados['mejor_nombre']}")
    ax.grid(True, alpha=0.3)

    ax = axes[1, 0]
    datos_std = (datos - datos.mean()) / datos.std()
    scipy_stats.probplot(datos_std, dist="norm", plot=ax)
    ax.set_title(f"Q-Q Plot ({resultados['mejor_nombre']})")
    ax.grid(True, alpha=0.3)

    ax = axes[1, 1]
    ax.axis("off")
    stats_text = (
        f"N observaciones:  {len(datos)}\n"
        f"Media:            {datos.mean():.4f}\n"
        f"Mediana:          {datos.median():.4f}\n"
        f"Desv. estandar:   {datos.std():.4f}\n"
        f"Minimo:           {datos.min():.4f}\n"
        f"Maximo:           {datos.max():.4f}\n"
        f"Asimetria:        {datos.skew():.4f}\n"
        f"Curtosis:         {datos.kurtosis():.4f}\n\n"
        f"Seleccionada: {resultados['mejor_nombre']}\n"
        f"KS p-value: {resultados['mejor']['ks_pvalue']:.4f}\n"
        f"Parametros: {resultados['mejor']['params']['notas']}"
    )
    ax.text(0.05, 0.95, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment="top", fontfamily="monospace",
            bbox=dict(boxstyle="round", facecolor="lightgray", alpha=0.5))

    plt.tight_layout()
    ruta = os.path.join(OUTPUT_DIR, f"{id_variable}_distribucion.png")
    plt.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close()


def ejecutar_analisis():
    datos = cargar_datos()
    catalogo = cargar_variables_prototipo()
    resultados_globales = []

    for id_variable in datos.columns:
        fila_cat = catalogo[catalogo["ID_Tecnico"] == id_variable]
        nombre_amigable = fila_cat.iloc[0].get("Nombre_amigable", "") if not fila_cat.empty else ""

        datos_var = datos[id_variable].dropna()
        resultados = ajustar_distribuciones(datos_var)
        if resultados is None:
            continue

        generar_histograma(id_variable, datos_var, resultados, nombre_amigable)

        mejor = resultados["mejor"]
        resultados_globales.append({
            "ID_Tecnico": id_variable,
            "Nombre_amigable": nombre_amigable,
            "N_observaciones": len(datos_var),
            "Media": datos_var.mean(),
            "Std": datos_var.std(),
            "Min": datos_var.min(),
            "Max": datos_var.max(),
            "Mejor_distribucion": resultados["mejor_nombre"],
            "KS_pvalue": mejor["ks_pvalue"],
            "Param1": mejor["params"]["param1"],
            "Param2": mejor["params"]["param2"],
            "Param3": mejor["params"]["param3"],
            "Notas": mejor["params"]["notas"],
        })

    df_resumen = pd.DataFrame(resultados_globales)
    df_resumen.to_csv(os.path.join(OUTPUT_DIR, "resumen_distribuciones.csv"), index=False, encoding="utf-8")
    return df_resumen


if __name__ == "__main__":
    ejecutar_analisis()
