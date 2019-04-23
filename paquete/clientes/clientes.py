import sys
sys.path.insert(1,"../conexion")
import conexion
sys.path.insert(1,"../panel")
import funcionalidades
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import pymysql
import vehiculo_cliente
import formulario_cliente
from belfrywidgets import ToolTip
import smtplib
import ficha



Conexion=conexion.Conexion
Vehiculos=vehiculo_cliente.Vehiculos
adaptable=funcionalidades.adaptable
siHayFrame=funcionalidades.siHayFrame
agregaFrame=funcionalidades.agregaFrame
cerrarFrame=funcionalidades.cerrarFrame
verDiaMesAnio=funcionalidades.verDiaMesAnio
FormularioCliente=formulario_cliente.FormularioCliente
desactivar=funcionalidades.desactivar
activar=funcionalidades.activar
posicionar=funcionalidades.posicionar
Ficha=ficha.Ficha





class Cliente(Conexion,tk.Frame):

    #clase de panel de cliente

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        

        self.var_entry_id=tk.StringVar()
        self.var_marca=tk.StringVar()
        self.var_modelo=tk.StringVar()
        self.var_matricula=tk.StringVar()

        
        
        
    def abrirFormularioCliente(self,boton):

        desactivar(boton)

        ventana_formulario=tk.Toplevel(self)
        ventana_formulario.resizable(0,0)
        ventana_formulario.transient(self)
        ventana_formulario.title("Clientes")
        posicionar(ventana_formulario)

        ventana_formulario.protocol(
            "WM_DELETE_WINDOW",
            lambda:self.cerrarTop(boton,ventana_formulario)
            )

        self.formulario=FormularioCliente(ventana_formulario)
        self.formulario.grid()
        

    def cerrarTop(self,boton,ventana):

        activar(boton)
        self.formulario.destroy()
        ventana.destroy()
    
    


    def ver_inicial(
        self,
        letra,
        frameGrande,
        abc,
        selec,
        lista
        ):

        #-ver registros segun la inicial de la lista desplegable--

        try:
            self.miCursor=self.miBase.cursor()
            if letra:
                letra="{}%".format(letra)
            if selec.get() == "Nombre"and letra:
                self.miCursor.execute(
            
                    "SELECT * FROM datos_usuarios2 where nombre like %s",
                    letra
                    )
                resultado = self.miCursor.fetchall()
                if resultado:
                    siHayFrame(lista)
                    self.ver_varios(resultado,frameGrande,lista)
                else:
                    messagebox.showinfo("Atención","Sin resultados")

            elif selec.get() == "1er Apellido" and letra:
                self.miCursor.execute(
                    "SELECT * FROM datos_usuarios2 where apellido like %s",
                    letra
                    )
                resultado = self.miCursor.fetchall()
                if resultado:
                    siHayFrame(lista)
                    self.ver_varios(resultado,frameGrande,lista)
                else:
                    messagebox.showinfo("Atención","Sin resultados")

            elif selec.get() == "2do Apellido" and letra:
                self.miCursor.execute(
                    "SELECT * FROM datos_usuarios2 where apellido_dos like %s",
                    letra
                    )
                resultado = self.miCursor.fetchall()
                if resultado:
                    siHayFrame(lista)
                    self.ver_varios(resultado,frameGrande,lista)
                else:
                    messagebox.showinfo("Atención","Sin resultados")

            elif selec.get() == "Marca" and letra:
                self.miCursor.execute(
                    "SELECT d.id_cliente,d.documento,d.nombre,d.apellido,d.apellido_dos,v.marca,v.modelo,v.matricula from vehiculos v join datos_usuarios2 d on d.id_cliente=v.cliente_n where v.marca like %s order by 1",
                    letra
                    )
                resultado=self.miCursor.fetchall()
                if resultado:
                    siHayFrame(lista)
                    self.ver_vehiculos(resultado,frameGrande,lista)
                else:
                    messagebox.showinfo("Atención","Sin resultados")

            elif selec.get() == "Modelo" and letra:
                self.miCursor.execute(
                    "SELECT d.id_cliente,d.documento,d.nombre,d.apellido,d.apellido_dos,v.marca,v.modelo,v.matricula from vehiculos v join datos_usuarios2 d on d.id_cliente=v.cliente_n where v.modelo like %s order by 1",
                    letra
                    )
                resultado=self.miCursor.fetchall()
                if resultado:
                    siHayFrame(lista)
                    self.ver_vehiculos(resultado,frameGrande,lista)
                else:
                    messagebox.showinfo("Atención","Sin resultados")

            elif selec.get() == "Matrícula" and letra:
                self.miCursor.execute(
                    "SELECT d.id_cliente,d.documento,d.nombre,d.apellido,d.apellido_dos,v.marca,v.modelo,v.matricula from vehiculos v join datos_usuarios2 d on d.id_cliente=v.cliente_n where v.matricula like %s order by 1",
                    letra
                    )
                resultado=self.miCursor.fetchall()
                if resultado:
                    siHayFrame(lista)
                    self.ver_vehiculos(resultado,frameGrande,lista)
                else:
                    messagebox.showinfo("Atención","Sin resultados")

            else:
                messagebox.showinfo("Atención","Filtro no especificado")


        except:
            messagebox.showinfo("Atención","Sin resultados")

        finally:

            self.miCursor.close()
            abc.set("")
            selec.set("")

    def ver_vehiculos(self,resultado,frameGrande,lista):

        # instancia de vehiculos muestra filtro en pantalla

        self.vehiculos=Vehiculos(frameGrande)
        self.vehiculos.grid()
        #siHayFrame(lista)
        self.vehiculos.verPorVehiculo(resultado,frameGrande,lista)




    def ver_todos(self,frameGrande,lista):

        #ver todos los clientes--

        self.miCursor=self.miBase.cursor()
        self.miCursor.execute(
            "SELECT id_cliente,ingreso,documento,nacimiento,nombre,apellido,apellido_dos,telefono,direccion,correo FROM datos_usuarios2 where estado=1")
        resultado = self.miCursor.fetchall()

        if resultado:


            siHayFrame(lista)

            self.ver_varios(resultado,frameGrande,lista)

        else:

            messagebox.showinfo("Atención","No hay registros")


    def verLaFicha(self,resultado,lista,frameGrande):

        if resultado:

            self.ficha=Ficha(frameGrande)
            self.ficha.grid()

            siHayFrame(lista)
            self.ficha.ver_ficha(frameGrande,resultado,lista)

        else:
            messagebox.showinfo("Atención","Sin resultados")
        
    

    def ver_varios(self,resultado,frameGrande,lista):

        siHayFrame(lista)


        #-mostrar mas de un resultado

        try:

            self.frameDinamico=tk.Frame(frameGrande,bg="")
            self.frameDinamico.grid(row=0,column=0,sticky="n")
            frameGrande.rowconfigure(0,weight=4)
            frameGrande.columnconfigure(0,weight=4)
            agregaFrame(self.frameDinamico,lista)

            #mostrar los datos encontrados
            frameTabla=tk.Frame(self.frameDinamico)
            frameTabla.grid(row=1,column=0,sticky="nsew")
            self.frameDinamico.rowconfigure(1,weight=4)
            self.frameDinamico.columnconfigure(0,weight=4)

            frameTitulo=tk.Frame(frameTabla)
            frameTitulo.grid(row=0, column=0)
            frameTabla.columnconfigure(0,weight=4)

            titulo_varios = tk.Label(
                frameTitulo,
                text="{} Clientes".format(len(resultado)),
                font=self.bold
                )
            titulo_varios.grid(row=0,column=0,ipady=3)
            
            frame3 = tk.Frame(
                frameTabla,
                relief="groove",
                bd=5
                )
            frame3.grid(
                sticky="nsew",
                row=1,
                column=0
                )



            frame4 = tk.Frame(frameTabla)
            frame4.grid(
                row=1,
                column=1,
                sticky="e"
                )
            campos = tk.Frame(frame3)
            campos.grid(row=0,column=0, sticky="nsew")


            
            

            texto=(
                "ID",
                "Ingreso",
                "Documento",
                "Nacimiento",
                "Nombre",
                "1er Apellido",
                "2do Apellido",
                "Teléfono",
                "Domicilio",
                "Correo"
                )

            width=8
            col=0
            for t in texto:

                campo = tk.Label(
                    campos,
                    text=texto[col],
                    bd=1,
                    relief="sunken",
                    background="#5a98c4",
                    fg="white",
                    width=width
                    )

                campo.grid(
                    row=0,
                    column=col,
                    ipady=5,
                    sticky="nsew"
                    )
            
                col+=1
                if col==1 or col==3 or col==7:
                    width=10
                elif col==2:
                    width=13
                elif 4<=col<=6:
                    width=15
                elif col==8:
                    width=28
                else:
                    width=30

            if len(resultado)>18:

                scroll = tk.Scrollbar(frame4)
                c=tk.Canvas(frame3,yscrollcommand=scroll.set)

                scroll.config(command=c.yview)
                scroll.grid(sticky="e",column=8,row=1,ipady=285)
                linea= tk.Frame(frame3)
                linea.grid(sticky="nse",column=9,row=1)
                contenedor = tk.Frame(c, width=100)
                contenedor.grid(row=2,column=0,pady=0)
            

                c.create_window(0,0,window=contenedor,anchor="nw")
                c.grid(sticky="nsew",row=1,column=0)
                frame3.rowconfigure(1,weight=32)
                frame3.columnconfigure(1,weight=1)

            else:
                contenedor = tk.Frame(frame3)
                contenedor.grid(row=2)

                            
            widgets2 = {}
            row=1
            for num, ing, doc, nac, nom, ape, ape_dos, tel, calle, n in resultado:

                ingVar=tk.StringVar()
                verDiaMesAnio(ing,ingVar)
                nacVar=tk.StringVar()
                verDiaMesAnio(nac,nacVar)
            
                widgets2[num] ={
                "Cliente Nº": tk.Label(
                    contenedor,
                    text=num,
                    bd=1,
                    relief="sunken",
                    width=8
                    ),
                "Ingreso": tk.Label(
                    contenedor,
                    text=ingVar.get(),
                    bd=1,
                    relief="sunken",
                    width=10
                    ),
                "Documento": tk.Label(
                    contenedor,
                    text=doc,
                    bd=1,
                    relief="sunken",
                    width=13
                    ),
                "Nacimiento": tk.Label(
                    contenedor,
                    text=nacVar.get(),
                    bd=1,
                    relief="sunken",
                    width=10
                    ),
                "Nombre": tk.Label(
                    contenedor,
                    text=nom,
                    bd=1,
                    relief="sunken",
                    width=15
                    ),
                "1er Apellido": tk.Label(
                    contenedor,
                    text=ape,
                    bd=1,
                    relief="sunken",
                    width=15
                    ),
                "2do Apellido": tk.Label(
                    contenedor,
                    text=ape_dos,
                    bd=1,
                    relief="sunken",
                    width=15
                    ),
                "Teléfono": tk.Label(
                    contenedor,
                    text=tel,
                    bd=1,
                    relief="sunken",
                    width=10
                    ),
                "Domicilio": tk.Label(
                    contenedor,
                    text=calle,
                    bd=1,
                    relief="sunken",
                    width=28
                    ),
                "Correo": tk.Label(
                    contenedor, 
                    text=n,
                    bd=1,
                    relief="sunken",
                    width=30
                    )
                }

                widgets2[num]["Cliente Nº"].grid(row=row, column=0, sticky="nsew",ipady=5)
                widgets2[num]["Ingreso"].grid(row=row, column=1, sticky="nsew",ipady=5)
                widgets2[num]["Documento"].grid(row=row, column=2, sticky="nsew",ipady=5)
                widgets2[num]["Nacimiento"].grid(row=row, column=3, sticky="nsew",ipady=5)
                widgets2[num]["Nombre"].grid(row=row, column=4, sticky="nsew",ipady=5)
                widgets2[num]["1er Apellido"].grid(row=row, column=5, sticky="nsew",ipady=5)
                widgets2[num]["2do Apellido"].grid(row=row, column=6, sticky="nsew",ipady=5)
                widgets2[num]["Teléfono"].grid(row=row, column=7, sticky="nsew",ipady=5)
                widgets2[num]["Domicilio"].grid(row=row, column=8, sticky="nsew",ipady=5)
                widgets2[num]["Correo"].grid(row=row, column=9, sticky="nsew",ipady=5)
                row+=1

            if len(resultado)>18:

                frame3.update()
                c.config(scrollregion=c.bbox("all"))

            

        except:

            messagebox.showinfo("Atención","Se ha perdido la conexión")

                 

        finally:
            
            self.miCursor.close()

    

    