import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import pymysql
from belfrywidgets import ToolTip
import sys
sys.path.insert(1,"../conexion")
import conexion
sys.path.insert(1,"../panel")
import funcionalidades

Conexion=conexion.Conexion
adaptable=funcionalidades.adaptable
verDiaMesAnio=funcionalidades.verDiaMesAnio
siHayFrame=funcionalidades.siHayFrame
agregaFrame=funcionalidades.agregaFrame
cerrarFrame=funcionalidades.cerrarFrame
desactivar=funcionalidades.desactivar
activar=funcionalidades.activar
posicionar=funcionalidades.posicionar
cerrarToplevel=funcionalidades.cerrarToplevel


class Movimientos(Conexion,tk.Frame):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.listaMov=[] # lista para el formulario dinámico
        self.listaMov2=[]

        
    def pantallaMovimientos(self,frameGrande,lista):

        siHayFrame(lista)

        self.frameDinamico=tk.Frame(frameGrande,bg="")
        self.frameDinamico.grid(row=0,column=0,sticky="nsew")
        frameGrande.rowconfigure(0,weight=4)
        frameGrande.columnconfigure(0,weight=4)
        agregaFrame(self.frameDinamico,lista)

        # frame izquierdo

        frameIzquierdo=tk.Frame(self.frameDinamico,bg="")
        frameIzquierdo.grid(row=0,column=0,sticky="nw",padx=0)
        self.frameDinamico.rowconfigure(0, weight=4)

        frameLinea=tk.Frame(self.frameDinamico,bg="#000",width=2)
        frameLinea.grid(row=0,column=1,sticky="ns")


        formMovimientos=tk.Frame(frameIzquierdo)
        formMovimientos.grid(row=2,column=0,sticky="nw")

        titMovimientos=tk.Label(
            formMovimientos,
            text="Gestión de movimientos",
            bg="black",
            fg="white",
            bd=1
            )
        titMovimientos.grid(row=0,column=0,sticky="nsew",ipady=5)

        frameDeBotones=tk.Frame(formMovimientos)
        frameDeBotones.grid(row=1,column=0)

        self.boton=tk.Button(
            frameDeBotones,
            image=self.ingresos,
            command=lambda:self.formularioDinamico("ingresos"),
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            text=" Ingresos",
            font=self.bold,
            compound="left"
            )
        self.boton.grid(row=0,column=0,ipadx=10)

        self.boton2=tk.Button(
            frameDeBotones,
            image=self.egresos,
            command=lambda:self.formularioDinamico("egresos"),
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            text=" Egresos",
            font=self.bold,
            compound="left"
            )
        self.boton2.grid(row=0,column=1,ipadx=10)
            

        self.frameFormulario=tk.Frame(formMovimientos,bd=0)
        self.frameFormulario.grid(row=2,column=0,sticky="nsew")

        self.frameTabla=tk.Frame(self.frameDinamico,bg="")
        self.frameTabla.grid(row=0,column=2,sticky="nw")

        self.frame = tk.Frame(self.frameTabla)
        self.frame.grid(row=1,column=0)

        campos=tk.Frame(self.frame)
        campos.grid(row=0,column=0)

        listaCampos=["ID","Artículo","Costo unitario","Cantidad","Fecha","Usuario"]
        w=8
        col=0

        for l in listaCampos:
            label=tk.Label(
                campos,
                text=listaCampos[col],
                bd=1,
                width=w,
                bg="black",
                fg="white"
                )
            label.grid(row=0,column=col,ipady=5)
            col += 1

            if col==1:
                w=25
            else:
                w=15

        self.formularioDinamico("ingresos")


        

    def formularioDinamico(self,tabla):


        elFormulario=tk.Frame(self.frameFormulario)
        elFormulario.grid(row=0,column=0,sticky="nsew")


        if tabla == "ingresos":

           
            self.boton.config(bg="green",fg="white")
            self.boton2.config(bg="white",fg="#27455b")

        elif tabla == "egresos":

        
            self.boton2.config(bg="red",fg="white")
            self.boton.config(bg="white",fg="#27455b")


        elTexto="Gestionar {}".format(tabla)

        titulo=tk.Label(
            elFormulario,
            text=elTexto,
            fg="#27455b",
            font=self.bold
            )
        titulo.grid(row=0,column=0,ipady=5,sticky="nsew")

        frameCuerpo=tk.Frame(elFormulario)
        frameCuerpo.grid(row=1,column=0,sticky="nsew")

        labels=["ID:", "Artículo:","Costo unitario:","Cantidad:"]
        i=0
        for l in labels:

            label=tk.Label(frameCuerpo,text=labels[i])
            label.grid(row=i,column=0,sticky="e",pady=10,padx=10)

            i += 1

        self.IdMov=tk.StringVar()
        self.costoUnit=tk.StringVar()
        self.laCantidad=tk.StringVar()
       

        self.entryMov=tk.Entry(
            frameCuerpo,
            width=8,
            textvariable=self.IdMov)
        self.entryMov.grid(row=0,column=1,sticky="w",padx=10)
        MovId=tk.Button(
            frameCuerpo,
            image=self.lupa,
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            command=lambda:self.buscar(tabla)
            )
        MovId.grid(row=0,column=1)
        ToolTip(MovId,"Buscar por ID")

        self.comboArt=ttk.Combobox(
            frameCuerpo,
            values=self.selec_articulo(),
            state="readonly",
            width=18
            )
        self.comboArt.grid(row=1,column=1,sticky="w",padx=10)

        cargaArt=tk.Button(
            frameCuerpo,
            image=self.cargarArticulo,
            command=lambda:self.cargaArticulo(),
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            )
        cargaArt.grid(row=1,column=2)

        self.entryCosto=tk.Entry(
            frameCuerpo,
            width=8,
            textvariable=self.costoUnit)
        self.entryCosto.grid(row=2,column=1,sticky="w",padx=10)

        self.entryCant=tk.Entry(
            frameCuerpo,
            width=8,
            textvariable=self.laCantidad)
        self.entryCant.grid(row=3,column=1,sticky="w",padx=10)

        frameBotones=tk.Frame(elFormulario,bg="#214472")
        frameBotones.grid(row=2,column=0,pady=15,sticky="nsew")



        #botones
        
        funciones=(
            lambda:self.limpiar(),
            lambda:self.actualizar(tabla),
            lambda:self.crear(tabla)
            )

        n=0
        for t in self.texto:
            boton=tk.Button(
                frameBotones,
                image=self.imagenes[n],
                command=funciones[n],
                cursor="hand2",
                relief="flat",
                bg="#214472",
                fg="white",
                activebackground="black",
                activeforeground="white",
                text=self.texto[n],
                font=self.bold,
                compound="left"
                )
            boton.grid(row=0,pady=5,padx=10,column=n)
            n+=1

        self.crearFrame(tabla)

    def cargaArticulo(self):

        if self.comboArt.get():

            try:
                self.miCursor=self.miBase.cursor()

                self.miCursor.execute("SELECT costo from articulos where nombre=%s",self.comboArt.get())
                resultado=self.miCursor.fetchone()

                self.costoUnit.set(resultado[0])

            except:
                messagebox.showinfo("Aviso","Datos no cargados")

            finally:
                self.miCursor.close()


    def limpiar(self):

        self.IdMov.set("")
        self.comboArt.set("")
        self.costoUnit.set("")
        self.laCantidad.set("")
        self.entryMov.config(state="normal")

    def actualizar(self,tabla):

        if self.IdMov.get() and self.comboArt.get() and self.laCantidad.get().isdigit() and self.costoUnit.get().isdigit():

            try:

                self.miCursor=self.miBase.cursor()

                self.miCursor.execute("SELECT idArt from articulos where nombre like %s",self.comboArt.get())
                ide=self.miCursor.fetchone()

                if tabla == "ingresos":

                    actualiza="UPDATE  ingresos set costo=(%s),cantidad=(%s),usuario=(%s) where id=%s"

                elif tabla == "egresos":

                    actualiza="UPDATE  egresos set costo=(%s),cantidad=(%s),usuario=(%s) where id=%s"

                self.miCursor.execute(
                    actualiza,
                    (
                        self.costoUnit.get(),
                        self.laCantidad.get(),
                        2,
                        self.IdMov.get()
                        )
                    )

                if tabla == "ingresos":

                    self.miCursor.execute("SELECT id FROM ingresos")

                if tabla == "egresos":

                    self.miCursor.execute("SELECT id FROM egresos")


                cantidad=self.miCursor.fetchall()

                self.limpiar()

                self.formularioDinamico(tabla)

                messagebox.showinfo("Aviso","Registro exitoso")

                
            except:

                messagebox.showinfo("Aviso","No se ha podido actualizar")

            finally:
                self.miBase.commit()
                self.miCursor.close()



        else:

            messagebox.showinfo("Atención","Faltan datos")

    def crear(self,tabla):

        if self.comboArt.get() and self.laCantidad.get().isdigit() and self.costoUnit.get().isdigit():

            try:

                self.miCursor=self.miBase.cursor()

                dt= datetime.datetime.now()
                actual=dt.strftime("%Y-%m-%d")

                self.miCursor.execute("SELECT idArt from articulos where nombre=%s",self.comboArt.get())
                IdArticulo=self.miCursor.fetchone()

                if tabla == "ingresos":

                    insertar="INSERT INTO ingresos (articulo,costo,cantidad,fecha,usuario) values(%s,%s,%s,%s,%s)"

                else:

                    insertar="INSERT INTO egresos (articulo,costo,cantidad,fecha,usuario) values(%s,%s,%s,%s,%s)"

                self.miCursor.execute(
                    insertar,
                    (
                        IdArticulo[0],
                        self.costoUnit.get(),
                        self.laCantidad.get(),
                        actual,
                        1
                        )
                    )

                self.miCursor.execute("SELECT existencias from existencias where id=%s",IdArticulo[0])
                existe=self.miCursor.fetchone()

                # se suma o resta a las existencias

                if tabla == "ingresos":

                    existencia= int(existe[0]) + int(self.laCantidad.get())
                    actualizaExistencias = "UPDATE existencias set existencias=(%s),ingreso=(%s) where id=%s"

                else:

                    existencia = int(existe[0]) - int(self.laCantidad.get())
                    actualizaExistencias = "UPDATE existencias set existencias=(%s),egreso=(%s) where id=%s"

            
                self.miCursor.execute(
                    actualizaExistencias,
                    (
                        existencia,
                        actual,
                        IdArticulo[0]
                        )
                    )

                if tabla == "ingresos":

                    self.miCursor.execute("SELECT id FROM ingresos")

                if tabla == "egresos":

                    self.miCursor.execute("SELECT id FROM egresos")


                cantidad=self.miCursor.fetchall()

                self.limpiar()

                self.formularioDinamico(tabla)

                messagebox.showinfo("Aviso","Registro exitoso")



            except:

                messagebox.showerror("Error","Registro no efectuado")

            finally:

                self.miBase.commit()
                self.miCursor.close()
                self.limpiar()

        else:

            messagebox.showinfo("Atención","Faltan datos")


    def buscar(self,tabla):

        if self.IdMov.get():

            try:
                self.miCursor=self.miBase.cursor()

                if tabla == "ingresos":

                    consulta="SELECT articulo,costo,cantidad FROM ingresos where id = %s"

                elif tabla == "egresos":

                    consulta="SELECT articulo,costo,cantidad FROM egresos where id = %s"

                self.miCursor.execute(
                    consulta,
                    (
                        self.IdMov.get()
                        )

                    )
                encontrado=self.miCursor.fetchone()

                self.costoUnit.set(encontrado[1])
                self.laCantidad.set(encontrado[2])

                self.miCursor.execute("SELECT nombre from articulos where idArt=%s",encontrado[0])
                art=self.miCursor.fetchone()

                self.comboArt.set(art[0])


                self.entryMov.config(state="disable")
                

            except:
                messagebox.showinfo("Aviso","Registro no encontrado")
                
            finally:
                
                self.miCursor.close()

        else:

            messagebox.showerror("Error","Ingrese un número")


    def selec_articulo(self):

        try:
            self.miCursor = self.miBase.cursor()
            self.miCursor.execute("SELECT nombre FROM articulos order by idArt")
            artic=self.miCursor.fetchall()

            lista = []
            n=0
            for a in artic:
                
                lista.append(artic[n][0])
                n += 1
            return lista

        finally:

            self.miCursor.close()



    def crearFrame(self,tabla):

        try:

            self.miCursor = self.miBase.cursor()

            if tabla == "ingresos":

                self.miCursor.execute("SELECT * FROM ingresos order by id ASC")

            if tabla == "egresos":

                self.miCursor.execute("SELECT * FROM egresos order by id ASC")


            resultado = self.miCursor.fetchall()

            if resultado:

                if len(resultado)>18:


                    self.frameScroll=tk.Frame(self.frameTabla)
                    self.frameScroll.grid(row=1,column=2,sticky="e")

                    scroll = tk.Scrollbar(self.frameScroll)#comienzo del  scroll
                    
                    self.canvas=tk.Canvas(
                        self.frame,
                        yscrollcommand=scroll.set
                        )

                    scroll.config(command=self.canvas.yview)
                    scroll.grid(
                        sticky="e",
                        column=0,
                        row=1,
                        ipady=285
                        )
                    
                    self.contenedor = tk.Frame(self.canvas)
                    self.contenedor.grid(row=2,sticky="nsew")

                    self.canvas.create_window(
                        0,0,
                        window=self.contenedor,
                        anchor="nw"
                        )
                    self.canvas.grid(sticky="nsew")

                else:

                    self.contenedor = tk.Frame(self.frameTabla)
                    self.contenedor.grid(row=2,sticky="nsew")


                
                listado = {}
                row=0
                for ide,art,costo,cant,fecha,usu in resultado:

                    self.miCursor.execute("SELECT nombre from articulos where idArt=%s",art)
                    articulo=self.miCursor.fetchone()

                    fechaVer=tk.StringVar()
                    verDiaMesAnio(fecha,fechaVer)
                
                    listado[art] ={
                    "Id": tk.Label(
                        self.contenedor,
                        text=ide,
                        bd=1,
                        relief="sunken",
                        width=8
                        ),
                    "Articulo": tk.Label(
                        self.contenedor,
                        text=articulo[0],
                        bd=1,
                        relief="sunken",
                        width=25
                        ),
                    "Costo": tk.Label(
                        self.contenedor,
                        text=costo,
                        bd=1,
                        relief="sunken",
                        width=15
                        ),
                    "Cantidad": tk.Label(
                        self.contenedor,
                        text=cant,
                        bd=1,
                        relief="sunken",
                        width=15
                        ),
                    "Fecha": tk.Label(
                        self.contenedor,
                        text=fechaVer.get(),
                        bd=1,
                        relief="sunken",
                        width=15
                        ),
                    "Usuario": tk.Label(
                        self.contenedor,
                        text=usu,
                        bd=1,
                        relief="sunken",
                        width=15
                        )
                    
                    
                    }

               
                    listado[art]["Id"].grid(row=row, column=0,ipady=5)
                    listado[art]["Articulo"].grid(row=row, column=1,ipady=5) 
                    listado[art]["Costo"].grid(row=row, column=2,ipady=5)
                    listado[art]["Cantidad"].grid(row=row, column=3,ipady=5)
                    listado[art]["Fecha"].grid(row=row, column=4,ipady=5)
                    listado[art]["Usuario"].grid(row=row, column=5,ipady=5)
                    row+=1

                    linea= tk.Frame(self.frame)
                    linea.grid(
                        sticky="nse",
                        column=3,
                        row=0
                        )

                    if len(resultado)>18:

                        self.frame.update()
                        self.canvas.config(scrollregion=self.canvas.bbox("all"))#fin del scroll
        #except:
            #messagebox.showinfo("Atencion","No hay datos")

        finally:

            self.miCursor.close()