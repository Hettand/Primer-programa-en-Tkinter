from tkinter import messagebox
import pymysql
import smtplib
import tkinter as tk
import sys
sys.path.insert(1,"../panel")
import funcionalidades
from screeninfo import get_monitors



class Conexion():

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # ------------ Fuentes, imágenes, colores -------------------------------

        self.font=("verdana",12)
        self.bold=("verdana",12,"bold")
        
        self.masculino=tk.PhotoImage(file="../img/masculino.png")
        self.femenino=tk.PhotoImage(file="../img/femenina.png")
        self.none=tk.PhotoImage(file="../img/none.png")

        self.taller2=tk.PhotoImage(file="../img/taller2.png")
        self.taller=tk.PhotoImage(file="../img/taller.png")
        self.filtro = tk.PhotoImage(file="../img/filtro.png")
        
        self.imgClientes=tk.PhotoImage(file="../img/clientes.png")
        self.formClientes=tk.PhotoImage(file="../img/formClientes.png")
        self.agregaVehiculo=tk.PhotoImage(file="../img/agregaVehiculo.png")
        self.fichaCliente=tk.PhotoImage(file="../img/fichaCliente.png")
        self.filtro=tk.PhotoImage(file="../img/filtro.png")
        self.item=tk.PhotoImage(file="../img/item.png")
        self.editar=tk.PhotoImage(file="../img/editar.png")
        
        self.editartrabajo=tk.PhotoImage(file="../img/editartrabajo.png")
        self.imagen_t=tk.PhotoImage(file="../img/agregaTrabajo.png")

        self.verServicios=tk.PhotoImage(file="../img/verServicios.png")
        self.verSegurosImg=tk.PhotoImage(file="../img/verSeguros.png")
        self.service=tk.PhotoImage(file="../img/formServicios.png")
        self.seguro=tk.PhotoImage(file="../img/formSeguros.png")

        self.categorias=tk.PhotoImage(file="../img/categorias.png")
        self.existencias=tk.PhotoImage(file="../img/existencias.png")
        self.movi=tk.PhotoImage(file="../img/movi.png")

        self.lupa=tk.PhotoImage(file="../img/lupa.png")
        self.escoba=tk.PhotoImage(file="../img/escoba.png")
        self.actualiza=tk.PhotoImage(file="../img/actualizar.png")
        self.mas=tk.PhotoImage(file="../img/mas.png")
        self.maschico=tk.PhotoImage(file="../img/maschico.png")
        self.romper=tk.PhotoImage(file="../img/romper.png")


        self.gestionCat=tk.PhotoImage(file="../img/gestionCat.png")
        self.gestionMed=tk.PhotoImage(file="../img/gestionMed.png")
        self.gestionProv=tk.PhotoImage(file="../img/gestionProv.png")

        self.limites=tk.PhotoImage(file="../img/limites.png")
        self.cargarArticulo=tk.PhotoImage(file="../img/editarLimites.png")

        self.ingresos=tk.PhotoImage(file="../img/ingresos.png")
        self.egresos=tk.PhotoImage(file="../img/egresos.png")


        
        self.elUsuario="Paola"

        self.empresa = "labase"

        self.lista=[] # acá estarán los frameDinamico del programa

        self.imagenes=(#para los botones de los formularios
            self.escoba,
            self.actualiza,
            self.mas
            )
        self.texto=(" Limpiar"," Actualizar"," Crear")

        
        
        try :
            self.miBase = pymysql.connect(
                host="localhost",
                database= self.empresa,
                user="root",
                password=""
                )

            self.miBase2 = pymysql.connect(
                host="localhost",
                database="taller",
                user="root",
                password=""
                )

        except:
            messagebox.showinfo("Información", "Verifique su conexión") 
        