import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_DATOS = os.path.join(BASE_DIR, "datos")
CARPETA_RESPALDOS = os.path.join(BASE_DIR, "respaldos")

if not os.path.exists(CARPETA_DATOS):
    os.mkdir(CARPETA_DATOS)

if not os.path.exists(CARPETA_RESPALDOS):
    os.mkdir(CARPETA_RESPALDOS)

ARCHIVO_DATOS = os.path.join(CARPETA_DATOS, "contactos.dat")
ARCHIVO_INDICE = os.path.join(CARPETA_DATOS, "indice.json")
ARCHIVO_HASH = os.path.join(CARPETA_DATOS, "contactos.sha256")
ARCHIVO_JSON = os.path.join(CARPETA_DATOS, "contactos.json")
ARCHIVO_PDF = os.path.join(CARPETA_DATOS, "reporte.pdf")

# Longitudes fijas de cada campo
# 6 + 30 + 12 + 30 + 21 + 1 (\n) = 100 caracteres exactos
LONG_ID = 6
LONG_NOMBRE = 30
LONG_TELEFONO = 12
LONG_CORREO = 30
LONG_CIUDAD = 21
TAMANIO_REGISTRO = LONG_ID + LONG_NOMBRE + LONG_TELEFONO + LONG_CORREO + LONG_CIUDAD + 1