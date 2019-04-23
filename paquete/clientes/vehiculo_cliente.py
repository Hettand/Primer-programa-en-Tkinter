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
posicionar=funcionalidades.posicionar
siHayFrame=funcionalidades.siHayFrame
agregaFrame=funcionalidades.agregaFrame
cerrarFrame=funcionalidades.cerrarFrame



class Vehiculos(Conexion,ttk.Frame):


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


    def verPorVehiculo(self,resultado,frameGrande,lista):

        self.frameDinamico=tk.Frame(frameGrande,bg="")
        self.frameDinamico.grid(row=0,column=0,sticky="n",pady=(20,0))
        frameGrande.rowconfigure(0,weight=4)
        frameGrande.columnconfigure(0,weight=4)
        agregaFrame(self.frameDinamico,lista)

        frameTitulo=tk.Frame(self.frameDinamico)
        frameTitulo.grid(row=0,column=0,sticky="nsew")

        titulo_ver = tk.Label(
            frameTitulo, 
            text="Clientes que coinciden con su búsqueda: {}".format(
                len(resultado)
                ),
            height=2, 
            bd=1,
            relief="groove",
            bg="black",
            fg="white"

            )
        titulo_ver.grid(row=0,column=0,sticky="nsew")
        frameTitulo.columnconfigure(0, weight=20)

        botonCerrar=tk.Button(
            frameTitulo,
            text="x",
            bg="red",
            fg="white",
            relief="flat",
            font=("verdana",12,"bold"),
            command=lambda:cerrarFrame(lista)
            )
        botonCerrar.grid(row=0,column=1,ipadx=2,ipady=2,sticky="nsew")
        frameTitulo.columnconfigure(1, weight=1)

        frame3 = tk.Frame(self.frameDinamico)
        frame3.grid(sticky="nsew",row=2,column=0)


        frame4 = tk.Frame(self.frameDinamico)
        frame4.grid(sticky="e",row=2,column=1)
        #frameDinamico.columnconfigure(0, weight=1)


        campos = tk.Frame(frame3)
        campos.grid(row=1,sticky="nsew")

        texto=(
            "Cliente Nº",
            "Documento",
            "Nombre",
            "1er Apellido",
            "2do Apellido",
            "Marca",
            "Modelo",
            "Matricula"
            )
        col=0
        width=10

        for t in texto:
            label = tk.Label(
                campos,
                text=texto[col],
                borderwidth=2,
                relief="groove",
                width=width,
                background="#5a98c4",
                fg="white"
                )
            label.grid(row=1, column=col,ipady=5)
            col+=1

            if col==1 or col==7:
                width=10
            elif 2<=col<=4:
                width=12
            elif 5>=col<=6:
                width=15
        
        if len(resultado) > 15:

            # aparece scroll si registros > 15

            scroll = tk.Scrollbar(frame4)
            c=tk.Canvas(frame3,yscrollcommand=scroll.set,bg="white")
            scroll.config(command=c.yview)
            scroll.grid(sticky="e",column=8,row=1,ipady=270)
            linea= tk.Frame(frame3)
            linea.grid(sticky="nse",column=9,row=1)
            contenedor = tk.Frame(c)
            contenedor.grid(row=2,pady=0)

            c.create_window(0,0,window=contenedor,anchor="nw")
            c.grid(sticky="nsew",row=2,column=0)

        else:

            contenedor = tk.Frame(frame3)
            contenedor.grid(row=2)

        frame3.rowconfigure(2,weight=32)
                          

        
        widgets2 = {}
        row=0
        for num, doc, nom, ape, ape_d, marc, model, matri in resultado:
            row += 1
            widgets2[num] ={
            "Cliente Nº": tk.Label(contenedor, text=num,borderwidth=2,relief="groove",width=10),
            "Documento": tk.Label(contenedor, text=doc,borderwidth=2,relief="groove",width=10),
            "Nombre": tk.Label(contenedor, text=nom,borderwidth=2,relief="groove",width=12),
            "1er Apellido": tk.Label(contenedor, text=ape,borderwidth=2,relief="groove",width=12),
            "2do Apellido": tk.Label(contenedor, text=ape_d,borderwidth=2,relief="groove",width=12),
            "Marca": tk.Label(contenedor, text=marc,borderwidth=2,relief="groove",width=15),
            "Modelo": tk.Label(contenedor, text=model,borderwidth=2,relief="groove",width=15),
            "Matricula": tk.Label(contenedor, text=matri,borderwidth=2,relief="groove",width=10),
            }

            widgets2[num]["Cliente Nº"].grid(row=row, column=0, sticky="nsew",ipady=5)
            widgets2[num]["Documento"].grid(row=row, column=1, sticky="nsew",ipady=5) 
            widgets2[num]["Nombre"].grid(row=row, column=2, sticky="nsew",ipady=5)
            widgets2[num]["1er Apellido"].grid(row=row, column=3, sticky="nsew",ipady=5) 
            widgets2[num]["2do Apellido"].grid(row=row, column=4, sticky="nsew",ipady=5) 
            widgets2[num]["Marca"].grid(row=row, column=5, sticky="nsew",ipady=5) 
            widgets2[num]["Modelo"].grid(row=row, column=6, sticky="nsew",ipady=5) 
            widgets2[num]["Matricula"].grid(row=row, column=7, sticky="nsew",ipady=5) 

        if len(resultado) > 15:

            frame3.update()
            c.config(scrollregion=c.bbox("all"))



#-----------------formulario al presionar el botón de añadir vehiculo-------------------    

def formulario_vehiculo(
    miBase,
    el_entry,
    var_marca,
    var_modelo,
    var_matricula,
    escoba,
    mas,
    app
    ):

    try:

        miCursor = miBase.cursor()
        consulta="SELECT * FROM datos_usuarios2 where documento=%s"
        miCursor.execute(
            consulta,
            el_entry.get()
            )
        resultado = miCursor.fetchone()
        

 #-Si hay un resultado se abrira la ventana del formulario y apareceran los datos del cliente   
        
        if resultado:


            ventana_vehiculo=tk.Toplevel()
            ventana_vehiculo.resizable(0,0)
            ventana_vehiculo.transient(app)
            ventana_vehiculo.title("Vehículo")
            posicionar(ventana_vehiculo)
            
        
           
            
            label_title=tk.Label(
                ventana_vehiculo,
                bg="black",
                fg="white",
                text="Añadir Vehículo"
                )
            label_title.grid(row=0,column=0,ipady=3,sticky="nsew")

            var_cliente=tk.StringVar()

            frame_datos=tk.Frame(ventana_vehiculo)
            frame_datos.grid(
                row=1,
                column=0,
                sticky="nsew"
                )

            label_name=tk.Label(
                frame_datos,
                textvariable=var_cliente
                )
            label_name.grid(
                row=0,
                padx=10,
                pady=5,
                sticky="nsew"
                )
            

            
            var_cliente.set(
                "Cliente Nº {}   {} {} {}   Documento Nº {}".format(
                    resultado[0],
                    resultado[4],
                    resultado[5],
                    resultado[6],
                    resultado[2]
                    )
                )

            frame_form=tk.Frame(ventana_vehiculo,bd=2,relief="groove")
            frame_form.grid(row=2,column=0,sticky="nsew")

            labels=["Marca:","Modelo:","Matrícula:"]
            var_marca=tk.StringVar()
            var_modelo=tk.StringVar()
            var_matricula=tk.StringVar()
            textvars=[var_marca,var_modelo,var_matricula]
            n=0
            w=30
            for l in labels:

                label=tk.Label(frame_form,text=labels[n])
                label.grid(row=n,column=0,sticky="e",padx=20,pady=20)
                entry=tk.Entry(frame_form,
                width=w,textvariable=textvars[n])
                entry.grid(row=n,column=1,sticky="w",padx=20,pady=20)
                n += 1
                if n ==2:
                    w=20


            frame_form2=tk.Frame(ventana_vehiculo,bg="#5a98c4")
            frame_form2.grid(row=3,column=0,sticky="nsew")
            frame_form3=tk.Frame(frame_form2,bg="#5a98c4")
            frame_form3.grid(row=3,column=0,sticky="e",padx=(240,0))

            imagenes=[escoba,mas]
            text=[" Limpiar"," Crear"]
            func=(
                lambda:reset_formulario(
                    var_marca,
                    var_modelo,
                    var_matricula
                    ),
                lambda:agregar_vehiculo(
                    miBase,
                    var_marca,
                    var_modelo,
                    var_matricula,
                    el_entry,
                    ventana_vehiculo
                    )

                )

            n=0
            for t in text:
            
                boton=tk.Button(
                    frame_form3,
                    image=imagenes[n],
                    command=func[n],
                    cursor="hand2",
                    relief="flat",
                    bg="#5a98c4",
                    fg="white",
                    activebackground="black",
                    activeforeground="white",
                    text=text[n],
                    font=("verdana",12,"bold"),
                    compound="left"
                    )
                boton.grid(row=0,pady=5,padx=10,column=n)
                n+=1

                

        else:
            messagebox.showinfo("Atención","Ingrese un número válido")
            el_entry.set("")


    finally:

        miBase.commit()
        miCursor.close()

#-----------limpiar formulario-----------

def reset_formulario(var_marca,var_modelo,var_matricula):



    var_marca.set("")
    var_modelo.set("")
    var_matricula.set("")

#----------------------agregar vehiculo------------------------

def agregar_vehiculo(miBase,var_marca,var_modelo,
    var_matricula,var_entry_id,ventana_vehiculo):

    if var_marca.get()!="" and var_modelo.get()!="" and var_matricula.get()!="":

        try:
            miCursor = miBase.cursor()
            miCursor.execute("SELECT id_cliente from datos_usuarios2 where documento=%s",var_entry_id.get())
            cliente=miCursor.fetchone()

            consulta="INSERT INTO vehiculos (cliente_n,marca,modelo,matricula) values(%s,%s,%s,%s)"
            miCursor.execute(
                consulta,(
                    cliente[0],
                    var_marca.get(),
                    var_modelo.get(),
                    var_matricula.get()
                    )
                )
            messagebox.showinfo(
                "Información",
                "Se ha vinculado el vehículo {} {}\nMatrícula: {} al cliente con el documento: {}".format(
                    var_marca.get(),
                    var_modelo.get(),
                    var_matricula.get(),
                    var_entry_id.get()
                    )
                )
            var_entry_id.set("")
            ventana_vehiculo.destroy()


        except pymysql.err.DataError:

            messagebox.showinfo(
                "Atención",
                "Ingrese los datos correctamente\nVerifique la matrícula"
                )
            

        finally:

            miBase.commit()
            miCursor.close()


    else:
        messagebox.showinfo("Atención","Ingrese los datos del vehículo")



