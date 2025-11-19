
# Project Charter - Entendimiento del Negocio

## Nombre del Proyecto

Sistema de reconocimiento de señales manuales (Lenguaje de Señas Americano ASL): 
aplicación de visión por computadora

## Objetivo del Proyecto

El objetivo principal del presente proyecto es desarrollar un sistema robusto, capaz de traducir de manera automática fotos de señas visuales a texto. Para esto se utilizará una base de datos con imágenes de señas del Lenguaje de Señas Americano (ASL) con 29 categorías distintas, cada una representando una letra/carácter especifico. Para una mayor comprensión de estas categorías consultar la información completa en el diccionario de dato anexo. 

Las fotos serán subidas por el cliente por medio de una página web, y luego el sistema debe estar en la capacidad de reconocer a que letra en particular se refiere la imagen, y darle como resultado al cliente esta letra/carácter.

## Alcance del Proyecto

### Incluye:

- El proyecto se realizará utilizando un conjunto de datos de imágenes de señas asociadas al alfabeto de Lenguaje de Señas Americano (ASL), estructurado en 29 categorías distintas. Este dataset, obtenido de Kaggle, cuenta con 87.000 imágenes de señas.

- Al finalizar el proyecto se espera haber desarrollado un modelo de aprendizaje profundo capaz de clasificar cada una de las fotos cargadas por el cliente entre alguna letra/carácter del alfabeto de ASL. Los resultados incluyen la obtención de un modelo entrenado y optimizado, junto con un informe detallado de métricas de rendimiento como accuracy global, precisión, recall y F1-score para cada una de las categorías, demostrando la capacidad del sistema para realizar inferencias correctas sobre fotos nuevas.

- Se espera que la página web al recibir una foto sea capaz de detectar de manera automática a que letra/carácter hace referencia la seña de la foto y le indique al cliente el resultado de esta predicción.

- Criterios de éxito: obtener una red neuronal con un Accuracy Global >= 90%, y que métricas como la precisión, el recall y el f1-Score tengan un valor mayor al 80% individual para cada una de las categorías. Adicionalmente, que la página web permita subir una foto y arrojar un resultado asociado a la predicción de la seña. 

### Excluye:

- No podrá procesar videos cargados ni en tiempo real de señas. Sólo imágenes cargadas.

- No se espera que detecte letras del alfabeto ASL, no tiene capacidad de detectar palabras o frases completas.

- El sistema sólo podrá detectar señas del lenguaje ASL, no otras variantes (Lenguaje de Señas Colombiano, etc.)

- No se desarrollara una aplicación móvil para ningún sistema operativo, sólo funcionara a través de una página web.

## Metodología

La metodología del proyecto seguirá un enfoque iterativo y basado en TSDP. Inicialmente, el documento actual describe la etapa de Entendimiento del Negocio, que incluye la definición del proyecto y los objetivos del mismo. Posteriormente, se realizara la etapa de Adquisición Comprensión y Procesamiento de Datos,  lo cual incluye cargar la base de datos, realizar una exploración inicial, que permita revisar el balanceo de las categorías, la homogeneidad del tamaño de las imágenes y la calidad de las mismas.  Se realizará el pre-procesamiento y aumentación de datos para preparar las imágenes para el entrenamiento. En la Fase de Modelado se hará la selección y el entrenamiento de una red neuronal convolucional (CNN), posiblemente utilizando técnicas de Transfer Learning para aprovechar modelos pre-entrenados, esta etapa también comprende la evaluación rigurosa utilizando métricas de clasificación estándar (accuracy, precisión, recall y F1-Score entre otras) sobre un conjunto de prueba independiente, para validar su precisión y capacidad de generalización antes de presentar las conclusiones y los posibles pasos futuros. Finalmente, el modelo será desplegado por medio de un servicio web.

## Cronograma

| Etapa | Duración Estimada | Fechas |
|------|---------|-------|
| Entendimiento del negocio y carga de datos | 1 semana | del 14 de noviembre al 20 de noviembre de 2025 |
| Pre-procesamiento y análisis exploratorio de datos| 1 semana | del 21 de noviembre al 27 de noviembre de 2025 |
| Modelamiento y extracción de características | 1 semana | del 28 de noviembre al 4 de diciembre de 2025 |
| Despliegue | 6 días | del 5 de diciembre al 10 de diciembre de 2025 |
| Evaluación y entrega final | 4 días | del 11 de diciembre al 14 de diciembre de 2025|

## Equipo del Proyecto

- David Francisco Ortiz Gutiérrez (david.f.ortizg@gmail.com)
- Fabián Camilo Rojas Beltrán (fcrojasb@unal.edu.co)

## Presupuesto


| Categoría de Gasto                 | Descripción                                                                 | Costo Estimado (USD) | Notas                                                                                       |
|-----------------------------------|-----------------------------------------------------------------------------|-----------------------|---------------------------------------------------------------------------------------------|
| I. Personal                     |                                                                             |                       |                                                                                             |
| 2 Científicos de Datos            | Pre-procesamiento, diseño del modelo, optimización, despliegue del modelo   | $6.500                | 1 mes a tiempo parcial                                                                       |
| II. Infraestructura y Software  |                                                                             |                       |                                                                                             |
| Almacenamiento Cloud GCP          | Para almacenar el dataset de imágenes                                       | $10                   | 10GB por 1 mes                                                                               |
| Licencias de Software             | Herramientas para el desarrollo                                             | $0                    | Herramientas open-source (Python, TensorFlow/PyTorch, scikit-learn)                         |
| Plataforma de Despliegue          |                                                                             | $0                    | Se utilizarán herramientas gratuitas como MLFlow, FastAPI, etc.                             |
| III. Misceláneos                |                                                                             |                       |                                                                                             |
| Contingencias                     | Fondo de imprevistos                                                        | $50                   | Posible licenciamiento adicional u otros costos marginales                                  |
| *TOTAL ESTIMADO DEL PROYECTO*  |                                                                             | *$6.560*            |                                                                                             |

## Stakeholders

- Instituciones educativas, estudiantes, docentes, personas con discapacidades auditivas y de habla.
- Los integrantes de las instituciones educativas actúan como validadores de la funcionalidad de la herramienta como instrumento para la enseñanza y el aprendizaje del lenguaje de señas. A su vez, personas con discapacidades auditivas y del habla, validaran la herramienta como aplicación para la asistencia básica.
- Expectativa: crear una interfaz intuitiva y sencilla, con predicciones de las fotos de señas confiables.

## Aprobaciones

- Científico de Datos: David Francisco Ortiz Gutiérrez
- Científico de Datos: Fabián Camilo Rojas Beltrán
