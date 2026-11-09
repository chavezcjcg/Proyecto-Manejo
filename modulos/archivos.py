import os
from modulos.configuracion import (
    ARCHIVO_DATOS, LONG_ID, LONG_NOMBRE, LONG_TELEFONO,
    LONG_CORREO, LONG_CIUDAD, TAMANIO_REGISTRO
)
from modulos.indice import cargar_indice, guardar_indice
from modulos.seguridad import guardar_hash_seguridad


def empaquetar(codigo, nombre, telefono, correo, ciudad):
    c_id = str(codigo).ljust(LONG_ID)
    c_id = c_id[:LONG_ID]

    c_nom = str(nombre).ljust(LONG_NOMBRE)
    c_nom = c_nom[:LONG_NOMBRE]

    c_tel = str(telefono).ljust(LONG_TELEFONO)
    c_tel = c_tel[:LONG_TELEFONO]

    c_cor = str(correo).ljust(LONG_CORREO)
    c_cor = c_cor[:LONG_CORREO]

    c_ciu = str(ciudad).ljust(LONG_CIUDAD)
    c_ciu = c_ciu[:LONG_CIUDAD]

    registro = f"{c_id}{c_nom}{c_tel}{c_cor}{c_ciu}\n"
    return registro


def desempaquetar(linea):
    if len(linea) < TAMANIO_REGISTRO:
        return None

    pos = 0

    texto_codigo = linea[pos : pos + LONG_ID]
    codigo = int(texto_codigo.strip())
    pos = pos + LONG_ID

    texto_nombre = linea[pos : pos + LONG_NOMBRE]
    nombre = texto_nombre.strip()
    pos = pos + LONG_NOMBRE

    texto_telefono = linea[pos : pos + LONG_TELEFONO]
    telefono = texto_telefono.strip()
    pos = pos + LONG_TELEFONO

    texto_correo = linea[pos : pos + LONG_CORREO]
    correo = texto_correo.strip()
    pos = pos + LONG_CORREO

    texto_ciudad = linea[pos : pos + LONG_CIUDAD]
    ciudad = texto_ciudad.strip()

    contacto = {
        "id": codigo,
        "nombre": nombre,
        "telefono": telefono,
        "correo": correo,
        "ciudad": ciudad
    }
    return contacto


def inicializar_archivos():
    if not os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "w", encoding="utf-8", newline="\n") as archivo:
            pass

    indice = cargar_indice()
    guardar_indice(indice)
    guardar_hash_seguridad()


def guardar_contacto(codigo, nombre, telefono, correo, ciudad):
    indice = cargar_indice()
    if codigo in indice:
        raise ValueError(f"El código {codigo} ya existe en el índice.")

    registro = empaquetar(codigo, nombre, telefono, correo, ciudad)

    with open(ARCHIVO_DATOS, "a", encoding="utf-8", newline="\n") as archivo:
        posicion = archivo.tell()
        print("Posicion inicial:", posicion)
        archivo.write(registro)
        print("Posicion final:", archivo.tell())

    indice[codigo] = posicion
    guardar_indice(indice)
    guardar_hash_seguridad()
    return posicion


def buscar_contacto(codigo_buscado):
    indice = cargar_indice()
    if codigo_buscado not in indice:
        print(f"No se encontró ningún contacto con el código {codigo_buscado}.")
        return None, None

    posicion = indice[codigo_buscado]
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8", newline="\n") as archivo:
            print("Posicion inicial:", archivo.tell())
            archivo.seek(posicion)
            print("Posicion final:", archivo.tell())

            linea = archivo.readline()
            contacto = desempaquetar(linea)
            if contacto is not None:
                print(f"Contacto encontrado en la posición {posicion}: {contacto}")
                return contacto, posicion
    except FileNotFoundError:
        print("El archivo 'contactos.dat' no se encontró.")

    return None, None


def modificar_contacto(codigo_buscado, nuevo_nombre, nuevo_telefono, nuevo_correo, nueva_ciudad):
    indice = cargar_indice()
    if codigo_buscado not in indice:
        raise KeyError(f"No se encontró ningún contacto con el código {codigo_buscado}.")

    posicion = indice[codigo_buscado]
    registro_actualizado = empaquetar(codigo_buscado, nuevo_nombre, nuevo_telefono, nuevo_correo, nueva_ciudad)

    with open(ARCHIVO_DATOS, "r+", encoding="utf-8", newline="\n") as archivo:
        print("Posición inicial:", archivo.tell())
        archivo.seek(posicion)
        print("Posición de modificación in-place:", archivo.tell())
        archivo.write(registro_actualizado)

    guardar_hash_seguridad()
    print("Contacto modificado correctamente.")
    return posicion


def mostrar_todos():
    contactos = []
    if not os.path.exists(ARCHIVO_DATOS):
        return contactos

    with open(ARCHIVO_DATOS, "r", encoding="utf-8", newline="\n") as archivo:
        while True:
            linea = archivo.readline()
            if not linea:
                break
            contacto = desempaquetar(linea)
            if contacto is not None:
                contactos.append(contacto)
    return contactos