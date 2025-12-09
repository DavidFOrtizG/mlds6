
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import io
import json
import requests

# Título de la página

st.set_page_config(page_title='Sistema de reconocimiento de señales manuales')

st.title('Sistema de reconocimiento de señales manuales (Lenguaje de Señas Americano ASL):')

st.header('aplicación de visión por computadora')

st.divider()

st.markdown('''
Por medio de esta página Web se realiza el despliegue del proyecto ***Sistema de reconocimiento de señales manuales (Lenguaje de Señas Americano ASL):*** 
_aplicación de visión por computadora* del Curso "MLDS6 - Metodologías Ágiles para el Desarrollo de Proyectos con Machine Learning"_.
  
El cual consiste en tomar una foto tomada por el cliente de una seña y predecir por medio de un modelo de aprendizaje automático a que seña hace referencia la imagen.
''')

st.divider()

c29, c30, c31 = st.columns([0.5,7,0.5])

with c30:

  st.subheader('Instrucciones:')
  
  st.markdown('''
  Por favor toma una foto de tu seña para poder generar la predicción

  En la foto debe aparecer únicamente la mano realizando la seña deseada.
  ''')

  enable = st.checkbox("Enable camera")
  
  picture = st.camera_input("Take a picture", disabled=not enable)
  
  if picture is not None:
    
    image = Image.open(picture)
    
    save_path = "image.jpg"

    image.save(save_path)
  
    st.success("Imagen almacenada")
    
    st.subheader('Ahora presiona en el botón "Predecir"')
    
    if st.button("Predecir"):
  
      image_path = "image.jpg"
      
      with open(image_path, 'rb') as image_file:
        
        files = {'file': (image_path, image_file, 'image/jpeg')}
        response = requests.post("https://fastapi-asl-1074222614966.us-central1.run.app/uploadfile/", files=files)
        
        response_data = json.loads(response.text)
        prediction = response_data.get('prediction')
        
        labels = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','del','nothing','space']
        
        predict = np.array(list(prediction.values()), dtype=np.float32)
        
        label_predict = np.argmax(predict)
        
        sign = labels[label_predict]
        
        df = pd.DataFrame(list(prediction.values()), index=labels, columns=["Probabilidad"])

        info_box_result = st.info(f"""
        Tu seña es: {sign}
                                  """)
        
        st.subheader(f"Probabilidades")
        
        st.bar_chart(df)

        gracias  = st.success(f"""
        Gracias por usar nuestra aplicación !
                                  """)
      
    else:

      st.info(f"""
      Esperando a que presiones el botón...
      """)
  
  st.stop()
