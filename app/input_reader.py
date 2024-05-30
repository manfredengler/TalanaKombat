import json

def read_input(filename:str) -> dict:# -> Any    :
    """ Recibe nombre de archivo, intenta leer el archivo .json en la carpeta y luego parsearlo a dict"""
    path:str = f'./input/{filename}.json'
    with open(file=path, mode='r') as input_file:
        json_data: dict = json.load(input_file)
        return json_data
    