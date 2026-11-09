import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from modulos.configuracion import TAMANIO_REGISTRO
from modulos.archivos import (
    inicializar_archivos, guardar_contacto,
    buscar_contacto, modificar_contacto
)
from modulos.seguridad import (
    verificar_integridad, crear_respaldo,
    obtener_informacion_archivo
)
from modulos.exportacion import exportar_json, generar_pdf


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agenda de Contactos - Registros de Tamaño Fijo")
        self.geometry("700x480")
        self.resizable(False, False)

        inicializar_archivos()
        self.crear_menu()
        self.crear_pantalla()
        self.verificar_integridad_inicio()

    def verificar_integridad_inicio(self):
        valido, detalle = verificar_integridad()
        if valido == False:
            messagebox.showwarning("Alerta de Integridad", detalle)

    def mostrar_acerca_de(self):
        mensaje = "Agenda con registros de tamaño fijo.\nAcceso directo con seek() y tell()."
        messagebox.showinfo("Ayuda", mensaje)

    def crear_menu(self):
        barra_menu = tk.Menu(self)

        # Menú Contactos
        menu_contactos = tk.Menu(barra_menu, tearoff=0)
        menu_contactos.add_command(label="Agregar", command=self.opc_agregar)
        menu_contactos.add_command(label="Buscar por ID", command=self.opc_buscar)
        menu_contactos.add_command(label="Modificar", command=self.opc_modificar)
        menu_contactos.add_separator()
        menu_contactos.add_command(label="Salir", command=self.destroy)
        barra_menu.add_cascade(label="Contactos", menu=menu_contactos)

        # Menú Exportar
        menu_exportar = tk.Menu(barra_menu, tearoff=0)
        menu_exportar.add_command(label="Exportar a JSON", command=self.opc_exportar_json)
        menu_exportar.add_command(label="Generar reporte PDF", command=self.opc_generar_pdf)
        barra_menu.add_cascade(label="Exportar", menu=menu_exportar)

        # Menú Herramientas
        menu_herramientas = tk.Menu(barra_menu, tearoff=0)
        menu_herramientas.add_command(label="Verificar integridad", command=self.opc_verificar_integridad)
        menu_herramientas.add_command(label="Crear respaldo ZIP", command=self.opc_crear_respaldo)
        menu_herramientas.add_command(label="Información del archivo", command=self.opc_info_archivo)
        barra_menu.add_cascade(label="Herramientas", menu=menu_herramientas)

        # Menú Ayuda
        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.config(menu=barra_menu)

    def crear_pantalla(self):
        panel = ttk.LabelFrame(self, text=" Registro de Operaciones y Archivo ", padding=10)
        panel.pack(fill="both", expand=True, padx=12, pady=12)

        self.consola = tk.Text(panel, wrap="word", font=("Courier", 10))
        self.consola.pack(fill="both", expand=True)

        self.imprimir_log("Programa iniciado.")
        self.imprimir_log(f"Tamaño fijo configurado por registro: {TAMANIO_REGISTRO} bytes.\n")

    def imprimir_log(self, mensaje):
        self.consola.insert("end", f"> {mensaje}\n")
        self.consola.see("end")

    def opc_agregar(self):
        try:
            val_id = simpledialog.askstring("Agregar Contacto", "Código ID (número entero):")
            if val_id is None:
                return
            codigo = int(val_id.strip())

            nombre = simpledialog.askstring("Agregar Contacto", "Nombre:")
            if nombre is None:
                nombre = ""

            telefono = simpledialog.askstring("Agregar Contacto", "Teléfono:")
            if telefono is None:
                telefono = ""

            correo = simpledialog.askstring("Agregar Contacto", "Correo:")
            if correo is None:
                correo = ""

            ciudad = simpledialog.askstring("Agregar Contacto", "Ciudad:")
            if ciudad is None:
                ciudad = ""

            posicion = guardar_contacto(codigo, nombre, telefono, correo, ciudad)
            msg = f"Contacto guardado en la posición {posicion} del archivo."
            self.imprimir_log(msg)
            messagebox.showinfo("Éxito", msg)
        except ValueError as err:
            messagebox.showerror("Error", str(err))

    def opc_buscar(self):
        val_id = simpledialog.askstring("Buscar Contacto", "Ingrese código ID a buscar:")
        if val_id is None:
            return
        try:
            codigo = int(val_id.strip())
            contacto, posicion = buscar_contacto(codigo)
            if contacto is None:
                self.imprimir_log(f"No se encontró ningún contacto con el código {codigo}.")
                messagebox.showwarning("No encontrado", f"El código {codigo} no existe.")
                return

            res = f"Contacto encontrado en la posición {posicion}:\n"
            res = res + f"  Código: {contacto['id']}\n"
            res = res + f"  Nombre: {contacto['nombre']}\n"
            res = res + f"  Teléfono: {contacto['telefono']}\n"
            res = res + f"  Correo: {contacto['correo']}\n"
            res = res + f"  Ciudad: {contacto['ciudad']}"

            self.imprimir_log(res)
            messagebox.showinfo("Resultado", res)
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un número entero válido.")

    def opc_modificar(self):
        val_id = simpledialog.askstring("Modificar Contacto", "Código ID del contacto:")
        if val_id is None:
            return
        try:
            codigo = int(val_id.strip())
            contacto, posicion_actual = buscar_contacto(codigo)
            if contacto is None:
                messagebox.showwarning("No encontrado", f"El código {codigo} no existe.")
                return

            nuevo_nom = simpledialog.askstring("Modificar", "Nombre:", initialvalue=contacto['nombre'])
            if nuevo_nom is None:
                nuevo_nom = contacto['nombre']

            nuevo_tel = simpledialog.askstring("Modificar", "Teléfono:", initialvalue=contacto['telefono'])
            if nuevo_tel is None:
                nuevo_tel = contacto['telefono']

            nuevo_cor = simpledialog.askstring("Modificar", "Correo:", initialvalue=contacto['correo'])
            if nuevo_cor is None:
                nuevo_cor = contacto['correo']

            nueva_ciu = simpledialog.askstring("Modificar", "Ciudad:", initialvalue=contacto['ciudad'])
            if nueva_ciu is None:
                nueva_ciu = contacto['ciudad']

            posicion = modificar_contacto(codigo, nuevo_nom, nuevo_tel, nuevo_cor, nueva_ciu)
            msg = f"Contacto con código {codigo} sobrescrito en la posición {posicion}."
            self.imprimir_log(msg)
            messagebox.showinfo("Éxito", msg)
        except (ValueError, KeyError) as err:
            messagebox.showerror("Error", str(err))

    def opc_exportar_json(self):
        cant, ruta = exportar_json()
        msg = f"Se exportaron {cant} contactos a '{ruta}'."
        self.imprimir_log(msg)
        messagebox.showinfo("Exportar JSON", msg)

    def opc_generar_pdf(self):
        try:
            ruta = generar_pdf()
            msg = f"Reporte PDF generado correctamente en '{ruta}'."
            self.imprimir_log(msg)
            messagebox.showinfo("Reporte PDF", msg)
        except Exception as err:
            messagebox.showerror("Error PDF", str(err))

    def opc_verificar_integridad(self):
        valido, detalle = verificar_integridad()
        self.imprimir_log(f"Integridad: {detalle}")
        if valido == True:
            messagebox.showinfo("Integridad Verificada", detalle)
        else:
            messagebox.showwarning("Alerta de Modificación", detalle)

    def opc_crear_respaldo(self):
        nom_zip, orig, comp = crear_respaldo()
        msg = f"Respaldo creado: {nom_zip}\nTamaño original: {orig} bytes\nTamaño comprimido: {comp} bytes"
        self.imprimir_log(msg)
        messagebox.showinfo("Respaldo Creado", msg)

    def opc_info_archivo(self):
        info = obtener_informacion_archivo()
        self.imprimir_log("Consulta de metadatos realizada.")
        messagebox.showinfo("Información del Archivo", info)