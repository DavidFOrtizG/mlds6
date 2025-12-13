# Informe de salida

## Resumen Ejecutivo

Este proyecto desarrolló e implementó exitosamente un modelo de Machine Learning para la traducción de lenguaje de señas basado en MobileNetV2, alcanzando una precisión del 95% en el conjunto de prueba gracias al fine-tuning y la optimización de hiperparámetros con Optuna. La solución se desplegó utilizando una arquitectura MLOps completa, incluyendo el versionamiento de datos con DVC y GCS, y un stack serverless que consta de una API FastAPI/Docker alojada en Google Cloud Run y un frontend en Streamlit. A pesar de las altas métricas internas, la principal limitación se observa en producción: el modelo no logra generalizar completamente a ciertas señas realizadas por diferentes personas (ej. A vs. M vs. N), un desafío atribuido al uso de un dataset entrenado con un único usuario, lo cual se identifica como la principal área de mejora futura.

## Resultados del proyecto

- Resumen de los entregables y logros alcanzados en cada etapa del proyecto.
### Etapas del proyecto
- Adquisición de datos: Se entrega un codigo de descarga de datos que se conecta a la plataforma Kaggle para descargar el dataset. Adicionalmente se realiza versionamiento de los datos mediante DVC conectado a un bucket de GCS.
- Analisis Exploratorio: Se genera un notebook que realiza un analisis exploratorio de los datos, este revisa tamaño, legibilidad y  contraste de las imagenes, y adicionalmente el balanceo de clases.
- Preprocesamiento: Se entrega un codigo de preprocesamiento de datos que realiza la división de los datos en conjuntos de entrenamiento, validación y testeo. Para cada uno de lo conjuntos de datos se realiza un preprocesamiento correspondiente a la remosión del fondo y aumento de contraste, esto con el objetivo de remover la mayor cantidad de diferencias entre los datos de entrenamiento y los que recibirá el modelo una vez se despliegue.
- Modelamiento: Se hizo uso de Transfer Learning mediante el modelo pre-entrenado MobileNetV2. La arquitectura se compone del extractor de features congelado y un cabezal de clasificación personalizado. Adicionalmente se realizó  fine-tuning sobre el backbone y optimización de hiperparámetros con Optuna.
- Despliegue: Se entregan los archivos base para el despliegue del modelo, consistente en un frontend deplegado mediante `Streamlit` como una [app](https://hiszc2t3rm4nq7ndvmr5ru.streamlit.app/) hosteada en la web de Streamlit. Para el backend, encargado de recibir imagenes, ejecutar el modelo y retornar las predicciones, se implementa una API mediante `FastAPI`, hosteada en Google Cloud Run mediante Docker. La app en streamlit envia las iamgenes al endpoint de predicción de la API, la cual retorna el resultado que luego es mostrado en Streamlit.


### Evaluación del modelo final y comparacion con el modelo base:
El modelo inicial se realizó haciendo uso del modelo pre-entrenado MobileNetV2 más un cabezal de clasificación personalizado, este modelo obtuvo un acuracy de 0.88 y un F1 de las  clases entre 0.79 y 0.94, teniendo posibilidades de mejora en varias clases.

Para el modelo final se tomo el modelo base, se realizó fine-tunning del backbone y adicionalmente se realizó optimización de los hiperparámetros del cabezal (cantidad de neuronas de la primera capa, cantidad de neuronas de la segunda capa, tasa de dropout y tasa de aprendizaje de entrenamiento) con Optuna

### Descripción de los resultados

En el conjunto de datos prueba el modelo se desempeña de forma correcta y muestra una gran capacidad de distinción de las diferentes señas, con una precisión del 95%. Sin embargo, al momento de entregarle imagenes de señas realizadas por otras personas mediante la app, se observa que la capacidad de distinguir ciertas señas, especialmente aquellas que muestran señas similares (como A - M - N - S - T y Y - L - J - I - Z) disminuye por la similitud que estas tienen.

## Lecciones aprendidas
- Se reconoce la utilidad del uso de servicios Serverless como Google Cloud Run para el despliegue de aplicaciones de este estilo. De igual forma, la versatilidad de Docker para hacer el despliegue del modelo y sus dependencias de forma sencilla fue de gran utilidad para el proyecto.
- El uso de DVC para el versionamiento de datos resulto siendo de gran utilidad debido al gran peso de los conjuntos de datos utilizados, tanto en espacio como en computo para el preprocesamiento. DVC permitió cambiar entre entornos locales y Colab de forma fluida.
- Una de los desafios del proyecto fue el uso de herramientas como Colab por los recurso computacionales que ofrece al tiempo que se desarrolla en local. El aprender a mover el proyecto de un ambiente a otro de forma fluida fue de gran utilidad
- Como se mencionó en la sección anterior, al usar un dataset de señas realizadas por una sola persona condiciona el performance del modelo a imagenes similares a las del dataset original. Esto afecta el modelo al intentar predecir iamgenes de señas ajenas al dataset original. El uso de un dataset mas variado (diferentes personas, angulos, etc) podria beneficiar el desempeño del modelo en producción.

## Impacto del proyecto

El objetivo del proyecto es poder brindar una herramienta útil, fácil y confiable que permita la enseñanza y el aprendizaje del lenguaje de señas.

## Conclusiones

- Alto Rendimiento en Prueba: El modelo final, optimizado mediante fine-tuning y Optuna, logró una precisión del 95% en el conjunto de prueba, demostrando la eficacia del Transfer Learning con MobileNetV2.

- Despliegue Exitoso: Se validó un flujo MLOps robusto utilizando DVC para datos y un stack serverless (FastAPI/Docker en Google Cloud Run) para la API y Streamlit para el frontend.

- Desafío de Generalización: La limitación del dataset monousuario causó una disminución en el rendimiento en producción, especialmente en la distinción de señas similares, sugiriendo la necesidad de mayor diversidad de datos.

