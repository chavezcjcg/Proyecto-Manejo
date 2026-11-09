import os
import zipfile
import hashlib
from datetime import datetime
from modulos.configuracion import (
    ARCHIVO_DATOS, ARCHIVO_INDICE, ARCHIVO_HASH,
    CARPETA_RESPALDOS, TAMANIO_REGISTRO
)


def calcular_hash(ruta):
    sha256 = hashlib.sha256()
    with open(ruta, "rb") as archivo:
        while True:
            bloque = archivo.read(4096)
            if not bloque:
                break
            sha256.update(bloque)
    return sha256.hexdigest()


def guardar_hash_seguridad():
    if os.path.exists(ARCHIVO_DATOS):
        hash_archivo = calcular_hash(ARCHIVO_DATOS)
        with open(ARCHIVO_HASH, "w", encoding="utf-8") as archivo:
            archivo.write(hash_archivo)


def verificar_integridad():
    if not os.path.exists(ARCHIVO_HASH):
        guardar_hash_seguridad()
        return True, "No existía hash previo. Se ha generado uno nuevo."

    if not os.path.exists(ARCHIVO_DATOS):
        guardar_hash_seguridad()
        return True, "No existía archivo de datos previo."

    with open(ARCHIVO_HASH, "r", encoding="utf-8") as archivo:
        hash_original = archivo.read().strip()

    hash_actual = calcular_hash(ARCHIVO_DATOS)

    print("Hash original:", hash_original)
    print("Hash actual:  ", hash_actual)

    if hash_original == hash_actual:
        print("El archivo no ha sido modificado")
        return True, "Los archivos son idénticos"
    else:
        print("El archivo ha sido modificado")
        return False, "Los archivos son distintos"


def crear_respaldo():
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo_zip = f"respaldo_{fecha}.zip"
    ruta_zip = os.path.join(CARPETA_RESPALDOS, nombre_archivo_zip)

    with zipfile.ZipFile(ruta_zip, "w", compression=zipfile.ZIP_DEFLATED) as zip_archivo:
        if os.path.exists(ARCHIVO_DATOS):
            zip_archivo.write(ARCHIVO_DATOS, arcname="contactos.dat")
        if os.path.exists(ARCHIVO_INDICE):
            zip_archivo.write(ARCHIVO_INDICE, arcname="indice.json")

    tam_original = 0
    if os.path.exists(ARCHIVO_DATOS):
        tam_original = tam_original + os.path.getsize(ARCHIVO_DATOS)

    if os.path.exists(ARCHIVO_INDICE):
        tam_original = tam_original + os.path.getsize(ARCHIVO_INDICE)

    tam_comprimido = os.path.getsize(ruta_zip)

    print("Respaldo ZIP creado correctamente.")
    print("Tamaño original:", tam_original, "bytes")
    print("Tamaño comprimido:", tam_comprimido, "bytes")
    return ruta_zip, tam_original, tam_comprimido


def obtener_informacion_archivo():
    if not os.path.exists(ARCHIVO_DATOS):
        return "El archivo de contactos todavía no existe."

    estado = os.stat(ARCHIVO_DATOS)
    fecha_mod = datetime.fromtimestamp(estado.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    tam_total = estado.st_size
    cantidad_registros = tam_total // TAMANIO_REGISTRO

    permiso_lectura = os.access(ARCHIVO_DATOS, os.R_OK)
    if permiso_lectura == True:
        texto_lectura = "Concedido"
    else:
        texto_lectura = "Denegado"

    permiso_escritura = os.access(ARCHIVO_DATOS, os.W_OK)
    if permiso_escritura == True:
        texto_escritura = "Concedido"
    else:
        texto_escritura = "Denegado"

    info = ""
    info = info + "Archivo: " + str(ARCHIVO_DATOS) + "\n"
    info = info + "Tamaño total: " + str(tam_total) + " bytes\n"
    info = info + "Tamaño de cada registro: " + str(TAMANIO_REGISTRO) + " bytes\n"
    info = info + "Cantidad de registros: " + str(cantidad_registros) + "\n"
    info = info + "Última modificación: " + str(fecha_mod) + "\n"
    info = info + "Permiso de lectura: " + texto_lectura + "\n"
    info = info + "Permiso de escritura: " + texto_escritura

    print(info)
    return info