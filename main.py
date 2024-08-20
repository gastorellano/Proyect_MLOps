from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string 
from typing import List


app = FastAPI()
app.title = "Buscador de películas"
movies_credits = pd.read_csv('DATA/movies_credits.csv') #Se crea un DataFrame para las diferentes consultas.
recomendacion_df = pd.read_parquet('DATA/recomendacion.parquet')

vectorizacion = TfidfVectorizer(stop_words=None)#Se coloca None porque ha sido previamente depurado
matrizTFIDF = vectorizacion.fit_transform(recomendacion_df['descripcion_combinada'])

#Obtenemos la similitud del coseno
similitud_coseno = cosine_similarity(matrizTFIDF, matrizTFIDF) 

@app.get("/", tags=['Home'])
def read_root():
    return {"message": "Bienvenido a la API de películas. Aquí podrás obtener datos de filmaciones."}


# Recibe un mes escrito en español, y devuelve la cantidad de películas estrenadas durante ese mes, que se encuentren en todo el dataset
@app.get("/meses/{mes}", tags=['Buscar cantidad por mes'])
def cantidad_filmaciones_mes(mes: str): 
    """Esta función retorna las películas estrenadas en un mes determinado.
    Espera un argumento: el 'mes' de estreno, ingresado en español.
    Retorna la cantidad de filmaciones estrenadas durante ese mes, cualquier año, dentro de todo el dataset.
    """
    #Creo un diccionario de meses y sus números respectivos, que utilizaré en las funciones
    meses = {
    'enero': 1,
    'febrero': 2,
    'marzo': 3,
    'abril': 4,
    'mayo': 5,
    'junio': 6,
    'julio': 7,
    'agosto': 8,
    'septiembre': 9,
    'octubre': 10,
    'noviembre': 11,
    'diciembre': 12
}
    movies_credits['release_date']= pd.to_datetime(movies_credits['release_date'],format= '%Y-%m-%d')
    # Confirmo que la fecha se encuentre en formato datatime, para extraer el mes. 

    mes = mes.lower()     # La importancia de convertirlo a minúsculas es para que la búsqueda no arroje errores y haya coincidencia.
    
    if mes not in meses:
        raise HTTPException(status_code=400, detail=f"Mes ingresado '{mes}' no es válido. Por favor ingrese un mes en Español.")
    # Se establece el error en caso de no indicarse un mes correctamente y en español.
    
    numero_mes = meses[mes] # Obtengo el número del mes
    
    # Contar las películas estrenadas en el mes especificado, que hayan sido estrenadas
    lista_filmaciones = movies_credits[
        (movies_credits['release_date'].dt.month == numero_mes) #Busco los valores del número del mes
        & (movies_credits['status'] == 'Released') #La segunda condición es que el estado sea 'Released'
    ]
    
    cantidad_filmaciones = len(lista_filmaciones) #Guardo en una variable la cantidad de elementos 
    
    return {"mes": mes, "cantidad de peliculas": cantidad_filmaciones} 


# Definir la función recomendacion
def recomendacionPeliculas(title, df=recomendacion_df, similitud_coseno=similitud_coseno):
    try:
        indice = df[df['title'].str.lower() == title.lower()].index[0] # Se define el índice de película similar
        similitud = list(enumerate(similitud_coseno[indice])) 
        similitud = sorted(similitud, key=lambda x: x[1], reverse=True) #Se obtiene el score de similitud y se ordenan.
        # Se obtienen las películas similares, dejando afuera la primera(que es el mismo título):
        similitud = similitud[1:6]
        indices_similares = [i[0] for i in similitud]
        peliculas_similares = df['title'].iloc[indices_similares].tolist() #Se crea una lista con las películas
        mensaje = f"Se encontraron los siguientes títulos similares a '{title}':"
        print(mensaje)
        # Retornar la lista de títulos similares
        return peliculas_similares
    except IndexError:
        print(f"No se encontró la película '{title}'. Por favor, intente con otro título.")

@app.get("/recomendacion/{titulo}", response_model=List[str])
def recomendacion(titulo: str):
    """
    Devuelve un listado de cinco películas similares, orientadas según el titulo, genero y descripcion
    en todo el dataset.

    Recibe un único Parámetro:
    El título de la película a la que se desea obtener recomendaciones (str)."""

    peliculas_recomendadas = recomendacionPeliculas(titulo, recomendacion_df, similitud_coseno)
    return peliculas_recomendadas
