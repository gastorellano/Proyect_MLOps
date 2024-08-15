from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()

movies_credits = pd.read_csv('DATA/movies_credits.csv') #Se crea un DataFrame para las diferentes consultas.




## Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.
@app.get("/meses/{mes}")
def cantidad_filmaciones_mes(mes: str): 
    """Esta función retorna las películas estrenadas en un mes determinado.
    Espera un argumento: el 'mes' de estreno, ingresado en español.
    Retorna la cantidad de filmaciones estrenadas durante ese mes, cualquier año, dentro de todo el dataset.
    """
    #Mapeo de meses en español a numeros para utulizar funcion day of the week de pandas
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
    # Formatear la columna de release_date a formato datatime. 
    movies_credits['release_date']= pd.to_datetime(movies_credits['release_date'],format= '%Y-%m-%d')
    # Convertir el nombre del mes a minúsculas para asegurar coincidencia
    mes = mes.lower()
    
    # Verificar si el mes ingresado es válido, de lo contrario arroja error.
    if mes not in meses:
        raise HTTPException(status_code=400, detail=f"Mes ingresado '{mes}' no es válido. Por favor ingrese un mes en Español.")
    
    # Obtener el número del mes
    mes_numero = meses[mes]
    
    # Contar las películas estrenadas en el mes especificado, que hayan sido estrenadas
    lista_filmaciones = movies_credits[
        (movies_credits['release_date'].dt.month == mes_numero) 
    #    & (movies_credits['status'] == 'Released')
    ]
    
    cantidad_filmaciones = len(lista_filmaciones)
    
    return {"mes": mes, "cantidad de peliculas": cantidad_filmaciones} 
