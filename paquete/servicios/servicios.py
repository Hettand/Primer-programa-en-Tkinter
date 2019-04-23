"""Añadir nuevos servicios, ver lista de servicios, botones de añadir seguro y ver 
lista de seguros"""
import sys
sys.path.insert(1,"../conexion")
import conexion
sys.path.insert(1,"../panel")
import funcionalidades

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pymysql
from belfrywidgets import ToolTip
import seguros




Conexion=conexion.Conexion
verSeguros=seguros.verSeguros
agregarSeguro=seguros.agregar
adaptable=funcionalidades.adaptable
posicionar=funcionalidades.posicionar


class Servicio(Conexion,tk.Frame):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
    




    def agregar(self):

        self.id = tk.StringVar()
        self.nombre = tk.StringVar()

        ventana=tk.Toplevel(self)
        ventana.resizable(0,0)
        ventana.transient(self)
        posicionar(ventana)

        frame_superior = tk.Frame(ventana,bg="black")
        frame_superior.grid(row=0,sticky="nsew")

        frame_medio = tk.Frame(ventana)
        frame_medio.grid(row=1)
        
        frame_inferior = tk.Frame(ventana,bg="#214472")
        frame_inferior.grid(row=2)

        label_img=tk.Label(
            frame_superior,
            image=self.taller,
            bg="black"
            )
        label_img.grid(row=0,column=0,padx=20)

        label_superior=tk.Label(
            frame_superior,
            text="Formulario Servicios",
            bg="black",
            fg="white",
            font=self.font
            )
        label_superior.grid(row=0,column=1,padx=30)


        idLabel = tk.Label(
            frame_medio,
            text="Id: "
            )
        idLabel.grid(row=1, column=0,sticky="e", padx=10,pady=10)


        nomLabel = tk.Label(
            frame_medio,
            text="Categoría: "
            )
        nomLabel.grid(row=2, column=0,sticky="e", padx=4,pady=10)

        id_entry = tk.Entry(
            frame_medio,
            width=10,
            textvariable=self.id
            )
        id_entry.grid(row=1, column=1, padx=10,pady=10,sticky="w")

        nom_entry = tk.Entry(
            frame_medio,
            width=40,
            textvariable=self.nombre
            )
        nom_entry.grid(row=2, column=1,padx=10,pady=10,sticky="w")

        #botones
        texto=("Limpiar","Buscar","Actualizar","Crear")
        funciones=(
            lambda:self.limpiar(),
            lambda:self.buscar(),
            lambda:self.actualizar(),
            lambda:self.crear()
            )
        n=0
        for t in texto:
            boton=ttk.Button(
                frame_inferior,
                text=texto[n],
                command=funciones[n]
                )
            boton.grid(row=0,pady=10,padx=10,column=n)
            n+=1

        
        

    def cargar(self):

        #cargar todos los servicios
        try:

            self.miCursor = self.miBase.cursor()
            self.miCursor.execute("SELECT * FROM servicios")
            resultado = self.miCursor.fetchall()

            if resultado:

                ventana_s=tk.Toplevel(self)
                ventana_s.resizable(0,0)
                ventana_s.transient(self)
                posicionar(ventana_s)

                frames1=tk.Frame(
                    ventana_s,
                    bg="black"
                    )
                frames1.grid(sticky="ew",row=0)

                label_imagen=tk.Label(
                    frames1,
                    bg="black",
                    image=self.taller
                    )
                label_imagen.grid(row=0,column=0,sticky="e",padx=20)

                label_titulo=tk.Label(
                    frames1,
                    bg="black",
                    fg="white",
                    text="Servicios registrados",
                    font=self.font
                    )
                label_titulo.grid(row=0,column=1,padx=60)


                frame_s2 = tk.Frame(ventana_s)
                frame_s2.grid(row=1,column=0)

                campos=tk.Frame(frame_s2)
                campos.grid(row=0,column=0)


                frameScroll=tk.Frame(ventana_s)
                frameScroll.grid(row=1,column=2,sticky="e")

                scroll = tk.Scrollbar(frameScroll)#comienzo del  scroll
                
                c=tk.Canvas(
                    frame_s2,
                    yscrollcommand=scroll.set
                    )

                scroll.config(command=c.yview)
                scroll.grid(
                    sticky="e",
                    column=0,
                    row=1,
                    ipady=120
                    )
                
                contenedor = tk.Frame(c)
                contenedor.grid(row=2)

                c.create_window(
                    0,0,
                    window=contenedor,
                    anchor="nw"
                    )
                c.grid(sticky="nsew")


                ide = tk.Label(
                    campos,
                    text="Id",
                    borderwidth=2,
                    relief="groove",
                    width=20,
                    background="#5a98c4",
                    fg="white"
                    )
                ide.grid(row=0, column=0,sticky="w",ipady=5)
                cat = tk.Label(
                    campos,
                    text="Categoría",
                    borderwidth=2,
                    relief="groove",
                    width=35,
                    background="#5a98c4",
                    fg="white"
                    )
                cat.grid(row=0, column=1,sticky="w",ipady=5)

                listado = {}
                row=1
                for ide,nom in resultado:
                
                    listado[ide] ={
                    "Id": tk.Label(
                        contenedor,
                        text=ide,
                        borderwidth=2,
                        relief="groove",
                        width=20
                        ),
                    "Categoría": tk.Label(
                        contenedor,
                        text=nom,
                        borderwidth=2,
                        relief="groove",
                        width=35
                        )
                    }
                    listado[ide]["Id"].grid(row=row, column=0,ipady=5) 
                    listado[ide]["Categoría"].grid(row=row, column=1,ipady=5)
                    row+=1

                    linea= tk.Frame(frame_s2)
                    linea.grid(
                        sticky="nse",
                        column=3,
                        row=1
                        )

                    frame_s2.update()
                    c.config(scrollregion=c.bbox("all"))#fin del scroll
        except:
            messagebox.showinfo("Atencion","Datos no encontrados")

        finally:


            self.miCursor.close()


    def limpiar(self):

        #limpiar formulario

        self.id.set("")
        self.nombre.set("")


    def crear(self):

        # crear servicio

        try:
            
            self.miCursor = self.miBase.cursor()
            consulta= "INSERT INTO servicios (id_servicio,nombre) values(null,%s)"
            self.miCursor.execute(consulta, self.nombre.get())

            messagebox.showinfo("Nuevo servicio","{}".format(self.nombre.get()))

            self.limpiar()

        except pymysql.err.DataError:
            messagebox.showerror("Error","Datos incorrectos")

        except pymysql.err.InternalError:
            messagebox.showerror("Error","Datos incorrectos")
            
        except pymysql.err.IntegrityError:
            messagebox.showerror(
                "Error", 
                "Intenta ingresar un servicio ya existente\nVerifique"
                )

        finally:
            self.miBase.commit()
            self.miCursor.close()
            


    def buscar(self):

        # buscar servicio en el formulario

        try:
            
            self.miCursor = self.miBase.cursor()
            

            if self.id.get():
                
                self.miCursor.execute(
                    "SELECT * FROM servicios where id_servicio = %s;",
                    self.id.get()
                    )
                consulta = self.miCursor.fetchone()
                self.ver_uno(consulta)

            elif self.nombre.get():

                self.miCursor.execute(
                    "SELECT * FROM servicios where nombre = %s;",
                    self.nombre.get()
                    )
                resultado = self.miCursor.fetchone()

                self.id.set(resultado[0])
                self.nombre.set(resultado[1])
        
        except pymysql.err.DataError:
            self.limpiar()
            messagebox.showerror("Error", "Datos incorrectos")
            

        except TypeError:
            self.limpiar()
            messagebox.showinfo("Atencion", "Servicio no encontrado")
       

        finally:
            
            self.miBase.commit()
            self.miCursor.close()


    def ver_uno(self,consulta):

        self.id.set(consulta[0])
        self.nombre.set(consulta[1])






    def actualizar(self):

        # actualizar servicio

        try:
            
            self.miCursor = self.miBase.cursor()
            
            buscado=self.miCursor.execute(
                "SELECT * FROM servicios where id_servicio = %s",
                self.id.get()
                )
            encontrado=self.miCursor.fetchone()

            
            if encontrado:
                consulta = "UPDATE servicios set nombre=(%s) where id_servicio=(%s)"
                self.miCursor.execute(
                    consulta,
                    (self.nombre.get(),self.id.get()
                        )
                    )

                messagebox.showinfo(
                    "Información", 
                    "Servicio \nNº {}\nActualizado con éxito".format(
                        self.id.get()
                        )
                    )
                self.limpiar()
            else:
                messagebox.showinfo("Atencion","Ingrese un registro válido")

        finally:

            self.miBase.commit()
            self.miCursor.close()


    def cargarSeguros(self):

        try:

            self.miCursor = self.miBase.cursor()
            self.miCursor.execute("SELECT * FROM seguros")
            resultado = self.miCursor.fetchall()

            if resultado:

                ventanaSeguros=tk.Toplevel(self)
                ventanaSeguros.resizable(0,0)
                ventanaSeguros.transient(self)
                posicionar(ventanaSeguros)
               

                verSeguros(resultado,ventanaSeguros,self.taller)

            else:

                messagebox.showinfo("Atencion", "Registro de seguros no encontrados")



        finally:

            self.miBase.commit()
            self.miCursor.close()




       