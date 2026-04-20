## Estructura del Proyecto

- `utils/`: Módulos de lógica (Carga, procesamiento, validación, estadísticas).
- `config/`: Configuración de reglas de negocio en formato JSON.
- `input/`: Datos de entrada (CSV del Anexo 1).
- `output/`: Resultados generados.
- `db/`: Scripts SQL para la base de datos.
- `diagramas/`: Diagramas UML.
- `pipeline.py`: Orquestador principal.
- `main.py`: Entrada para pruebas.

## Instalación

```bash
uv sync
cp .env.example .env
```

## Uso

### Pipeline completo
```bash
uv run pipeline.py
```

Este comando:
1. Carga el catálogo de 14 variables
2. Carga datos reales del Anexo 1
3. Ajusta distribuciones estadísticas
4. Genera histogramas
5. Valida rangos y reglas
6. Genera Excel de resultados

### Generar PDF con histogramas
```bash
uv run python -c "from utils.generar_informe_pdf import generar_informe_pdf; generar_informe_pdf()"
```
Archivo: `output/informe_semana2.pdf`

### Main (opciones)
```bash
# Ver stats de datos
uv run main.py --datos

# Generar histogramas
uv run main.py --histogramas

# Generar simulación
uv run main.py --simulacion
```

## Archivos Generados

| Archivo | Descripción |
|---------|-------------|
| `output/catalogo_variables.csv` | Catálogo de variables |
| `output/resultados_pipeline.xlsx` | Resultados Excel |
| `output/informe_semana2.pdf` | PDF con histogramas |
| `output/analisis_distribuciones/*.png` | Histogramas por variable |

## Diagramas UML

En `diagramas/`:

| Archivo | Descripción |
|---------|-------------|
| `clases_actual.png` | Diagrama de clases |
| `secuencia_actual.png` | Diagrama de secuencia |

Para regenerar (requiere PlantUML + Graphviz):
```bash
cd diagramas
java -jar plantuml.jar -tpng -pipe < diagrama_clases_uml.puml > clases_actual.png
java -jar plantuml.jar -tpng -pipe < diagrama_secuencia_uml.puml > secuencia_actual.png
```
