import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pymysql
from belfrywidgets import ToolTip
import sys
sys.path.insert(1,"../panel")
import funcionalidades
posicionar=funcionalidades.posicionar


def verSeguros(resultado,ventana,imagen):

    frames1=tk.Frame(
        ventana,
        bg="black"
        )
    frames1.grid(sticky="ew",row=0)
    label_imagen=tk.Label(
        frames1,
        bg="black",
        image=imagen
        )
    label_imagen.grid(row=0,column=0,sticky="e",padx=20)

    label_titulo=tk.Label(
        frames1,
        bg="black",
        fg="white",
        text="Seguros registrados"
        )
    label_titulo.grid(row=0,column=1,padx=60)


    frame_s2 = tk.Frame(ventana)
    frame_s2.grid(row=1,column=0)

    campos=tk.Frame(frame_s2)
    campos.grid(row=0,column=0)


    frameScroll=tk.Frame(ventana)
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
    
    contenedor = tk.Frame(
        c
        )
    contenedor.grid(
        row=2
        )

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
        width=6,
        background="#5a98c4",
        fg="white"
        )
    ide.grid(row=0, column=0,sticky="w",ipady=5)
    nombre = tk.Label(
        campos,
        text="Seguro",
        borderwidth=2,
        relief="groove",
        width=15,
        background="#5a98c4",
        fg="white"
        )
    nombre.grid(row=0, column=1,sticky="w",ipady=5)
    dire = tk.Label(
        campos,
        text="Dirección",
        borderwidth=2,
        relief="groove",
        width=25,
        background="#5a98c4",
        fg="white"
        )
    dire.grid(row=0, column=2,sticky="w",ipady=5)
    tel = tk.Label(
        campos,
        text="Teléfono",
        borderwidth=2,
        relief="groove",
        width=12,
        background="#5a98c4",
        fg="white"
        )
    tel.grid(row=0, column=3,sticky="w",ipady=5)
    persona = tk.Label(
        campos,
        text="Persona de contacto",
        borderwidth=2,
        relief="groove",
        width=25,
        background="#5a98c4",
        fg="white"
        )
    persona.grid(row=0, column=4,sticky="w",ipady=5)

    listado = {}
    row=1
    for ide,nom,dire,tel,pers in resultado:
    
        listado[ide] ={
        "Id": tk.Label(
            contenedor,
            text=ide,
            borderwidth=2,
            relief="groove",
            width=6
            ),
        "Seguro": tk.Label(
            contenedor,
            text=nom,
            borderwidth=2,
            relief="groove",
            width=15
            ),
        "Direccion": tk.Label(
            contenedor,
            text=dire,
            borderwidth=2,
            relief="groove",
            width=25
            ),
        "Telefono": tk.Label(
            contenedor,
            text=tel,
            borderwidth=2,
            relief="groove",
            width=12
            ),
        "Persona": tk.Label(
            contenedor,
            text=pers,
            borderwidth=2,
            relief="groove",
            width=25
            )
        }
        listado[ide]["Id"].grid(row=row, column=0,ipady=5) 
        listado[ide]["Seguro"].grid(row=row, column=1,ipady=5)
        listado[ide]["Direccion"].grid(row=row, column=2,ipady=5)
        listado[ide]["Telefono"].grid(row=row, column=3,ipady=5)
        listado[ide]["Persona"].grid(row=row, column=4,ipady=5)
        row+=1

        linea= tk.Frame(frame_s2)
        linea.grid(
            sticky="nse",
            column=3,
            row=1
            )

        frame_s2.update()
        c.config(scrollregion=c.bbox("all"))#fin del scroll

def agregar(imagen,serv,miBase):

        ide = tk.StringVar()
        nombre = tk.StringVar()
        dire = tk.StringVar()
        tel= tk.StringVar()
        contacto= tk.StringVar()

        ventana=tk.Toplevel(serv)
        ventana.resizable(0,0)
        ventana.transient()
        posicionar(ventana)

        frame_superior = tk.Frame(ventana,bg="black")
        frame_superior.grid(row=0,sticky="nsew")

        frame_medio = tk.Frame(ventana)
        frame_medio.grid(row=1)
        
        frame_inferior = tk.Frame(ventana,bg="#214472")
        frame_inferior.grid(row=2)

        label_img=tk.Label(
            frame_superior,
            image=imagen,
            bg="black"
            )
        label_img.grid(row=0,column=0,padx=20)

        label_superior=tk.Label(
            frame_superior,
            text="Formulario Seguros",
            bg="black",
            fg="white"
            )
        label_superior.grid(row=0,column=1,padx=30)


        idLabel = tk.Label(
            frame_medio,
            text="Id: "
            )
        idLabel.grid(row=1, column=0,sticky="e", padx=10,pady=10)


        nomLabel = tk.Label(
            frame_medio,
            text="Nombre: "
            )
        nomLabel.grid(row=2, column=0,sticky="e", padx=4,pady=10)

        direLabel = tk.Label(
            frame_medio,
            text="Dirección: "
            )
        direLabel.grid(row=3, column=0,sticky="e", padx=4,pady=10)

        telLabel = tk.Label(
            frame_medio,
            text="Teléfono: "
            )
        telLabel.grid(row=4, column=0,sticky="e", padx=4,pady=10)

        contLabel = tk.Label(
            frame_medio,
            text="Contacto: "
            )
        contLabel.grid(row=5, column=0,sticky="e", padx=4,pady=10)

        id_entry = tk.Entry(
            frame_medio,
            width=10,
            textvariable=ide
            )
        id_entry.grid(row=1, column=1, padx=10,pady=10,sticky="w")

        nom_entry = tk.Entry(
            frame_medio,
            width=40,
            textvariable=nombre
            )
        nom_entry.grid(row=2, column=1,padx=10,pady=10,sticky="w")

        dire_entry = tk.Entry(
            frame_medio,
            width=40,
            textvariable=dire
            )
        dire_entry.grid(row=3, column=1,padx=10,pady=10,sticky="w")

        tel_entry = tk.Entry(
            frame_medio,
            width=40,
            textvariable=tel
            )
        tel_entry.grid(row=4, column=1,padx=10,pady=10,sticky="w")

        cont_entry = tk.Entry(
            frame_medio,
            width=40,
            textvariable=contacto
            )
        cont_entry.grid(row=5, column=1,padx=10,pady=10,sticky="w")

        #botones
        texto=("Limpiar","Buscar","Actualizar","Crear")
        funciones=(
            lambda:limpiar(id_entry,ide,nombre,dire,tel,contacto),
            lambda:buscar(id_entry,ide,nombre,dire,tel,contacto,miBase),
            lambda:actualizar(id_entry,ide,nombre,dire,tel,contacto,miBase),
            lambda:crearSeguro(ide,nombre,dire,tel,contacto,miBase)
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

def limpiar(id_entry,ide,nombre,dire,tel,contacto):

    id_entry.config(state="normal")
    ide.set("")
    nombre.set("")
    dire.set("")
    tel.set("")
    contacto.set("")


def buscar(id_entry,ide,nombre,dire,tel,contacto,miBase):
    
    # buscar seguro en el formulario

    try:
        
        miCursor = miBase.cursor()
        

        if ide.get():

            
            miCursor.execute(
                "SELECT * FROM seguros where id_seguro = %s;",
                ide.get()
                )

        elif nombre.get():


            miCursor.execute(
                "SELECT * FROM seguros where nombre = %s;",
                nombre.get()
                )

        resultado = miCursor.fetchone()

        ide.set(resultado[0])
        id_entry.config(state="readonly")
        nombre.set(resultado[1])
        dire.set(resultado[2])
        tel.set(resultado[3])
        contacto.set(resultado[4])



    except pymysql.err.DataError:
        limpiar(ide,nombre,dire,tel,contacto)
        messagebox.showerror("Error", "Datos incorrectos")
        

    except TypeError:
        limpiar(id_entry,ide,nombre,dire,tel,contacto)
        messagebox.showinfo("Atencion", "Seguro no encontrado")
   

    finally:
        
        miBase.commit()
        miCursor.close()


def crearSeguro(ide,nombre,dire,tel,contacto,miBase):
    #-crear seguro--

    try:
        miCursor = miBase.cursor()

        if nombre.get() and dire.get() and tel.get() and contacto.get():

            consulta="INSERT INTO seguros (id_seguro,nombre,direccion,telefono,persona_contacto) values (null,%s,%s,%s,%s)"

            miCursor.execute(
                consulta,
                (
                    nombre.get(),
                    dire.get(),
                    tel.get(),
                    contacto.get()
                    )
                )

            messagebox.showinfo(
                "Nuevo Seguro",
                "{} fue agregado con éxito".format(nombre.get()
                    )
                )

        else:

            messagebox.showerror(
                "Atención",
                "Datos incompletos"
                )

    except pymysql.err.IntegrityError:
        messagebox.showinfo(
            "Error",
            "Datos únicos ya existentes"
            )

    except pymysql.err.InternalError:
        messagebox.showinfo(
            "Atención",
            "Datos incorrectos o incompletos, verifique"
            )

    except IndexError:
        messagebox.showinfo(
            "Atención",
            "Verificar datos"
            )

    finally:

        miBase.commit()
        miCursor.close()

def actualizar(id_entry,ide,nombre,dire,tel,contacto,miBase):

    try:
        miCursor=miBase.cursor()

        buscado=miCursor.execute(
                "SELECT * FROM seguros where id_seguro = %s",
                ide.get()
                )
        encontrado=miCursor.fetchone()

            
        if encontrado:
            consulta = "UPDATE seguros set nombre=(%s),direccion=(%s),telefono=(%s),persona_contacto=(%s) where id_seguro=(%s)"
            miCursor.execute(
                consulta,
                (
                    nombre.get(),
                    dire.get(),
                    tel.get(),
                    contacto.get(),
                    encontrado[0]
                    )
                )

            messagebox.showinfo(
                "Información", 
                "Seguro \nNº{} {}\nActualizado con éxito".format(
                    ide.get(),nombre.get()
                    )
                )
            limpiar(id_entry,ide,nombre,dire,tel,contacto)
        else:
            messagebox.showinfo("Atencion","Ingrese un registro válido")

    finally:

        miBase.commit()
        miCursor.close()