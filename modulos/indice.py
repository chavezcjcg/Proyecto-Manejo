import os
import json
from modulos.configuracion import ARCHIVO_INDICE


def cargar_indice():
    indice = {}
    if not os.path.exists(ARCHIVO_INDICE):
        return indice

    try:
        with open(ARCHIVO_INDICE, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            for clave in datos:
                codigo = int(clave)
                posicion = int(datos[clave])
                indice[codigo] = posicion
            return indice
    except FileNotFoundError:
        print("El archivo de índice no existe")
        return indice
    except json.JSONDecodeError:
        print("El archivo de índice no tiene formato válido")
        return indice


def guardar_indice(indice):
    with open(ARCHIVO_INDICE, "w", encoding="utf-8") as archivo:
        json.dump(indice, archivo, indent=4)