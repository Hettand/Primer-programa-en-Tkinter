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
sys.path.insert(2,"../panel")
import funcionalidades
import design

Conexion=conexion.Conexion
adaptable=funcionalidades.adaptable
verDiaMesAnio=funcionalidades.verDiaMesAnio
guardaAnioMesDia=funcionalidades.guardaAnioMesDia
siHayFrame=funcionalidades.siHayFrame
agregaFrame=funcionalidades.agregaFrame
cerrarFrame=funcionalidades.cerrarFrame
desactivar=funcionalidades.desactivar
activar=funcionalidades.activar
posicionar=funcionalidades.posicionar
cerrarToplevel=funcionalidades.cerrarToplevel
configuraToplevel=funcionalidades.configuraToplevel
botonNegro=design.botonNegro

class Ficha(Conexion,ttk.Frame):



    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        dt= datetime.datetime.now()
        self.actual=dt.strftime("%Y-%m-%d")

        self.var_marca=tk.StringVar()
        self.var_modelo=tk.StringVar()
        self.var_matricula=tk.StringVar()

        self.numMatricula=tk.StringVar()
        

    def ver_ficha(self,frameGrande,resultado,lista):

        siHayFrame(lista)

        self.frameDinamico=tk.Frame(frameGrande,bg="")
        self.frameDinamico.grid(row=0,column=0,sticky="nsew")
        frameGrande.rowconfigure(0,weight=4)
        frameGrande.columnconfigure(0,weight=4)
        agregaFrame(self.frameDinamico,lista)

        #mostrar los datos encontrados
        frame_ficha=tk.Frame(self.frameDinamico)
        frame_ficha.grid(row=0,column=0,sticky="nsew")
        self.frameDinamico.rowconfigure(0, weight=4)

        frameLinea=tk.Frame(self.frameDinamico,bg="#000",width=2)
        frameLinea.grid(row=0,column=1,sticky="ns")

        frame2_ficha=tk.Frame(frame_ficha,background="black")
        frame2_ficha.grid(row=0,column=0,sticky="nsew")
        datos_label=tk.Label(frame_ficha,text="Ficha del cliente N°{}".format(resultado[0]),background="black",fg="white")
        datos_label.grid(row=0,column=0)
        self.editarBoton=tk.Button(
            frame_ficha,
            image=self.editar,
            cursor="hand2",
            relief="flat",
            activebackground="#fff",
            bg="#000",
            command=lambda:self.editarDatos(frameGrande,resultado,lista)
            )
        self.editarBoton.grid(row=0,column=0,sticky="e",padx=5)
        ToolTip(self.editarBoton,"Editar datos")

        frame3_ficha=tk.Frame(frame_ficha)
        frame3_ficha.grid(row=2,column=0,sticky="nsew")

        frameFoto=tk.Frame(frame3_ficha,bg="#000")
        frameFoto.grid(row=0,column=0)

        if resultado[11] == 0:
            foto=self.none
        elif resultado[11] == 1:
            foto=self.femenino
        elif resultado[11] == 2:
            foto=self.masculino

        labelFoto=tk.Label(frameFoto,image=foto,bg="black")
        labelFoto.grid(row=0,column=0,pady=10,padx=20)
        labelnombre=tk.Label(
            frameFoto,
            text="{}\n{}\n{}".format(resultado[4],resultado[5],resultado[6]),
            fg="#fff",
            bg="#000"
            )
        labelnombre.grid(row=1, column=0,ipady=10)


        ing=tk.StringVar()
        verDiaMesAnio(resultado[1],ing)
        nac=tk.StringVar()
        verDiaMesAnio(resultado[3],nac)

        labels=["Ingreso:","Documento:","Nacimiento:","Teléfono:","Dirección:","Correo:"]
        results=[ing.get(),resultado[2],nac.get(),resultado[7],resultado[8],resultado[9]]

        frameDatos=tk.Frame(frame3_ficha)
        frameDatos.grid(row=0,column=1)

        n=0
        for l in labels:

            label=tk.Label(frameDatos,text=labels[n])
            label.grid(row=n,column=0,sticky="w",padx=10)
            label2=tk.Label(frameDatos,text=results[n],font=self.bold)
            label2.grid(row=n,column=1,sticky="w",padx=10)

            n += 1

        try:

            self.miCursor = self.miBase.cursor()
            consulta2="SELECT marca,modelo,matricula FROM vehiculos where (cliente_n=%s) and (estado=%s)"
            self.miCursor.execute(
                consulta2,(resultado[0],1)
                )
            vehiculos=self.miCursor.fetchall()

            cantidad=len(vehiculos)

            frame4_ficha=tk.Frame(frame_ficha,bg="#000")
            frame4_ficha.grid(row=3,column=0,sticky="nsew",columnspan=2)
            
            titulo=tk.Label(frame_ficha,text="Vehículos: {}".format(cantidad), bg="black", fg="white")
            titulo.grid(row=3,column=0)

            self.sacarVehiculo="",
            self.agregarVehiculo="",
            self.editarVehiculo="",
            
            botones=[
                self.sacarVehiculo,self.agregarVehiculo,self.editarVehiculo
                ]
            
            text=["Desvincular vehículo","Agregar vehículo","Editar vehículo seleccionado"]
            
            imagenes=(
                self.romper,self.maschico,self.editar
                )
            func=(
                lambda:self.desvinculaVehiculo(frameGrande,resultado,lista),
                lambda:self.agregaEditaVehiculo(frameGrande,resultado,lista,"Agregar"),
                lambda:self.EditaVehiculo(frameGrande,resultado,lista)
                )

            e=0
            x=80
            for d in botones:

                botones[e]=botonNegro(botones[e],frame_ficha,imagenes[e])
                botones[e].grid(row=3,column=0,sticky="e",padx=(5,x))
                botones[e].config(command=func[e])
                ToolTip(botones[e],text[e])
                e += 1
                if e == 1:
                    x=40
                else:
                    x=5


            

            if vehiculos:

              
                frameV=tk.Frame(frame_ficha)
                frameV.grid(row=4,column=0,sticky="nsew",columnspan=2)

                n=0
                for v in vehiculos:

                    numeroM = "{}".format(vehiculos[n][2])

                    label3=tk.Label(
                        frameV,
                        text=" {} {} - {}".format(vehiculos[n][0],vehiculos[n][1],vehiculos[n][2]),
                        image=self.item,
                        compound="left",
                        bd=1,
                        relief="sunken",
                        anchor="w",
                        font=self.bold
                        )

                    self.numMatricula.set(0)

                    label3.grid(row=n,column=0,sticky="nsew")
                    radio=tk.Radiobutton(frameV,variable=self.numMatricula, value=numeroM)
                    radio.grid(row=n,column=0,padx=10,sticky="e")
                    n += 1
                frameV.columnconfigure(0, weight=2)
                   
        finally:

            self.miCursor.close()


    def editarDatos(self,frameGrande,resultado,lista):

        desactivar(self.editarBoton)

        formEditar=tk.Toplevel(self.frameDinamico)

        configuraToplevel(formEditar,lista,self.frameDinamico,"Editar datos")
        formEditar.protocol(
                "WM_DELETE_WINDOW",
                lambda:cerrarToplevel(self.editarBoton,lista,formEditar)
                )

        # pasar al formulario los datos para editar

        frametitulo=tk.Frame(formEditar,bg="#000")
        frametitulo.grid(row=0,column=0,sticky="nsew")

        titulolabel=tk.Label(formEditar,text="Editar datos",bg="#000",fg="#fff")
        titulolabel.grid(row=0,column=0)

        self.ing=tk.StringVar()
        verDiaMesAnio(resultado[1],self.ing)
        self.nac=tk.StringVar()
        verDiaMesAnio(resultado[3],self.nac)

        self.nom=tk.StringVar()
        self.ape=tk.StringVar()
        self.apeDos=tk.StringVar()
        self.doc=tk.StringVar()
        self.tel=tk.StringVar()
        self.dire=tk.StringVar()
        self.cor=tk.StringVar()
        self.genero=tk.IntVar()

        listaVars=(self.ing,self.doc,self.nac,self.nom,self.ape,self.apeDos,self.tel,self.dire,self.cor)


        labels=["Ingreso:","Documento:","Nacimiento:","Nombre","1er Apellido","2do Apellido","Teléfono:","Domicilio:","Correo:"]
        results=[self.ing.get(),resultado[2],self.nac.get(),resultado[4],resultado[5],resultado[6],resultado[7],resultado[8],resultado[9]]


        n=0
        for v in listaVars:

            listaVars[n].set(results[n])

            n += 1
        
        frameForm=tk.Frame(formEditar)
        frameForm.grid(row=1,column=0,sticky="nsew") 

        n=0
        for l in labels:

            label=tk.Label(frameForm,text=labels[n])
            label.grid(row=n,column=0,sticky="e",padx=(25,10),pady=10)
            entry=tk.Entry(frameForm,textvariable=listaVars[n],width=30)
            entry.grid(row=n,column=1,sticky="w",padx=(10,25))

            n += 1

        frameGenero=tk.Frame(formEditar,bd=1,relief="sunken",height=55)
        frameGenero.grid(row=2,column=0,sticky="nsew")

        frameGenero2=tk.Frame(formEditar)
        frameGenero2.grid(row=2,column=0)

        fem=tk.Radiobutton(frameGenero2, text="Femenino", variable=self.genero, value=1)
        fem.grid(row=0,column=0,padx=10)

        masc=tk.Radiobutton(frameGenero2, text="Masculino", variable=self.genero, value=2)
        masc.grid(row=0,column=1,padx=10)

        self.genero.set(resultado[11])

        otroFrame=tk.Frame(formEditar,bg="#5a98c4")
        otroFrame.grid(column=0,row=3,sticky="nsew")


        boton=tk.Button(
                formEditar,
                image=self.actualiza,
                command=lambda:self.actualizarDatos(frameGrande,resultado,lista),
                cursor="hand2",
                relief="flat",
                bg="#5a98c4",
                fg="white",
                activebackground="black",
                activeforeground="white",
                text=" Actualizar",
                font=self.bold,
                compound="left"
                )
        boton.grid(row=3,column=0,pady=5)



    def actualizarDatos(self,frameGrande,resultado,lista):



        #en caso que haya fechas ingresadas las damos vuelta para guardarlas--
        if self.nac!="":
            guarda_nac=tk.StringVar()
            guardaAnioMesDia(self.nac.get(),guarda_nac)

        if self.ing!="" and self.doc!="" and self.nom!="" and  self.ape!="" and self.tel!="":


            guarda_ing=tk.StringVar()
            guardaAnioMesDia(self.ing.get(),guarda_ing)

            try:


                self.miCursor = self.miBase.cursor()
                consulta = "UPDATE datos_usuarios2 set ingreso=(%s), documento=(%s), nacimiento=(%s), nombre=(%s) ,apellido=(%s),apellido_dos=(%s), telefono=(%s) ,direccion=(%s),correo=(%s), foto=(%s) where id_cliente=(%s)"
                self.miCursor.execute(
                    consulta,
                    [guarda_ing.get(), self.doc.get(), guarda_nac.get(), self.nom.get(), self.ape.get(), self.apeDos.get(), self.tel.get(), self.dire.get(), self.cor.get(), self.genero.get(), resultado[0]]
                    )
                self.miBase.commit()

                self.miCursor.execute(
                    "SELECT * from datos_usuarios2 where id_cliente=%s",resultado[0])
                resultadoActualizado=self.miCursor.fetchone()
                
                self.ver_ficha(frameGrande,resultadoActualizado,lista)                

            except TypeError:

                messagebox.showinfo(
                    "Atención",
                    "No es posible actualizar\nVerifique los datos"
                    )

            except pymysql.err.InternalError:

                messagebox.showinfo(
                    "Atención",
                    "No es posible actualizar\nVerifique los datos"
                    )

            except pymysql.err.IntegrityError:

                messagebox.showinfo(
                    "Atención",
                    "Los datos documento y correo\ndeben ser exclusivos de cada cliente"
                    )

            except IndexError:

                messagebox.showinfo(
                    "Atención",
                    "Verifique el formato de las fechas")


            finally:
                
                self.miCursor.close()
                
        else:

            messagebox.showinfo(
                "Atención",
                "Faltan datos"
                )


    def agregaEditaVehiculo(self,frameGrande,resultado,lista,accion):


        formulario=tk.Toplevel(self.frameDinamico)

        configuraToplevel(formulario,lista,self.frameDinamico,"Vehículo")

        frametitulo=tk.Frame(formulario,bg="#000")
        frametitulo.grid(row=0,column=0,sticky="nsew")

        titulolabel=tk.Label(formulario,text="{} vehículo".format(accion),bg="#000",fg="#fff")
        titulolabel.grid(row=0,column=0)

        frame_form=tk.Frame(formulario)
        frame_form.grid(row=1,column=0,sticky="nsew")

        labels=["Marca:","Modelo:","Matrícula:"]
        
        textvars=[self.var_marca,self.var_modelo,self.var_matricula]
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
                w=12

        buscaBajas=tk.Button(
            frame_form,
            image=self.lupa,
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            command=lambda:self.buscarBajas()
            )
        buscaBajas.grid(row=2,column=1)
        ToolTip(buscaBajas,"Buscar vehículos desvinculados")

        frameBotones=tk.Frame(formulario,height=30,bg="#5a98c4")
        frameBotones.grid(row=2,column=0,sticky="nsew")

        frameBotones2=tk.Frame(formulario,bg="#5a98c4")
        frameBotones2.grid(row=2,column=0)

        if accion == "Agregar":

            desactivar(self.agregarVehiculo)

            formulario.protocol(
                "WM_DELETE_WINDOW",
                lambda:cerrarToplevel(self.agregarVehiculo,lista,formulario)
                )

            text=[" Limpiar"," Vincular"]
            imagenes=(self.escoba,self.mas)
            func=(lambda:self.limpiar(),lambda:self.crear(resultado,frameGrande,lista))

            n=0
            for t in text:
            
                boton=tk.Button(
                    frameBotones2,
                    image=imagenes[n],
                    command=func[n],
                    cursor="hand2",
                    relief="flat",
                    bg="#5a98c4",
                    fg="white",
                    activebackground="black",
                    activeforeground="white",
                    text=text[n],
                    font=self.bold,
                    compound="left"
                    )
                boton.grid(row=0,column=n,pady=5,padx=10)
                n+=1


        elif accion == "Editar":

            desactivar(self.editarVehiculo)

            formulario.protocol(
                "WM_DELETE_WINDOW",
                lambda:cerrarToplevel(self.editarVehiculo,lista,formulario)
                )


            try:
                self.miCursor = self.miBase.cursor()

                self.miCursor.execute("SELECT id_vehiculo,marca, modelo, matricula from vehiculos where matricula=%s",self.numMatricula.get())
                vehiculo = self.miCursor.fetchone()

                if vehiculo:

                    self.var_marca.set(vehiculo[1])
                    self.var_modelo.set(vehiculo[2])
                    self.var_matricula.set(vehiculo[3])

            finally:

                self.miCursor.close()

            boton=tk.Button(
                frameBotones2,
                image=self.actualiza,
                command=lambda:self.actualizaVehiculo(vehiculo[0],frameGrande,resultado,lista),
                cursor="hand2",
                relief="flat",
                bg="#5a98c4",
                fg="white",
                activebackground="black",
                activeforeground="white",
                text=" Actualizar",
                font=self.bold,
                compound="left"
                )
            boton.grid(row=0,column=n,pady=5,padx=10)


    def buscarBajas(self):

        if self.var_matricula.get():

            try:
                self.miCursor=self.miBase.cursor()
                self.miCursor.execute("SELECT marca,modelo,matricula from vehiculos where (matricula=%s) and (estado=%s)",(self.var_matricula.get(),0))
                vehiculo=self.miCursor.fetchone()

                if vehiculo:
                    self.var_marca.set(vehiculo[0])
                    self.var_modelo.set(vehiculo[1])
                    self.var_matricula.set(vehiculo[2])



                else:
                    messagebox.showinfo("Aviso","Vehículo no encontrado")
                    self.limpiar()

            except:
                messagebox.showinfo("Aviso","Vehículo no encontrado")

            finally:
                self.miCursor.close()

        else:
            messagebox.showinfo("Atención","Ingrese una matricula")
       
    def limpiar(self):

        self.var_marca.set("")
        self.var_modelo.set("")
        self.var_matricula.set("")


    def crear(self,resultado,frameGrande,lista):

        if self.var_marca.get() and self.var_modelo.get() and self.var_matricula.get():

            try:

                self.miCursor=self.miBase.cursor()
                insertar="INSERT INTO vehiculos (cliente_n,marca,modelo,matricula) values(%s,%s,%s,%s)"

                self.miCursor.execute(
                    insertar,
                    (resultado[0],self.var_marca.get(),self.var_modelo.get(),self.var_matricula.get())
                    )
                self.miBase.commit()

                self.miCursor.execute("SELECT id_vehiculo from vehiculos where matricula=%s",self.var_matricula.get())
                numero=self.miCursor.fetchone()

                insertar2="INSERT INTO alta_baja_vehiculos (fecha,accion,id_vehiculo,marca,modelo,matricula,id_cliente,documento) values (%s,%s,%s,%s,%s,%s,%s,%s)"
                self.miCursor.execute(
                    insertar2,
                    (self.actual,1,numero[0],self.var_marca.get(),self.var_modelo.get(),self.var_matricula.get(),resultado[0],resultado[2]))
                self.miBase.commit()

                self.miCursor.execute(
                    "SELECT * from datos_usuarios2 where id_cliente=%s",resultado[0])
                resultadoActualizado=self.miCursor.fetchone()
                
                self.ver_ficha(frameGrande,resultadoActualizado,lista)

            except pymysql.err.IntegrityError:

                self.vinculaVehiculo(frameGrande,resultado,lista)

            except:
                messagebox.showinfo("Atención","No se ha podido vincular el vehículo")

            finally:
                self.miCursor.close()

        else:
            messagebox.showinfo("Aviso","Faltan datos")


    def vinculaVehiculo(self,frameGrande,resultado,lista):

        try:
            self.miCursor=self.miBase.cursor()

            cambia="UPDATE vehiculos set estado=(%s) where (marca=%s) and (modelo=%s) and (matricula=%s) and (estado=%s)"
            self.miCursor.execute(
                cambia,
                (
                    1,
                    self.var_marca.get(),
                    self.var_modelo.get(),
                    self.var_matricula.get(),
                    0)
                )

            self.miCursor.execute("SELECT id_vehiculo from vehiculos where matricula=%s",self.var_matricula.get())
            numero=self.miCursor.fetchone()

            insertar2="INSERT INTO alta_baja_vehiculos (fecha,accion,id_vehiculo,marca,modelo,matricula,id_cliente,documento) values (%s,%s,%s,%s,%s,%s,%s,%s)"
            self.miCursor.execute(
                insertar2,
                (self.actual,1,numero[0],self.var_marca.get(),self.var_modelo.get(),self.var_matricula.get(),resultado[0],resultado[2]))
            self.miBase.commit()

            self.miCursor.execute(
                    "SELECT * from datos_usuarios2 where id_cliente=%s",resultado[0])
            resultadoActualizado=self.miCursor.fetchone()

            messagebox.showinfo("Vincular","Vínculo exitoso")
            
            self.ver_ficha(frameGrande,resultadoActualizado,lista)
            self.limpiar()

        except:
            messagebox.showinfo("Atención","No se ha vinculado el vehículo")

        finally:
            self.miCursor.close()




    def EditaVehiculo(self,frameGrande,resultado,lista):

        if len(self.numMatricula.get()) >= 6:

            self.agregaEditaVehiculo(frameGrande,resultado,lista,"Editar")

        else:
            messagebox.showinfo("Atención","Seleccione un vehículo")

                
    
    def desvinculaVehiculo(self,frameGrande,resultado,lista):

        if len(self.numMatricula.get()) >= 6:

            try:
                self.miCursor=self.miBase.cursor()
                self.miCursor.execute("SELECT id_vehiculo,marca,modelo,matricula from vehiculos where matricula=%s",self.numMatricula.get())
                ide=self.miCursor.fetchone()

                # si hay trabajos sin despachar no permite desvincular vehiculo del cliente

                self.miCursor.execute("SELECT id_trabajo from trabajos where (id_vehiculo=%s) and (estado!=%s)",
                    (ide[0],"Despachado"))
                sinDespachar=self.miCursor.fetchall()

                if sinDespachar:

                    lista2=[]
                    n=0
                    for s in sinDespachar:
                        lista2.append("Trabajo N°{}".format(sinDespachar[n]))
                        n += 1
                    texto=lista2.split("\n")

                    messagebox.showerror("Error","Acción no permitida vehículo sin despachar:\n{}".format(texto))

                else:

                    pregunta=messagebox.askyesno("Desvincular vehículo","¿Desea desvincular el vehiculo a este cliente?")

                    if pregunta:

                        self.miCursor.execute("UPDATE vehiculos SET estado=(%s) where id_vehiculo=%s",(0,ide[0]))

                        insertar2="INSERT INTO alta_baja_vehiculos (fecha,accion,id_vehiculo,marca,modelo,matricula,id_cliente,documento) values (%s,%s,%s,%s,%s,%s,%s,%s)"
                        
                        self.miCursor.execute(
                            insertar2,
                            (self.actual,0,ide[0],ide[1],ide[2],ide[3],resultado[0],resultado[2])
                            )
                
                        self.miBase.commit()

                        self.miCursor.execute(
                            "SELECT * from datos_usuarios2 where id_cliente=%s",resultado[0])
                        resultadoActualizado=self.miCursor.fetchone()

                        self.limpiar()
                        self.ver_ficha(frameGrande,resultadoActualizado,lista)


            finally:
                self.miCursor.close()

        else:
            messagebox.showinfo("Atención","Seleccione un vehículo")

    def actualizaVehiculo(self,id_vehiculo,frameGrande,resultado,lista):

        if self.var_marca.get() and self.var_modelo.get() and self.var_matricula.get():

            try:
                self.miCursor=self.miBase.cursor()
                actualiza="UPDATE vehiculos SET marca=(%s),modelo=(%s),matricula=(%s) where id_vehiculo=%s"
                self.miCursor.execute(
                    actualiza,
                    (
                        self.var_marca.get(),
                        self.var_modelo.get(),
                        self.var_matricula.get(),
                        id_vehiculo
                        )
                    )
                self.miBase.commit()

                self.miCursor.execute("SELECT id_vehiculo,marca,modelo,matricula from vehiculos where id_vehiculo=%s",id_vehiculo)
                elvehiculo=self.miCursor.fetchone()


                insertar2="INSERT INTO alta_baja_vehiculos (fecha,accion,id_vehiculo,marca,modelo,matricula,id_cliente,documento) values (%s,%s,%s,%s,%s,%s,%s,%s)"
                self.miCursor.execute(
                    insertar2,
                    (self.actual,2,elvehiculo[0],elvehiculo[1],elvehiculo[2],elvehiculo[3],resultado[0],resultado[2])
                    )
                self.miBase.commit()

                self.miCursor.execute(
                    "SELECT * from datos_usuarios2 where id_cliente=%s",resultado[0])
                resultadoActualizado=self.miCursor.fetchone()
                self.ver_ficha(frameGrande,resultadoActualizado,lista)
                self.limpiar()

            finally:

                self.miCursor.close()

        else:
            messagebox.showinfo("Atención","Faltan datos")