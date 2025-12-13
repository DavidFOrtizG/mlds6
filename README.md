# Sistema de reconocimiento de señales manuales (Lenguaje de Señas Americano ASL)

Principales secciones del repositorio

- `data/` — datos crudos, preprocesados y archivos HDF5 (subcarpetas: `raw/`, `preprocessed/`, `hdf5/`).
- `docs/` — documentación del proyecto (data dictionary, model report, deployment docs, etc.).
- `scripts/` — scripts ejecutables para adquisición, preprocesamiento, entrenamiento, evaluación y despliegue.
- `src/` — código fuente del paquete `mlds6` (preprocesamiento).
- `py_env/`, `requirements.txt`, `pyproject.toml` — entorno y dependencias.

Requisitos

- Python 3.12+ (se recomienda usar un entorno virtual).
- Instalar dependencias de entrenamiento

```bash
pip install virtualenv
.\py_env\Scripts\activate
pip install -r requirements.txt
```

- Instalar dependencias de despliegue
```bash
cd /scripts/deployment_fastapi
.\env\Scripts\activate
pip install -r requirements.txt
```

## Inicio Rapido

Detalles sobre cada una de las etapas puede encontrarse en la carpeta correspondiente a cada etapa en `/docs`. Para un inicio rapido:


- Configura las credenciales de DVC para acceder al bucket de GCS
- Descarga las imagenes base y preprocesadas

```bash
dvc pull
```

En caso de cargar un nuevo conjunto de imagenes base, es posible realizar el preprocesamiento usando 

```bash
python /scripts/preprocess.py
```

- Entrenamiento: Clona este repositorio en un ambiente de colab para hacer uso de GPU, carga el notebook `/scripts/MLDS6_Optuna.ipynb`. Ejecutar este notebook producirá un modelo con selección de hyperparámetros y listo para recibir imagenes ya preprocesadas.


- Evaluación: Con el modelo ya generado se puede evaluar sobre el set de entrenamiento
```bash
python scripts/evaluation/main.py
```

- Despliegue

- API FastAPI: `scripts/deployment_fastapi/main.py`
- App Streamlit: `scripts/deployment_streamlit/app.py`.

## Estructura destacada

- `scripts/data_acquisition/` y `scripts/preprocessing` — scripts para descargar y preparar los datos.
- `scripts/deployment_fastapi/model/` — modelo serializado (`asl_model.keras`) y utilidades de predicción.
- `src/mlds6/` — paquete Python con módulos de `preprocessing`
  


## Contacto

David Francisco Ortiz Gutiérrez (david.f.ortizg@gmail.com)

Fabián Camilo Rojas Beltrán (fcrojasb@unal.edu.co)
