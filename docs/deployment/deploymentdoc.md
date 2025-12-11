
# Despliegue de modelo (fast-api)

## Infraestructura

- **Nombre del modelo:** asl_model
- **Plataforma de despliegue:** DVC GCP y fast-api
- **Requisitos técnicos:** (lista de requisitos técnicos necesarios para el despliegue, como versión de Python, bibliotecas de terceros, hardware, etc.)
- **Requisitos de seguridad:** (lista de requisitos de seguridad necesarios para el despliegue, como autenticación, encriptación de datos, etc.)
- **Diagrama de arquitectura:** (imagen que muestra la arquitectura del sistema que se utilizará para desplegar el modelo)

## Código de despliegue

- **Archivo principal:** (nombre del archivo principal que contiene el código de despliegue)
- **Rutas de acceso a los archivos:** (lista de rutas de acceso a los archivos necesarios para el despliegue)
- **Variables de entorno:** (lista de variables de entorno necesarias para el despliegue)

## Documentación del despliegue

- **Instrucciones de instalación:** (instrucciones detalladas para instalar el modelo en la plataforma de despliegue)
- **Instrucciones de configuración:** (instrucciones detalladas para configurar el modelo en la plataforma de despliegue)
- **Instrucciones de uso:** (instrucciones detalladas para utilizar el modelo en la plataforma de despliegue)
- **Instrucciones de mantenimiento:** (instrucciones detalladas para mantener el modelo en la plataforma de despliegue)

# Despliegue pagina web (streamlit)

## Infraestructura

- **Plataforma de despliegue:** Streamlit Cloud

- **Requisitos técnicos:**

python 3.12

streamlit 1.52.1

numpy 2.0.2

pandas 2.2.2

ImageIO 2.37.2

pillow 11.3.0

requests 2.32.4

## Código de despliegue

- **Archivo principal:** app.py
- **Rutas de acceso a los archivos:** scripts/deployment_streamlit/app.py

## Documentación del despliegue

- **Instrucciones de instalación:**

1. Creación del archivo app.py usando las librerias de streamlit para generar las características deseadas de la página web
2. Guardar el archivo requirements.txt con las librerías necesarias para ejecutar app.py
3. En Streamlit Cloud se debe especificar el repositorio de GitHub donde esta el código de despliegue (se debe ser administrador del repositorio) y definirle la ruta del archivo app.py

- **Instrucciones de configuración:**

Se utilizaron las funciones de streamlit set_page_config, title, header, divider, markdown y subheader, checkbox, button, para definir el nombre de la página, los componentes de texto de la pagina, entre otros elementos de la página web.

Adicionalmente, se utilizo la función camara_input para tomar una foto de la mano del cliente, se usa la funcion Image para abrir la foto tomada, y se guarda la foto dentro del entorno de trabajo,

Por medio del siguiente código se realizó la solicitud post hacia la arquitectura de fast-api que genera la predicción.

Por último, se entrega la respuesta de la predicción por medio de la función info y se entrega un gráfico de barras de las probabilidades generadas por el modelo por medio de la función bar_chart.

- **Instrucciones de uso:** 

1. El cliente debe habilitar la camara por medio de un checkbox
2. Realizar una foto de la mano realizando la seña, es importante que la foto debe ser sólo para la seña y no incluir más elementos
3. La pagina web comunicara al cliente si la imagen fue almacenada correctamente
4. El cliente debe apretar el botón "Predecir"
5. La página web tomara algunos segundos en realizar una predicción, y luego arrojara la predicción de la seña junto con un gráfico de barras con las probabilidades de cada seña.

