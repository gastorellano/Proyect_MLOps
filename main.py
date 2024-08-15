from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()
app.title = "Buscador de películas"
movies_credits = pd.read_csv('DATA/movies_credits.csv') #Se crea un DataFrame para las diferentes consultas.


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
