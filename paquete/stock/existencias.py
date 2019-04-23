import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import pymysql
import sys
sys.path.insert(1,"../conexion")
import conexion
sys.path.insert(1,"../panel")
import funcionalidades

Conexion=conexion.Conexion
adaptable=funcionalidades.adaptable
agregaFrame=funcionalidades.agregaFrame
siHayFrame=funcionalidades.siHayFrame
verDiaMesAnio=funcionalidades.verDiaMesAnio


class Existencias(Conexion,tk.Frame):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


    def pantallaExistencias(self,frameGrande,lista):

        siHayFrame(lista)

        self.frameDinamico=tk.Frame(frameGrande,bg="")
        self.frameDinamico.grid(row=0,column=0,sticky="nsew")
        frameGrande.rowconfigure(0,weight=4)
        frameGrande.columnconfigure(0,weight=4)
        agregaFrame(self.frameDinamico,lista)

        frameIzquierdo=tk.Frame(self.frameDinamico,bg="")
        frameIzquierdo.grid(row=0,column=0,sticky="nw",padx=0)
        self.frameDinamico.rowconfigure(0, weight=4)

        frameLinea=tk.Frame(self.frameDinamico,bg="#000",width=2)
        frameLinea.grid(row=0,column=1,sticky="ns")

        formLimites=tk.Frame(frameIzquierdo)
        formLimites.grid(row=0,column=0,sticky="nw")

        titLimites=tk.Label(
            formLimites,
            text="Gestión de límites",
            bg="black",
            fg="white",
            bd=1
            )
        titLimites.grid(row=0,column=0,sticky="nsew",ipady=5)
        frameFormulario=tk.Frame(formLimites,bd=0)
        frameFormulario.grid(row=1,column=0,sticky="nsew")

        labelsLimites=["Artículo","Mínimo","Máximo"]

        n=0

        for l in labelsLimites:

            labelLimit=tk.Label(frameFormulario,text=labelsLimites[n])
            labelLimit.grid(row=n,column=0,sticky="e",padx=10,pady=10)
            n += 1

        self.comboArt=ttk.Combobox(
            frameFormulario,
            values=self.selec_articulo(),
            state="readonly",
            width=18
            )
        self.comboArt.grid(row=0,column=1,padx=10,pady=10,sticky="w")

        self.entryMin=tk.StringVar()
        self.entryMax=tk.StringVar()

        entMin=tk.Entry(frameFormulario,textvariable=self.entryMin,width=8)
        entMin.grid(row=1,column=1,padx=10,pady=10,sticky="w")
        entMax=tk.Entry(frameFormulario,textvariable=self.entryMax,width=8)
        entMax.grid(row=2,column=1,padx=10,pady=10,sticky="w")

        # botones del formulario

        cargaArt=tk.Button(
            frameFormulario,
            image=self.cargarArticulo,
            command=lambda:self.cargaLimites(),
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            )
        cargaArt.grid(row=0,column=2,padx=10,pady=10,sticky="w")

        frameBotones=tk.Frame(frameFormulario,bg="#214472")
        frameBotones.grid(row=3,column=0,columnspan=3,pady=(25,0),sticky="nsew")

        funciones=(
            lambda:self.limpiar(),
            lambda:self.modificarLimites()
            )
        texto=[" Limpiar"," Establecer límites"]

        imagenes=[self.escoba,self.limites]

        n=0
        for t in texto:
            boton=tk.Button(
                frameBotones,
                image=imagenes[n],
                command=funciones[n],
                cursor="hand2",
                relief="flat",
                bg="#214472",
                fg="white",
                activebackground="black",
                activeforeground="white",
                text=texto[n],
                font=self.bold,
                compound="left"
                )
            boton.grid(row=0,pady=5,padx=10,column=n)
            n+=1


        self.frameTabla=tk.Frame(self.frameDinamico,bg="")
        self.frameTabla.grid(row=0,column=2,sticky="nw")

        self.frame = tk.Frame(self.frameTabla)
        self.frame.grid(row=1,column=0)

        campos=tk.Frame(self.frame)
        campos.grid(row=0,column=0)

        listaCampos=["Artículo","Existencias","Cantidad","Mínimo","Máximo","Último ingreso","Último egreso"]
        w=25
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
                w=11
            elif col==2:
                w=18
            elif 3<=col<=4:
                w=10
            else:
                w=14

        


        self.crearFrame()



    def limpiar(self):

        self.comboArt.set("")
        self.entryMin.set("")
        self.entryMax.set("")

    def modificarLimites(self):

        if int(self.entryMin.get()) > int(self.entryMax.get()):

            messagebox.showerror("Incorrecto", "Mínimo debe ser menor que máximo")

        elif self.entryMin.get() and self.entryMax.get():

            try:

                self.miCursor=self.miBase.cursor()

                self.miCursor.execute("SELECT idArt from articulos where nombre like %s",self.comboArt.get())
                ide=self.miCursor.fetchone()

                actualiza="UPDATE existencias set minimo=(%s),maximo=(%s) where id=%s"

                self.miCursor.execute(
                    actualiza,
                    (
                    self.entryMin.get(),
                    self.entryMax.get(),
                    ide
                    )
                    )

                self.miCursor.execute("SELECT id FROM existencias")
                cantidad=self.miCursor.fetchall()


                self.limpiar()

                if len(cantidad) > 1:

                    self.eliminaFrame(cantidad)

                self.crearFrame()

            except:
                messagebox.showerror("Error","No se ha podido actualizar")

            finally:
                self.miBase.commit()
                self.miCursor.close()
                messagebox.showinfo("Aviso","Límites establecidos")

        else:
            messagebox.showinfo("Datos","Faltan datos")

    def eliminaFrame(self,cantidad):

        #para poder actualizar el frame cuando se hacen cambios

        self.contenedor.destroy()

        if len(cantidad) > 18:

                self.frameScroll.destroy()
                self.canvas.destroy()


    def cargaLimites(self):

        """primero busca el nombre que coincida con el
        id de articulos y existencias para poder extraer
        minimo y maximo, y plasmarlos en los entry"""

        if self.comboArt.get():

            try:
                self.miCursor=self.miBase.cursor()

                self.miCursor.execute("SELECT idArt from articulos where nombre like %s",self.comboArt.get())
                ide=self.miCursor.fetchone()

                self.miCursor.execute("SELECT minimo,maximo from existencias where id=%s",ide)
                resultado=self.miCursor.fetchone()

                self.entryMin.set(resultado[0])
                self.entryMax.set(resultado[1])


            finally:

                self.miCursor.close()


    def crearFrame(self):

        try:

            self.miCursor = self.miBase.cursor()
            self.miCursor.execute("SELECT * FROM existencias order by id ASC")
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
                for art,exi,cant,mini,maxi,ing,egre in resultado:

                    self.miCursor.execute("SELECT nombre from articulos where idArt=%s",art)
                    articulo=self.miCursor.fetchone()

                    # calculo de las unidades de medida según las existencias
                    listaCant=cant.split(" ")
                    cantidad=float(listaCant[0])
                    total=cantidad*(float(exi))
                    self.miCursor.execute("SELECT medida from medidas where id=%s",listaCant[1])
                    letras=self.miCursor.fetchone()

                    eltotal="{} {}".format(total,letras[0])

                    ingVar=tk.StringVar()
                    egreVar=tk.StringVar()
                    verDiaMesAnio(ing,ingVar)
                    verDiaMesAnio(egre,egreVar)
                
                    listado[art] ={
                    "Id": tk.Label(
                        self.contenedor,
                        text=articulo[0],
                        bd=1,
                        relief="sunken",
                        width=25
                        ),
                    "Existencias": tk.Label(
                        self.contenedor,
                        text=exi,
                        bd=1,
                        relief="sunken",
                        width=11
                        ),
                    "Total": tk.Label(
                        self.contenedor,
                        text=eltotal,
                        bd=1,
                        relief="sunken",
                        width=18
                        ),
                    "Min": tk.Label(
                        self.contenedor,
                        text=mini,
                        bd=1,
                        relief="sunken",
                        width=10
                        ),
                    "Max": tk.Label(
                        self.contenedor,
                        text=maxi,
                        bd=1,
                        relief="sunken",
                        width=10
                        ),
                    "Ingreso": tk.Label(
                        self.contenedor,
                        text=ingVar.get(),
                        bd=1,
                        relief="sunken",
                        width=14
                        ),
                    "Egreso": tk.Label(
                        self.contenedor,
                        text=egreVar.get(),
                        bd=1,
                        relief="sunken",
                        width=14
                        )
                    
                    }

                    # condicionales si esta por debajo del minimo y si esta por encima del maximo
                    if int(exi) <= int(mini):
                        listado[art]["Existencias"].config(bg="red",fg="#fff")

                    elif int(exi) > int(maxi) and int(maxi) != 0:
                        listado[art]["Existencias"].config(bg="green",fg="#fff")

                    else:
                        listado[art]["Existencias"].config(bg="#dbdddd",fg="#000")

                    listado[art]["Id"].grid(row=row, column=0,ipady=5)
                    listado[art]["Existencias"].grid(row=row, column=1,ipady=5) 
                    listado[art]["Total"].grid(row=row, column=2,ipady=5)
                    listado[art]["Min"].grid(row=row, column=3,ipady=5)
                    listado[art]["Max"].grid(row=row, column=4,ipady=5)
                    listado[art]["Ingreso"].grid(row=row, column=5,ipady=5)
                    listado[art]["Egreso"].grid(row=row, column=6,ipady=5)
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
        



