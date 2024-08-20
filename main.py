from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string 
from typing import List


app = FastAPI()
app.title = "Buscador de películas"
movies_credits = pd.read_parquet('DATA/movies_credits.parquet') #Se crea un DataFrame para las diferentes consultas.
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



# En el segundo endpoint se ingresa un día en idioma Español. Devuelve la cantidad de películas que fueron estrenadas en día consultado en la totalidad del dataset.

@app.get("/dias/{dia}")
def cantidad_filmaciones_dia(dia: str):
    """
    Devuelve la cantidad de películas estrenadas en un día específico, con estado 'released'.
    Parameteros:
    dia (str): El día de la semana en español (lunes, martes, miércoles, jueves, viernes, sábado, domingo).

    Retorna una cadena con la cantidad de películas estrenadas ese dia de la semana
    """
    # Mapeamos los días de la semana a números de día de la semana
    dias = {
        'lunes': 0,
        'martes': 1,
        'miércoles': 2,
        'miercoles':2,
        'jueves': 3,
        'viernes': 4,
        'sábado': 5,
        'sabado':5,
        'domingo': 6
    }
 
    movies_credits['release_date'] = pd.to_datetime(movies_credits['release_date'], errors='coerce') # Convertir la columna de fechas a datetime
    
    
    numero_dia = dias.get(dia.lower())# Obtenemos el numero de día, en minúscula
    
    if numero_dia is None:
        raise ValueError("Día inválido")
    
    # Filtrar las filas donde el día de la semana coincide con el día especificado y el estado es 'released'
    peliculas = movies_credits[(movies_credits['release_date'].dt.dayofweek == numero_dia) #Busco los valores del día
                 & (movies_credits['status'] == 'Released') #La segunda condición es que el estado sea 'Released'
                 ]
    cantidad = len(peliculas) #Se obtiene la cantidad
    return f"{cantidad} películas fueron estrenadas en los días {dia}."


#En el tercer endopoint, se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.
@app.get("/titulo/{titulo}")
def score_titulo(titulo: str):
    """
    Esta función espera el título de una película, y devuelve el título, el año de estreno y el score de una película específica en un str.
    """
    pelicula = movies_credits[movies_credits['title'].str.lower() == titulo.lower()] #Buscamos los valores en los que aparece el título
    if pelicula.empty:
            raise HTTPException(status_code=404, detail=f"Película '{titulo}' no encontrada.") #Si no aparece, devuelve el siguiente error.
        
    titulo = pelicula['title'].values[0]
    año = int(pelicula['release_year'].values[0])
    score = pelicula['vote_average'].values[0]
    
    return f"La película {titulo} fue estrenada en el año {año} con un score/popularidad de {score}."



# El siguiente endpoint recibe el título de una filmación esperando como respuesta el título, la cantidad de votos 
# y el valor promedio de las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, caso contrario, debemos contar
# con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.

@app.get("/votos/{titulo}")
def votos_titulo(titulo: str):
    """Se espera un parámetro: el título del film. Retorna el título, año de estreno, la cantidad de valoraciones y el valor promedio
    de los votos.
    Deberá de contar con al menos 2000 valoraciones, caso contrario, arrojara error. 
    """

    pelicula = movies_credits[movies_credits['title'].str.lower() == titulo.lower()]
    if pelicula.empty:
            raise HTTPException(status_code=404, detail=f"La película '{titulo}' no fue encontrada.")
    titulo = pelicula['title'].values[0]
    votos= int(pelicula['vote_count'].values[0])
    promedio = pelicula['vote_average'].values[0]
    año = int(pelicula['release_year'].values[0])
    if votos < 2000:
            raise HTTPException(status_code=404, detail=f"La película '{titulo}' tiene menos de 2000 valoraciones, por lo que no se devuelve ningún valor.")
    return f"La película {titulo} fue estrenada en el año {año}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio}."


#En este endpoint se debe ingresar el nombre de un actor que se encuentre dentro de un dataset, y devuelve
# el éxito del mismo medido a través del retorno. Además, la cantidad de películas que en las que ha 
# participado y el promedio de retorno. La definición no deberá considerar directores.
@app.get("/nombre_actor/{nombre_actor}") 
def get_actor(nombre_actor: str):
    """
    Se espera un parámetro: el nombre del actor (str). Devuelve el retorno del actor, cantidad de películas 
    en las que ha participado y el promedio de retorno.
    No se contemplan las películas en las que el actor también tiene el rol de director.
    """
    movies_credits['actor'] = movies_credits['actor'].str.lower().fillna('sin datos')
    movies_credits['director'] = movies_credits['director'].str.lower().fillna('sin datos')
    nombre_actor = nombre_actor.lower()
    # Convertimos a minúsculas. Además, colocamos 'sin datos' en los nulos.
       
    # Vamos a crear la variable actor_movies
    actor_movies = movies_credits[movies_credits.apply(lambda row: nombre_actor in row['actor'].split(', ') and nombre_actor not in row['director'].split(', '), axis=1)]
    #Se obtienen las películas en rol de actor, excluyendo aquellas donde también sea director
    if actor_movies.empty:
        raise HTTPException(status_code=404, detail="No se ha encontrado el actor")
    
    # Exito del actor, medido a través del retorno:
    retorno = actor_movies['return'].sum()
    cant_peliculas = actor_movies['id'].nunique()
    promedio_de_retorno = actor_movies['return'].mean()
    
    
    retorno = float(retorno)
    promedio_de_retorno = float(promedio_de_retorno)
    
    return f"El actor `{nombre_actor.title()}` ha participado de `{cant_peliculas}` filmaciones, el mismo ha conseguido un retorno de `{retorno:.2f}` con un promedio de `{promedio_de_retorno:.2f}` por filmación*"


#Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del 
# mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de 
# lanzamiento, retorno individual, costo y ganancia de la misma.

@app.get("/nombre_director/{nombre_director}")
def get_director(director: str):
    """
    Esta función recibe el nombre del Director (str), y devuelve las películas con fecha de estreno,
    el retorno individual, costo y ganancia (que será la recaudación menos el presupuesto)
    """
    director = director.lower()
    director_movies = movies_credits[movies_credits['director'].str.lower() == director]
    
    if director_movies.empty:
        raise HTTPException(status_code=404, detail=f"Director '{director}' no encontrado.")
    
    # El retorno individual será el promedio de retorno
    retorno = director_movies['return'].mean()
    movies_detalles = []
    for index, row in director_movies.iterrows():
        movie_details = {
            'titulo': row['title'],
            'retorno': row['return'],
            'costo': row['budget'],
            'ganancia': row['revenue'] - row['budget']
        }
        movies_detalles.append(movie_details)
    
    cadena = {
        'director_name': director.title(),  
        'total_return': retorno,
        'movies_details': movies_detalles
    }
    return cadena

# Definir la función recomendacion, para obtener la similitud del conseno y recomendar una lista de 5 películas similares.
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
    dentro de las 6000 películas más populares.

    Recibe un único Parámetro:
    El título de la película a la que se desea obtener recomendaciones (str)."""

    peliculas_recomendadas = recomendacionPeliculas(titulo, recomendacion_df, similitud_coseno)
    return peliculas_recomendadas
