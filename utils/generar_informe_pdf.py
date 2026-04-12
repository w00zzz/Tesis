import os
import pandas as pd
from datetime import datetime

try:
    from fpdf import FPDF
except ImportError:
    print("ERROR: fpdf2 no esta instalado. Ejecuta: uv add fpdf2")
    exit(1)

from utils.cargar_variables_prototipo import cargar_variables_prototipo
from utils.analisis_distribuciones import ejecutar_analisis


class InformePDF(FPDF):

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "Simulador de Turbina de Vapor - Semana 2", 0, 0, "L")
        self.cell(0, 8, datetime.now().strftime("%Y-%m-%d"), 0, 1, "R")
        self.line(10, 13, 200, 13)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", 0, 0, "C")

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(46, 134, 171)
        self.cell(0, 10, title, 0, 1, "L")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(46, 134, 171)
        self.cell(0, 8, title, 0, 1, "L")
        self.ln(2)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, text)
        self.ln(3)

    def bold_text(self, label, value):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 0, 0)
        w = self.get_string_width(label + ": ") + 2
        self.cell(w, 5, label + ": ", 0, 0)
        self.set_font("Helvetica", "", 10)
        self.cell(0, 5, str(value), 0, 1)


def generar_informe_pdf():
    df_analisis = ejecutar_analisis()
    catalogo = cargar_variables_prototipo()

    pdf = InformePDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Portada
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(46, 134, 171)
    pdf.cell(0, 15, "Simulador de Datos de Sensores", 0, 1, "C")
    pdf.cell(0, 15, "para la Turbina de Vapor", 0, 1, "C")
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "basado en la Caracterizacion Estadistica", 0, 1, "C")
    pdf.cell(0, 10, "de Datos Historicos SCADA", 0, 1, "C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, "Semana 2: Analisis de Distribuciones", 0, 1, "C")
    pdf.cell(0, 8, "y Modelo de Simulacion", 0, 1, "C")
    pdf.ln(15)

    pdf.set_font("Helvetica", "", 11)
    info = [
        ("Metodo", "Carga-Resistencia"),
        ("Variables SCADA", "7"),
        ("Mecanismos", "7 (SPE, WED, Choque termico, SCC, Creep, Fatiga, Vibraciones)"),
        ("Distribuciones", "Normal, Weibull, LogNormal, Gamma"),
        ("Modelo temporal", "AR(1) con phi = 0.7"),
    ]
    for label, value in info:
        pdf.bold_text(label, value)

    # Introduccion
    pdf.add_page()
    pdf.chapter_title("1. Introduccion")
    pdf.body_text(
        "Se caracterizaron estadisticamente las variables del Anexo 1 de la tesis "
        "de referencia y se disenyo el modelo de datos del simulador."
    )
    pdf.section_title("1.1 Catalogo de variables")
    pdf.body_text(
        f"Catalogo con {len(catalogo)} registros: "
        f"{len(catalogo[catalogo['Tipo_en_modelo'] == 'Carga'])} variables SCADA y "
        f"{len(catalogo[catalogo['Tipo_en_modelo'] == 'Resistencia'])} propiedades de materiales."
    )
    pdf.section_title("1.2 Modelo Entidad-Relacion")
    pdf.body_text(
        "Modelo con 4 tablas normalizadas: Variable, ParametroEstadistico, "
        "Simulacion y RegistroSimulado."
    )
    pdf.section_title("1.3 Modelo temporal AR(1)")
    pdf.body_text(
        "Modelo autorregresivo de orden 1 para series temporales con autocorrelacion."
    )
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(46, 134, 171)
    pdf.cell(0, 8, "X_t = mu + phi * (X_{t-1} - mu) + epsilon_t", 0, 1, "C")
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.body_text("Varianza del ruido: sigma_epsilon^2 = sigma_X^2 * (1 - phi^2). phi = 0.7.")

    # Histogramas
    pdf.add_page()
    pdf.chapter_title("2. Analisis de Distribuciones")
    pdf.body_text(
        "Se ajustaron 4 distribuciones y se selecciono la de mayor KS p-value."
    )

    histogramas_dir = "output/analisis_distribuciones/"
    histogramas = [f for f in os.listdir(histogramas_dir) if f.endswith(".png")]

    for hist_file in sorted(histogramas):
        id_var = hist_file.replace("_distribucion.png", "")
        fila_cat = catalogo[catalogo["ID_Tecnico"] == id_var]
        nombre = fila_cat.iloc[0].get("Nombre_amigable", "") if not fila_cat.empty else ""
        unidad = fila_cat.iloc[0].get("Unidad", "") if not fila_cat.empty else ""

        pdf.section_title(f"{id_var} - {nombre}")
        pdf.bold_text("Unidad", unidad)

        fila_analisis = df_analisis[df_analisis["ID_Tecnico"] == id_var]
        if not fila_analisis.empty:
            row = fila_analisis.iloc[0]
            pdf.bold_text("Distribucion", row["Mejor_distribucion"])
            pdf.bold_text("KS p-value", f"{row['KS_pvalue']:.4f}")
            pdf.bold_text("Parametros", row["Notas"])

        pdf.ln(3)
        try:
            pdf.image(os.path.join(histogramas_dir, hist_file), x=10, w=190)
        except Exception:
            pdf.body_text("(Imagen no disponible)")
        pdf.ln(5)

    # Tabla resumen
    pdf.add_page()
    pdf.chapter_title("3. Tabla Resumen")
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(46, 134, 171)
    pdf.set_text_color(255, 255, 255)
    headers = ["ID", "Nombre", "Distribucion", "Param1", "Param2", "KS p-value"]
    widths = [22, 28, 22, 28, 28, 25]
    for i, h in enumerate(headers):
        pdf.cell(widths[i], 7, h, 1, 0, "C", True)
    pdf.ln()
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 7)
    fill = False
    for _, row in df_analisis.iterrows():
        if fill:
            pdf.set_fill_color(240, 240, 240)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(widths[0], 6, str(row["ID_Tecnico"])[:12], 1, 0, "C", True)
        pdf.cell(widths[1], 6, str(row["Nombre_amigable"])[:14], 1, 0, "C", True)
        pdf.cell(widths[2], 6, str(row["Mejor_distribucion"]), 1, 0, "C", True)
        pdf.cell(widths[3], 6, f"{row['Param1']:.4f}", 1, 0, "C", True)
        pdf.cell(widths[4], 6, f"{row['Param2']:.4f}", 1, 0, "C", True)
        pdf.cell(widths[5], 6, f"{row['KS_pvalue']:.4f}", 1, 0, "C", True)
        pdf.ln()
        fill = not fill

    # Modelo AR(1)
    pdf.add_page()
    pdf.chapter_title("4. Documentacion del Modelo AR(1)")
    pdf.section_title("4.1 Autocorrelacion")
    pdf.body_text(
        "En procesos industriales las variables tienen inercia fisica. "
        "El valor actual depende del valor anterior."
    )
    pdf.section_title("4.2 Ecuacion")
    pdf.set_font("Helvetica", "I", 12)
    pdf.set_text_color(46, 134, 171)
    pdf.cell(0, 10, "X_t = mu + phi * (X_{t-1} - mu) + epsilon_t", 0, 1, "C")
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.body_text(
        "phi = 0.7 para procesos industriales. "
        "Referencia: Box & Jenkins (1976), Time Series Analysis."
    )

    output_path = "output/informe_semana2.pdf"
    pdf.output(output_path)
    print(f"Informe generado: {output_path}")


if __name__ == "__main__":
    generar_informe_pdf()
