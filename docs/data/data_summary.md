
# Reporte de Datos

Este Dataset contiene imágenes de señas del Lenguaje de Señas del Alfabeto Ingles, para 29 clases, 26 de ellas para las letras de la A a la Z, y 3 adicionales para el carácter 'del' o eliminar, 'space' o espacio, 'nothing' para una imagen sin señas.

## Resumen general de los datos

El dataset cuenta con un total de 87028 archivos, correspondientes a imágenes en formato .jpg. 

## Resumen de calidad de los datos

Todos los archivos pueden ser leídos como imágenes, además en las etiquetas no se tienen valores nulos o faltantes. Todas las imágenes tienen un tamaño de 200x200 pixeles.

## Variable objetivo

Las imágenes están clasificadas en las etiquetas 'A' 'B' 'C' 'D' 'E' 'F' 'G' 'H' 'I' 'J' 'K' 'L' 'M' 'N' 'O' 'P'
 'Q' 'R' 'S' 'T' 'U' 'V' 'W' 'X' 'Y' 'Z' 'del' 'space' 'nothing'. Estas están perfectamente balanceadas como se ve a continuación:


![Distribucion de Etiquetas](../assets/Distribucion_etiqueta.JPG)


## Variables individuales

En cuanto a la distribución de los pixeles de las imágenes se evidencia que no existen valores atípicos en relación al promedio pero si en relación a la desviación estándar:


![Distribucion pixeles](../assets/Distribucion_pixeles.JPG)


Esto puede explicarse por que al parecer todas las fotos fueron tomadas en la misma habitación, con la misma iluminación y las señas son realizadas por la misma persona, por lo tanto, el promedio de los pixeles es similar entre imágenes:


![Muestra imagenes](../assets/Muestra_imagenes.JPG)


Por otro lado, los valores atípicos asociados a la desviación estándar se deben a imágenes con alto contraste, específicamente a imágenes donde la mano se ve oscura, mientras que el fondo de la habitación en todas las imágenes está bien iluminado:


![Outliers desviacion](../assets/Outliers_desviacion.JPG)


Las estrategias de pre-procesamiento que se utilizaran dadas tanto las características de los datos, como la tarea a ejecutar (crear un sistema que permita clasificar fotos nuevas subidas por el usuario y las clasifique entre las señas del alfabeto del Lenguaje de Señas Americano) están:

•	Eliminar fondo
•	Recortar parte principal de la imagen
•	Redimensionar la imagen

