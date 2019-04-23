import sys
sys.path.insert(1,"../conexion")
import conexion
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import pymysql
from belfrywidgets import ToolTip
sys.path.insert(1,"../panel")
import funcionalidades
import re


verDiaMesAnio=funcionalidades.verDiaMesAnio
guardaAnioMesDia=funcionalidades.guardaAnioMesDia
posicionar=funcionalidades.posicionar
desactivar=funcionalidades.desactivar
activar=funcionalidades.activar
Conexion=conexion.Conexion

class FormularioCliente(Conexion,tk.Frame):

    #clase de panel de cliente

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.var_ingreso=tk.StringVar()
        self.var_doc = tk.StringVar()
        self.var_nac = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_apellido = tk.StringVar()
        self.var_ape_dos = tk.StringVar()
        self.var_tel = tk.StringVar()
        self.var_dire = tk.StringVar()
        self.var_correo = tk.StringVar()
        self.var_genero = tk.IntVar()

        self.formulario()



    def formulario(self):

        tit=tk.Label(
            self,
            text="Formulario de clientes",
            bg="black",
            fg="white"
            )
        tit.grid(row=0,column=0,columnspan=4,sticky="nsew")

        frameingreso=tk.Frame(self,bd=1,relief="sunken")
        frameingreso.grid(row=1,column=0,sticky="nsew",ipady=30)

        frameingreso2=tk.Frame(self)
        frameingreso2.grid(row=1,column=0)


        labelingreso=tk.Label(frameingreso2,text="Fecha de ingreso:")
        labelingreso.grid(row=1,column=1,padx=10,pady=10,sticky="e")

        entryIng=tk.Entry(frameingreso2,textvariable=self.var_ingreso,width=12)
        entryIng.grid(row=1,column=2,pady=10,sticky="w")

        frameForm=tk.Frame(self)
        frameForm.grid(row=2,column=0,sticky="nsew",pady=20)

        texto=["Documento:","Fecha de nacimiento:","Nombre:","1er Apellido:"]
        textvars=[self.var_doc,self.var_nac,self.var_nombre,self.var_apellido]
        n=0
        w=12
        for t in texto:

            label = tk.Label(frameForm,text=texto[n])
            label.grid(row=n,column=0,sticky="e",padx=10,pady=10)
            entry = tk.Entry(frameForm,width=w,textvariable=textvars[n])
            entry.grid(row=n,column=1,padx=10,pady=10,sticky="w")
            n += 1

            if n==5:
                w=12
            elif 1<=n<=4:
                w=20
            elif n == 6:
                w=28

        texto2=["2do Apellido","Teléfono:","Domicilio:","Correo:"]
        textvars2=[self.var_ape_dos,self.var_tel,self.var_dire,self.var_correo]
        w=12
        n=0
        for t in texto2:

            label = tk.Label(frameForm,text=texto2[n])
            label.grid(row=n,column=2,sticky="e",padx=10,pady=10)
            entry = tk.Entry(frameForm,width=w,textvariable=textvars2[n])
            entry.grid(row=n,column=3,padx=10,pady=10,sticky="w")
            n += 1

            if 1 <= n <= 2:
                w=30

        frameGenero=tk.Frame(self,bd=1,relief="sunken",height=55)
        frameGenero.grid(row=3,column=0,sticky="nsew")

        frameGenero2=tk.Frame(self)
        frameGenero2.grid(row=3,column=0)

        fem=tk.Radiobutton(frameGenero2, text="Femenino", variable=self.var_genero, value=1)
        fem.grid(row=0,column=0,padx=10)

        masc=tk.Radiobutton(frameGenero2, text="Masculino", variable=self.var_genero, value=2)
        masc.grid(row=0,column=1,padx=10)

        textobotones=[" Limpiar", " Crear"]

        funciones=(
            lambda:self.limpiar(),
            lambda:self.crear()
            )

        img=(self.escoba,self.mas)

        

        frameBotones=tk.Frame(self,bg="#5a98c4")
        frameBotones.grid(row=4,column=0,sticky="nsew",ipady=30)

        botones=tk.Frame(self,bg="#5a98c4")
        botones.grid(row=4,column=0,pady=(15,0))
        
            
        n=0
        for t in textobotones:
            boton=tk.Button(
                botones,
                image=img[n],
                command=funciones[n],
                cursor="hand2",
                relief="flat",
                bg="#5a98c4",
                fg="white",
                activebackground="black",
                activeforeground="white",
                text=textobotones[n],
                font=self.bold,
                compound="left"
                )
            boton.grid(row=3,column=n,padx=10)
            n+=1



    def limpiar(self):

    
        self.var_ingreso.set("")
        self.var_doc.set("")
        self.var_nac.set("")
        self.var_nombre.set("")
        self.var_apellido.set("")
        self.var_ape_dos.set("")
        self.var_tel.set("")
        self.var_dire.set("")
        self.var_correo.set("")
        self.var_genero.set(0)

    def crear(self):

        if self.var_doc.get() and self.var_nombre.get() and self.var_apellido.get() and self.var_nac.get() and self.var_tel.get() and self.es_correo_valido(self.var_correo.get()):

            try:
                self.miCursor = self.miBase.cursor()
                self.miCursor2 = self.miBase2.cursor()
                guarda_fecha=tk.StringVar()
                guarda_fecha2=tk.StringVar()

                if self.var_ingreso.get():
                    guardaAnioMesDia(self.var_ingreso.get(),guarda_fecha)
                    
                else:
                    dt= datetime.datetime.now()
                    actual=dt.strftime("%Y-%m-%d")
                    guarda_fecha.set(actual)
                    
                    
                if self.var_nac.get():
                    
                    guardaAnioMesDia(self.var_nac.get(),guarda_fecha2)

                    
                
                consulta= "INSERT INTO datos_usuarios2 (ingreso,documento,nacimiento,nombre,apellido,apellido_dos,telefono,direccion,correo,foto) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                self.miCursor.execute(
                    consulta,
                    (
                        guarda_fecha.get(),
                        self.var_doc.get(),
                        guarda_fecha2.get(),
                        self.var_nombre.get(),
                        self.var_apellido.get(),
                        self.var_ape_dos.get(),
                        self.var_tel.get(),
                        self.var_dire.get(),
                        self.var_correo.get(),
                        self.var_genero.get()
                        )
                    )
                self.miBase.commit()
                
                self.miCursor.execute(
                    "SELECT id_cliente,nombre,apellido,documento FROM datos_usuarios2 where documento = %s",
                    self.var_doc.get()
                    )
                
                resultado = self.miCursor.fetchone()

                messagebox.showinfo(
                    "Creación de cliente",
                    "Nuevo cliente nº {}\n{} {}\nDocumento: {}".format(
                        resultado[0],
                        resultado[1],
                        resultado[2],
                        resultado[3]
                        )
                    )

                # insercion del cliente en la base taller si no existe ya

                self.miCursor2.execute(
                    "SELECT id from bases where nombre=%s",self.empresa)
                base=self.miCursor2.fetchone()

                self.miCursor2.execute(
                    "SELECT bases FROM clientes where email = %s",
                    self.var_correo.get()
                    )
                bases = self.miCursor2.fetchone()

                if bases==None:

                    primerEmpresa = "{},".format(base[0])

                    
                    inserta="INSERT INTO clientes (email,bases,id_cliente) values (%s,%s,%s)"

                    self.miCursor2.execute(
                        inserta,
                        (
                            self.var_correo.get(),
                            primerEmpresa,
                            "{},".format(resultado[0])
                        )
                    )

                else:

                    # si existe se le agrega la empresa y su correspondiente numero de cliente en ella

                    self.miCursor2.execute(
                        "SELECT bases from clientes where email = %s",
                        var_correo.get()
                        )

                    talleres=self.miCursor2.fetchone()

                    lista=talleres.split(",")
            
                    if base not in lista:

                        lista.append(base[0])
                        cadena=(",").join(lista)

                        miCursor2.execute(
                            "UPDATE clientes set talleres=(%s)",
                            cadena
                            )

                self.limpiar()

            
            except pymysql.err.IntegrityError:
                messagebox.showinfo(
                    "Error",
                    "Intenta duplicar datos únicos ya existentes"
                    )

            except pymysql.err.InternalError:
                messagebox.showinfo(
                    "Atención",
                    "Datos incorrectos o incompletos, verifique"
                    )

            except IndexError:
                messagebox.showinfo(
                    "Atención",
                    "Verificar datos\nFormato de fecha DD/MM/AAAA"
                    )

            finally:

                self.miBase.commit()
                self.miBase2.commit()
                self.miCursor.close()
                self.miCursor2.close()

        else:
            messagebox.showinfo("Atención","Verificar datos")


    def es_correo_valido(self,correo):
        expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        return re.match(expresion_regular, correo.lower()) is not None


    """
    

    def buscarId(self):

        if self.var_id.get():

            try:

                self.miCursor=self.miBase.cursor()

                self.miCursor.execute(
                    "SELECT * FROM datos_usuarios2 where id_cliente = %s",
                    self.var_id.get()
                    )
                resultado = self.miCursor.fetchone()

                if resultado[1]:
                    verDiaMesAnio(resultado[1],self.var_ingreso)
                else:
                    self.var_ingreso.set("")

                if resultado[3]:
                    verDiaMesAnio(resultado[3],self.var_nac)
                else:
                    self.var_nac.set("")


                self.var_id.set(resultado[0])
                self.entryId.config(state="readonly")
                self.var_doc.set(resultado[2])
                self.var_nombre.set(resultado[4])
                self.var_apellido.set(resultado[5])
                self.var_ape_dos.set(resultado[6])
                self.var_tel.set(resultado[7])
                self.var_dire.set(resultado[8])
                self.var_correo.set(resultado[9])

            except:

                messagebox.showinfo("Aviso","Cliente no encontrado")

            finally:
        
                self.miCursor.close()

    def buscarDoc(self):

        if self.var_doc.get():

            try:

                self.miCursor=self.miBase.cursor()

                self.miCursor.execute(
                    "SELECT * FROM datos_usuarios2 where documento = %s",
                    self.var_doc.get()
                    )
                resultado = self.miCursor.fetchone()

                if resultado[1]:
                    verDiaMesAnio(resultado[1],self.var_ingreso)
                else:
                    self.var_ingreso.set("")

                if resultado[3]:
                    verDiaMesAnio(resultado[3],self.var_nac)
                else:
                    self.var_nac.set("")


                self.var_id.set(resultado[0])
                self.entryId.config(state="readonly")
                self.var_doc.set(resultado[2])
                self.var_nombre.set(resultado[4])
                self.var_apellido.set(resultado[5])
                self.var_ape_dos.set(resultado[6])
                self.var_tel.set(resultado[7])
                self.var_dire.set(resultado[8])
                self.var_correo.set(resultado[9])

            except:

                messagebox.showinfo("Aviso","Cliente no encontrado")

            finally:
        
                self.miCursor.close()


    """

                

    

            

