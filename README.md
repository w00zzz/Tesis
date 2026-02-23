## Estructura del Proyecto

- `utils/`: Módulos de lógica (Carga, procesamiento, validación, estadísticas).
- `config/`: Configuración de reglas de negocio en formato JSON.
- `input/`: Directorio para los datos reales (excluido de Git).
- `output/`: Resultados de los informes y catálogo (excluido de Git).
- `db/`: Scripts SQL para la base de datos de simulación.
- `pipeline.py`: Orquestador principal del flujo completo.
- `main.py`: Entrada secundaria para pruebas y prototipado rápido.

## Instalación y Configuración

1. **Instalar Dependencias** (Usando [uv](https://github.com/astral-sh/uv)):

   ```bash
   uv sync
   ```

2. **Configurar Entorno**:
   Copia el archivo de ejemplo y ajusta tus rutas:

   ```bash
   cp .env.example .env
   ```

3. **Definir Reglas**:
   Edita `config/reglas_validacion.json` para agregar validaciones personalizadas.

## Uso

Para ejecutar el pipeline completo de análisis:

```bash
uv run pipeline.py
```

Esto generará un reporte detallado en el terminal y exportará un archivo Excel en la carpeta `output/`.

O de forma manual ejecutando el main para probar:

```bash
uv run main.py
```

## Esquema de Datos

El sistema está diseñado para un modelo Entidad-Relación que gestiona simulaciones y registros de series de tiempo. El esquema SQL base se encuentra en `db/schema_er.sql`.
