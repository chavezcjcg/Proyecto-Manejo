import os
import json
from datetime import datetime
from reportlab.pdfgen import canvas
from modulos.configuracion import ARCHIVO_JSON, ARCHIVO_PDF
from modulos.archivos import mostrar_todos


def exportar_json(ruta=ARCHIVO_JSON):
    contactos = mostrar_todos()
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(contactos, archivo, indent=4, ensure_ascii=False)

    print("Exportación JSON realizada correctamente en:", ruta)
    cantidad = len(contactos)
    return cantidad, ruta


def generar_pdf(ruta_json=ARCHIVO_JSON, ruta_pdf=ARCHIVO_PDF):
    if not os.path.exists(ruta_json):
        exportar_json(ruta_json)

    with open(ruta_json, "r", encoding="utf-8") as archivo:
        contactos = json.load(archivo)

    pdf = canvas.Canvas(ruta_pdf)
    pdf.drawString(100, 750, "LISTADO DE CONTACTOS")

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.drawString(100, 730, f"Fecha de generación: {fecha}")
    pdf.drawString(100, 720, "------------------------------------------------------------")

    y = 690

    for contacto in contactos:
        codigo = contacto["id"]
        nombre = contacto["nombre"]
        telefono = contacto["telefono"]
        correo = contacto["correo"]
        ciudad = contacto["ciudad"]

        texto = f"{codigo} | {nombre} | {telefono} | {correo} | {ciudad}"
        pdf.drawString(60, y, texto)
        y = y - 20

        if y < 60:
            pdf.showPage()
            y = 750

    pdf.save()
    print("Documento generado")
    return ruta_pdf