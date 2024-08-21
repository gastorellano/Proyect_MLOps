# Proyecto Individual N° 1 MLOps: Sistema de Recomendación de Películas

Este proyecto representa mi primer gran reto en la etapa de labs, donde asumiré el rol de un MLOps Engineer con la misión de transformar datos crudos y sin procesar en un sistema de recomendación funcional.

## Contexto
Nuestro cliente ofrece servicios de agregación de plataformas de streaming. Los datos disponibles están en un estado bastante rudimentario: anidados, desordenados, y con un claro déficit de procesos automatizados para actualizar información crucial como nuevas películas o series. Deberemos preparar un MVP (Producto Mínimo Viable) que sea funcional y eficaz en un tiempo muy limitado.

## Objetivo
El objetivo es desarrollar un sistema de recomendación de películas que no solo solucione un problema de negocio real, sino que también sea escalable y fácil de mantener en un entorno de producción. Resulta necesario focalizar en la transformación de datos en el proceso de ETL, y en realizar un Análisis Exploratorio de Datos (EDA) completo y razonable.

## Índice
1. [Contexto](#Contexto)
2. [Objetico](#Objetivo)
3. [Consideraciones Iniciales](#consideraciones-iniciales)
4. [Proceso de ETL (Extracción, Carga y Transformación de los Datos)](#Proceso-de-ETL))
5. [Creación de API](#creación-de-funciones)
6. [Análisis Exploratorio de los Datos (EDA)](#análisis-exploratorio-de-los-datos-eda)
7. [Modelo de Recomendación](#modelo-de-recomendación)
8. [Conclusión](#conclusion)

## Consideraciones iniciales
La base de datos disponible consta de dos archivos CSV que contienen aproximadamente 45,000 filas de datos sin procesar. Estos datos deben ser transformados y preparados para su utilización en al menos seis funciones clave, las cuales serán detalladas más adelante según los requisitos específicos del cliente.

Una vez desarrolladas, estas funciones se implementarán a través de una API que será desplegada en [Render](https://dashboard.render.com/), garantizando así su accesibilidad y facilidad de uso.

Además, se requiere realizar un Análisis Exploratorio de Datos (EDA) exhaustivo, cuyo objetivo será proporcionar información valiosa al departamento de Analytics del cliente, mejorando así la implementación y eficacia del modelo de recomendación.

## Proceso de ETL
En los Notebooks se encuentra un archivo dedicado al proceso de ETL (Extracción, Transformación y Carga), donde se detalla cada paso que se llevó a cabo para preparar los datos.

La información original estaba distribuida en dos archivos: **movies_dataset.csv**, que contiene datos generales sobre las películas, y **credits.csv**, enfocado en el elenco y equipo de producción. Los datos no estaban normalizados, lo que requería una serie de transformaciones antes de que pudieran ser utilizados.

Se desarrollaron funciones específicas para desanidar columnas y extraer la información relevante. Este proceso incluyó la eliminación de columnas que no aportaban valor al proyecto y que, además, añadían una complejidad innecesaria. Asimismo, se crearon nuevas columnas para almacenar los datos desanidados, vinculando las filas correspondientes a través del 'id' de la filmación.

Además, se realizó un tratamiento preliminar de valores nulos, datos faltantes y duplicados, asegurando que los datos estuvieran en un estado adecuado para su posterior análisis y uso en las funciones requeridas. Finalmente, toda la información procesada se almacenó en un archivo tipo **.parquet**. Se ha elegido este formato para almacenar los datos procesados debido a su eficiencia en la compresión y almacenamiento en columnas, lo que permite una lectura rápida y una menor utilización de memoria. Su compatibilidad con herramientas como Apache Spark y Pandas facilita su integración en el flujo de trabajo de ETL y análisis. Además, .parquet es robusto y escalable, ideal para manejar grandes volúmenes de datos y asegurar el rendimiento óptimo del sistema de recomendación.



## Creación de funciones
En el archivo **main.py** se detallan las funciones desarrolladas para la API, construida utilizando la librería FastAPI. Esta API permite acceder a las siguientes consultas sobre la base de datos procesada:

- **Películas por mes**: Permite seleccionar un mes del año y cuenta el número de estrenos ocurridos en ese mes.
- **Películas por día**: Permite seleccionar un día de la semana y cuenta el número de estrenos en ese día.
- **Score de película**: Proporciona el año de estreno y un valor numérico que representa la popularidad de una película, dado su título.
- **Votación de película**: Devuelve el año de estreno y, si la película cumple con un mínimo de valoraciones, el promedio de estas valoraciones, dado el título de la película.
- **Información de actor**: Ofrece el número total de películas en las que ha participado un actor, así como el porcentaje de retorno de sus películas a lo largo de su carrera, dado su nombre.
- **Información de director**: Muestra el número y la lista de películas dirigidas por un director, junto con el porcentaje de retorno de cada una, dado el nombre del director.

La API ha sido desarrollada utilizando FastAPI y todas las funciones han sido implementadas en el archivo **main.py**. Se ha comprobado que las funciones operan correctamente en un entorno local y están disponibles para su verificación en la plataforma Render.

Se puede visualizar su funcionamiento en este [video demostrativo](https://drive.google.com/file/d/1fsT0HwtMSr8qcxzF9vK2cpa8inZpuNqZ/view?usp=sharing).

[Aquí](https://proyecto1-mlops-bmf7.onrender.com/docs) se puede encontrar la API desplegada.

## Análisis Exploratorio de los Datos (EDA)

En el archivo **EDA** de los Notebooks se detalla el proceso de análisis de los datos, ajustando y preparando la información para su correcta utilización en el sistema de recomendación. Aunque parte de la preparación de datos se realizó durante el proceso de ETL.(#extracción-carga-y-transformación-de-los-datos-etl), se llevó a cabo una limpieza y normalización adicional para asegurar que el archivo **.parquet** utilizado por las funciones sea preciso y adecuado. El análisis profundizó en la relevancia de los datos y su impacto en la producción del modelo de recomendación, empleando gráficos diversos para justificar la inclusión o exclusión de datos específicos. Finalmente, se generó un archivo abreviado con la información esencial para el correcto funcionamiento del sistema.
Durante el proceso de ETL, se realizó una evaluación preliminar del dataset, abordando valores nulos, duplicados y columnas innecesarias. El análisis exploratorio de datos (EDA) permitió realizar transformaciones adicionales, reducir el número de filas y manejar de manera detallada los valores nulos y duplicados. Se estandarizó el uso del alfabeto latino para asegurar consistencia en el dataset.

Se creó un dataset reducido para el sistema de recomendación, almacenado en formato Parquet para optimizar el almacenamiento y procesamiento de datos. Este proceso facilitó un análisis estadístico detallado, evaluando la distribución de las variables numéricas y sus correlaciones.

Se identificó una correlación positiva significativa entre el presupuesto y los ingresos. Además, se analizaron variables categóricas y su relación con ingresos y presupuesto, así como la variación temporal de estas variables.

Los resultados del análisis, que incluyen la incidencia del presupuesto en las ganancias y la relación entre películas con altas votaciones y mayores ingresos, proporcionan información valiosa para el desarrollo del sistema de recomendación y la mejora del proceso de visualización. Este análisis establece una base sólida para la implementación del sistema, permitiendo una visualización efectiva y el uso de patrones y correlaciones identificadas.



## Modelo de Recomendación
Al final del archivo **EDA**, se presenta un análisis detallado del proceso de preparación de datos para el modelo de recomendación. Se optó por utilizar TfidfVectorizer para la vectorización del texto debido a la inconsistencia en los datos numéricos, junto con la similitud del coseno para calcular la similitud entre películas.
La función de recomendación devuelve un conjunto de 5 películas relacionadas con el título proporcionado, ordenadas de acuerdo con su puntuación promedio, basada en las valoraciones encontradas en la base de datos en los elementos extraídos del título, género y descripción de la película.



## Conclusión

Este proyecto ha demostrado ser un desafío integral en la creación y despliegue de un sistema de recomendación de películas. Desde la limpieza y transformación de datos, pasando por el desarrollo de una API robusta con FastAPI, hasta la implementación de un modelo de recomendación basado en similitud textual, cada etapa ha contribuido a construir una solución efectiva y funcional.

La integración de la API con el modelo de recomendación permite a los usuarios acceder a información detallada sobre películas y obtener recomendaciones personalizadas basadas en sus preferencias. El uso del formato **.parquet** para el almacenamiento de datos optimiza tanto el rendimiento como el manejo de memoria, mientras que el análisis exploratorio de datos (EDA) proporciona una base sólida para entender y mejorar el sistema.

La implementación y pruebas realizadas localmente, así como su despliegue en plataformas como Render, aseguran que el sistema no solo cumple con los requerimientos del proyecto, sino que también está listo para un entorno de producción real. 

Como MVP (Producto Mínimo Viable), este proyecto ha logrado establecer una base sólida y funcional. Aunque se ha alcanzado un resultado positivo, con más experiencia y tiempo, existe un gran potencial para optimizar y mejorar significativamente el sistema. Esta solución proporciona una base robusta para futuros desarrollos y refinamientos, ofreciendo una plataforma eficiente y escalable para la recomendación de películas.

