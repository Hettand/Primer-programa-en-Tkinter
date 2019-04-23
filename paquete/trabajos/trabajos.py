"""En este archivo esta la clase Trabajo la cual tiene como constructor
el espacio de trabajos en el panel y las funciones que abren el inicio de un
nuevo trabajo y la edicion de un trabajo existente, luego para ver los trabajos
solicitados mas antiguos se llama a funcion en cargar_trabajaos.py"""
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pymysql
import datetime
from belfrywidgets import ToolTip
import smtplib
import sys

sys.path.insert(1,"../conexion")
import conexion
sys.path.insert(1,"../panel")
import funcionalidades



Conexion=conexion.Conexion
guardaAnioMesDia=funcionalidades.guardaAnioMesDia
verDiaMesAnio=funcionalidades.verDiaMesAnio
adaptable=funcionalidades.adaptable
posicionar=funcionalidades.posicionar
siHayFrame=funcionalidades.siHayFrame
agregaFrame=funcionalidades.agregaFrame
cerrarFrame=funcionalidades.cerrarFrame


class Trabajo(Conexion,tk.Frame):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        

        #panel de trabajos: labels, entries y botones
        

        self.trabajo_cliente=tk.StringVar()
        self.fecha=tk.StringVar()
        self.fecha_guardar=tk.StringVar()
        self.id_cliente=tk.IntVar()
        self.nombre=tk.StringVar()
        self.apellidos=tk.StringVar()
        self.documento=tk.StringVar()
        self.telefono=tk.StringVar()
        self.vehiculo_elegido=tk.StringVar()
        self.servicios=[]
        self.precio=tk.DoubleVar()
        self.precios=[]
        self.precios_strings=[]
        self.descuento=tk.DoubleVar()
        self.iva=tk.DoubleVar()
        self.iva_total=tk.DoubleVar()
        self.presupuesto=tk.DoubleVar()
        self.presupuesto_suma=0
        self.descuento_calculado=tk.DoubleVar()
        self.presupuesto_sinIva=tk.DoubleVar()
        self.suma=tk.DoubleVar()        


    def agregar_editar(self,existe,nombre_titulo,entry_cliente):

        """este formulario servira tanto para crear como para editar 
        un trabajo dependiendo del boton que se pulse al ingresar un
        numero en trabajo_entry. Los condicionales dentro de esta funcion
        sirven para diferenciar la creacion y edicion de un trabajo"""

        if self.trabajo_cliente.get() !="" and existe:
            """si se ha ingresado un numero y la funcion
            existe es valida sucede lo siguiente"""

            self.ventana_agrega_t=tk.Toplevel(self)
            self.ventana_agrega_t.resizable(0,0)
            self.ventana_agrega_t.protocol(
                "WM_DELETE_WINDOW",
                self.limpiezaDatos()
                )
            self.ventana_agrega_t.transient(self)
            posicionar(self.ventana_agrega_t)
            
            frame_formulario=tk.Frame(
                self.ventana_agrega_t,
                bd=6,
                relief="groove"
                )
            frame_formulario.grid()
        
            
            dt= datetime.datetime.now()#guardar fecha y hora actuales
            actual_fecha=dt.strftime("%d-%m-%Y")
            self.fecha.set(actual_fecha)
            fecha_ingresada=self.fecha.get()
            
            guardaAnioMesDia(fecha_ingresada,self.fecha_guardar)
            self.hora_guardar=dt.strftime("%H:%M:%S")
                        
            
            frame_fecha=tk.Frame(frame_formulario)#frame superior
            frame_fecha.grid(row=1,column=0)
            
            self.frame_cliente=tk.Frame(frame_formulario,bg="#214472")#frame datos del cliente
            self.frame_cliente.grid(row=2,column=0)
            
            frame_descripcion=tk.Frame(frame_formulario)#abarca frame_izquierdo, frame_derecho y frame_lado(scroll)
            frame_descripcion.grid(row=3,column=0,sticky="nsew",ipadx=370,ipady=132)
            frame_descripcion.grid_propagate(False)
            
            self.frame_izquierdo=tk.Frame(frame_descripcion)
            self.frame_izquierdo.grid(row=0,column=0,ipadx=170,ipady=130)
            self.frame_izquierdo.grid_propagate(False)
            
            self.frame_derecho=tk.Frame(frame_descripcion)
            self.frame_derecho.grid(row=0,column=1,sticky="nsew")
            
            
            self.frame_final=tk.Frame(frame_formulario,bd=5,relief="groove")#frame inferior
            self.frame_final.grid(row=4,ipadx=360,ipady=70)
            self.frame_final.grid_propagate(False)


            titulo=tk.Label(#este titulo sera el diferenciador entre editar y crear trabajo
                frame_fecha,
                text=nombre_titulo,
                font=("verdana",12,"bold")
                )
            titulo.grid(row=0,column=0,padx=20)
            fecha_label= tk.Label(
                frame_fecha,
                text="Fecha: "
                )
            fecha_label.grid(row=0, column=1,sticky="e", padx=10,pady=10)
            fecha_label2 = tk.Label(
                frame_fecha,
                width=13,
                textvariable=self.fecha
                )
            fecha_label2.grid(row=0, column=2, padx=10, pady=10,sticky="w")

            if nombre_titulo=="Nuevo trabajo":

                """entry_cliente cambia de valor segun si se trata de un nuevo trabajo
                o de una actualizacion"""

                entry_cliente=self.trabajo_cliente.get()

                

            else:

                
                entry_cliente=self.clienteEditar

            self.imprimir_cliente(entry_cliente)


            #mostrar cliente en el formulario de nuevo trabajo y en el de actualizar también
            id_label=tk.Label(
                self.frame_cliente,
                textvariable=self.id_cliente,
                bg="#214472",
                fg="white"
                )
            id_label.grid(row=0,column=0,pady=(10,0),padx=20)
            nombre_label=tk.Label(
                self.frame_cliente,
                textvariable=self.nombre,
                bg="#214472",
                fg="white"
                )
            nombre_label.grid(row=1,column=0,padx=20)
            apellidos_label=tk.Label(
                self.frame_cliente,
                textvariable=self.apellidos,
                bg="#214472",
                fg="white"
                )
            apellidos_label.grid(row=2,column=0,pady=(0,10),padx=20,sticky="e")

            documento_label=tk.Label(
                self.frame_cliente,
                textvariable=self.documento,
                bg="#214472",
                fg="white"
                )
            documento_label.grid(row=0,column=1,padx=10,pady=(10,0))
            
            telefono_label=tk.Label(
                self.frame_cliente,
                textvariable=self.telefono,
                bg="#214472",
                fg="white"
                )
            telefono_label.grid(row=1,column=1,padx=10)

            vehiculo_label=tk.Label(#label seguido de desplegable vehiculo
                self.frame_cliente,
                text="Vehículo: ",
                bg="#214472",
                fg="white"
                )
            vehiculo_label.grid(row=2,column=1,pady=(0,10),sticky="e")
            elegir_vehiculo=ttk.Combobox(
                self.frame_cliente,
                width=30,
                values=self.selec_vehiculo(entry_cliente),
                state="readonly"
                )
            elegir_vehiculo.grid(row=2,column=2,pady=(0,10),sticky="w")
            

            boton_vehiculo=tk.Button(#boton para elegir un vehiculo
                self.frame_cliente,
                text="+",
                font=("verdana",9,"bold"),
                cursor="hand2",
                fg="blue",
                activeforeground="white",
                activebackground="black",
                command=lambda:self.add_vehiculo(elegir_vehiculo.get())
                )
            boton_vehiculo.grid(row=2,column=3,pady=(0,10),sticky="w",padx=(5,20))

            servicios_label=tk.Label(#servicios
                self.frame_cliente,
                text="Servicios: ",
                bg="#214472",
                fg="white"
                )
            servicios_label.grid(row=0,column=2,padx=(10,0),pady=10,sticky="e")
            self.elegir_servicios=ttk.Combobox(
                self.frame_cliente,
                width=30,
                values=self.selec_servicio(),
                state="readonly"
                )
            self.elegir_servicios.grid(row=0,column=3,pady=10,sticky="w")
            
            precio_label=tk.Label(#precio del servicio seleccionado
                self.frame_cliente,
                text="Precio: ",
                bg="#214472",
                fg="white"
                )
            precio_label.grid(row=1,column=3,padx=(0,30),sticky="e")
            ingresar_precio=tk.Entry(
                self.frame_cliente,
                width=10,
                textvariable=self.precio
                )
            ingresar_precio.grid(row=2,column=3,padx=5,pady=10,sticky="e")


            label_v=tk.Label(self.frame_izquierdo,text="Vehículo: ")#vehiculo
            label_v.grid(
                row=0,
                column=0,
                padx=(10,0),
                pady=(0,10),
                sticky="w"
                )
            self.label_vehiculo=tk.Label(self.frame_izquierdo,text="")
            self.label_vehiculo.grid(
                row=0,
                column=1,
                padx=5,
                pady=(0,10)
                )

            label_m=tk.Label(self.frame_izquierdo,text="Matrícula: ")#matricula
            label_m.grid(
                row=1,
                column=0,
                padx=(10,0),
                pady=(0,10),
                sticky="w"
                )
            self.label_matricula=tk.Label(self.frame_izquierdo,text="")
            self.label_matricula.grid(
                row=1,
                column=1,
                padx=5,
                pady=(0,10)
                )


            label_seguro=tk.Label(self.frame_izquierdo,text="Seguro: ")#seguro
            label_seguro.grid(row=2,column=0,padx=10,sticky="w")
            self.lista_seguros=ttk.Combobox(
                self.frame_izquierdo,
                state="readonly",
                values=self.selec_seguro()
                )
            self.lista_seguros.grid(row=2,column=1)

            observaciones_label=tk.Label(#observaciones
                self.frame_izquierdo,
                text="Observaciones:"
                )
            observaciones_label.grid(row=3,column=0,padx=10,pady=30,sticky="wn")
            self.texto=tk.Text(self.frame_izquierdo,width=20,height=5,wrap="word")
            self.texto.grid(row=3,column=1,padx=10,pady=30,sticky="s")

            if nombre_titulo!="Nuevo trabajo":

                #mostrar fecha, vehiculo, seguro, estado y observ. ya guardados para este trabajo

                verDiaMesAnio(self.fechaEditar,self.fecha)#cambiar formato a dd/mm/aaaa

                self.label_vehiculo["text"]=self.vehiculoEditarNombre
                self.label_matricula["text"]=self.vehiculoEditarMatricula
                
                self.lista_seguros.set(self.seguroEditar)

                self.estado_label=tk.Label(self.frame_izquierdo,text="Estado: ")
                self.estado_label.grid(row=4,column=0,padx=10)

                self.estado_desplegable=ttk.Combobox(#desplegable de estado
                    self.frame_izquierdo,
                    values=["Solicitado","Iniciado","Terminado","Despachado"],
                    state="readonly"
                    )
                self.estado_desplegable.grid(row=4,column=1)
                self.estado_desplegable.set(self.estadoEditar)#estado almacenado en la bd

                if self.observacionesEditar:#ver observaciones guardadas

                    self.texto.insert("insert",self.observacionesEditar)

            
            
            frame_lado = tk.Frame(frame_descripcion)#frame a un lado del frame_derecho para el scroll 
            frame_lado.grid(row=0,column=2,sticky="e")
            

            scroll = tk.Scrollbar(frame_lado)#scroll termina en la funcion actualizar_resultados
            self.c=tk.Canvas(self.frame_derecho,yscrollcommand=scroll.set)
            scroll.config(command=self.c.yview)
            scroll.grid(sticky="e",column=4,row=0,ipady=100)
            frame_linea= tk.Frame(self.frame_derecho)
            frame_linea.grid(sticky="nse",row=0,column=1)
            
            self.contenedor = tk.Frame(self.c,width=190)
            self.contenedor.grid()

            self.c.create_window(0,0,window=self.contenedor,anchor="nw")
            self.c.grid(sticky="nsew")


            #este boton lo he escrito aqui porque debo definir el canvas antes de add_servicio
            boton_servicio=tk.Button(#añadir servicio
                self.frame_cliente,
                text="+",
                font=("verdana",9,"bold"),
                fg="blue",
                cursor="hand2",
                command=lambda:self.add_servicio(
                    self.elegir_servicios.get(),
                    self.precio.get()
                    ),
                activebackground="black",
                activeforeground="white"
                )
            boton_servicio.grid(row=2,column=4,padx=(5,10),sticky="w")            


            descuento_label=tk.Label( self.frame_final,text="Descuento: ")#descuento
            descuento_label.grid(row=1,column=0,sticky="w",pady=10)
            descuento_entry=tk.Entry(
                self.frame_final,
                textvariable=self.descuento,
                width=5
                )
            descuento_entry.grid(row=1,column=1,sticky="w",pady=10,padx=5)
            porcentaje_label=tk.Label(self.frame_final,text="%")
            porcentaje_label.grid(row=1,column=2,sticky="w",pady=10)
            desc_igual=tk.Button(
                self.frame_final,
                text="=",
                command=lambda:self.actualizar_resultados()
                )
            desc_igual.grid(row=1,column=3,sticky="w",padx=(30,5))
            desc_monto=tk.Label(
                self.frame_final,
                textvariable=self.descuento_calculado
                )
            desc_monto.grid(row=1,column=4,sticky="w")


            iva_label=tk.Label(self.frame_final,text="IVA: ")#zona iva
            iva_label.grid(row=2,column=0,sticky="w",pady=10)
            iva_entry=ttk.Entry(self.frame_final,textvariable=self.iva,width=5)
            iva_entry.grid(row=2,column=1,sticky="w",pady=10,padx=5)
            iva_porc=tk.Label(self.frame_final,text="%")
            iva_porc.grid(row=2,column=2,sticky="w",pady=10)
            iva_igual=tk.Button(
                self.frame_final,
                text="=",
                command=lambda:self.actualizar_resultados()#actualizar montos
                )
            iva_igual.grid(row=2,column=3,sticky="w",padx=(30,5))
            iva_monto=tk.Label(self.frame_final,textvariable=self.iva_total)
            iva_monto.grid(row=2,column=4,sticky="w")

            
            presup_sinIva=tk.Label(self.frame_final,text="Subtotal: ")#presupuesto sin iva
            presup_sinIva.grid(row=1,column=5,sticky="w",pady=10,padx=(180,20))
            resultado=tk.Label(
                self.frame_final,
                textvariable=self.presupuesto_sinIva
                )
            resultado.grid(row=1,column=6)



            
            suma_label=tk.Label(self.frame_final,text="Suma: ")#suma de los servicios
            suma_label.grid(row=0,column=5,pady=10,padx=(180,20))
            sumado=tk.Label(self.frame_final,textvariable=self.suma)
            sumado.grid(row=0,column=6)


            

            presupuesto_label=tk.Label(self.frame_final,text="Total: ")
            presupuesto_label.grid(row=2,column=5,sticky="w",pady=10,padx=(180,20))
            
            resultado=tk.Label(
                self.frame_final,
                textvariable=self.presupuesto,
                bg="darkblue",
                fg="white",
                font=("verdana",12,"bold")
                )
            resultado.grid(row=2,column=6,sticky="w")



            if nombre_titulo!="Nuevo trabajo" and self.serviciosEditar:

                """iteramos los resultados obtenidos en self.comprueba_trabajo
                para ir agregandolos al formulario"""

                n=0
                for s in self.serviciosEditar:
                    self.add_servicio(
                        self.serviciosEditar[n],
                        float(self.preciosEditar[n])
                        )
                    n+=1

                #descuento e iva
                self.descuento.set(self.descuentoEditar)
                self.iva.set(self.ivaEditar)
                self.actualizar_resultados()


            if nombre_titulo=="Nuevo trabajo":

                #botones que se crean segun se crea un nuevo trabajo o se edita

                self.creaBotonGuardar(nombre_titulo)

            else:

                self.creaBotonEditar(nombre_titulo)

        else:
            messagebox.showinfo(
                "Atención",
                "Ingrese un número válido"
                )

    




    def existe_cliente(self,numero):

        #comprobar la existencia de un cliente

        try:
            self.miCursor = self.miBase.cursor()
            self.miCursor.execute(
                "SELECT id_cliente FROM datos_usuarios2 WHERE id_cliente=%s",
                numero
                )
            resultado=self.miCursor.fetchone()
            return resultado
        finally:
            self.miBase.commit()
            self.miCursor.close()


    def imprimir_cliente(self,numero):

        #imprimir en el formulario los datos del cliente

        try:
            self.miCursor = self.miBase.cursor()
            self.miCursor.execute(
                "SELECT id_cliente,nombre,apellido,apellido_dos,documento,telefono FROM datos_usuarios2 where id_cliente like %s",
                numero
                )
            cliente=self.miCursor.fetchone()
            self.id_cliente.set("Cliente Nº {}".format(cliente[0]))
            self.nombre.set("{}".format(cliente[1]))
            self.apellidos.set("{} {}".format(cliente[2],cliente[3]))
            self.documento.set("Documento: {}".format(cliente[4]))
            self.telefono.set("Tel.: {}".format(cliente[5]))

        except:
            messagebox.showinfo("Atención","Sin resultados")

        finally:

            self.miBase.commit()
            self.miCursor.close()


    def selec_vehiculo(self,numero):

        #seleccionar un vehiculo vinculado al cliente

        try:
            self.miCursor = self.miBase.cursor()
            self.miCursor.execute(
                "SELECT * FROM vehiculos where cliente_n=%s",
                numero
                )
            vehiculos=self.miCursor.fetchall()
            lista=[]
            n=0
            for v in vehiculos:
                
                lista.append("{} - {}  {} - {}".format(
                    vehiculos[n][0],
                    vehiculos[n][2],
                    vehiculos[n][3],
                    vehiculos[n][4]
                    )
                )
                n+=1
                if n == len(vehiculos):
                    break
            return lista

        finally:

            self.miCursor.close()


    def selec_servicio(self):

        #lista desplegable de servicios

        try:
            self.miCursor = self.miBase.cursor()
            self.miCursor.execute("SELECT * FROM servicios")
            servicios=self.miCursor.fetchall()

            lista = []
            n=-1
            for s in servicios:
                n+=1
                lista.append("{}".format(servicios[n][1]))
                if n == len(servicios):
                    break
            return lista


        finally:

            self.miCursor.close()


    def selec_seguro(self):

        #elegir si tiene seguro sino elegir 'No'

        try:
            self.miCursor = self.miBase.cursor()
            self.miCursor.execute("SELECT nombre FROM seguros")
            seguros=self.miCursor.fetchall()
            lista=["No"]
            n=0
            for s in seguros:
                lista.append("{}".format(seguros[n][0]))
                n+=1
                if n == len(seguros):
                    break
            return lista


        finally:

            self.miCursor.close()

  
    def add_vehiculo(self,vehiculo):

        #vincular vehiculo al trabajo

        if vehiculo != "":
            lista_vehiculo=vehiculo.split(" - ")

            self.vehiculo_elegido.set("{}".format(lista_vehiculo[0]))
            self.label_vehiculo["text"]=lista_vehiculo[1]
            self.label_matricula["text"]=lista_vehiculo[2]


    def add_servicio(self,servicio,precio):

        """Al añadir un servicio con su precio serán añadidos a ambas listas
        como en la bd guardamos una lista con los precios tenemos que tenerla 
        convertida en strings. Al añadir tambien actualizamos presupuesto
        y reseteamos el combobox de servicios y el entry de precios"""

        if len(self.servicios)==0:
            #si la lista esta vacia reseteo el iva y el descuento
            self.descuento.set(0)
            self.iva.set(0)

        if servicio !="" and precio !="":
            

            self.servicios.append(servicio)
            
            self.precios.append(precio)

            self.precios_strings.append(str(precio))

            self.actualizar_presupuesto()

            self.elegir_servicios.set("")
            self.precio.set(0)                 
                      
            

    def eliminar(self,serv,pre):

        #eliminar el último servicio añadido

        n=(len(self.servicios)-1)
        

        ultimo_servicio = "serv{}".format(n)
        ultimo_precio = "pre{}".format(n)

        try:

            if str(serv).split(".")[-1]==ultimo_servicio:
                serv.grid_remove()
                self.servicios.pop()


            if str(pre).split(".")[-1]==ultimo_precio:
                pre.grid_remove()
                self.presupuesto.set(self.presupuesto_suma-self.precios[-1])

                self.precios.pop()
                self.precios_strings.pop()
            
        except:
            messagebox.showinfo("Aviso","No se ha podido eliminar")

        finally:
            self.actualizar_presupuesto()
 
        
    def actualizar_presupuesto(self):

        """Cada servicio con su precio(serv y pre) tendra un name diferente
        para poder ser identificado el último de ellos con el boton que 
        elimina el último servicio añadido"""

        try:

            i=0
            for s in self.servicios:
                name_serv="serv{}".format(i)
                serv=tk.Label(
                    self.contenedor,
                    name=name_serv,
                    text=self.servicios[i],
                    width=35
                    )
                serv.grid(row=i,column=0,sticky="w",padx=(0,5))


                name_pre="pre{}".format(i)
                pre=tk.Label(
                    self.contenedor,
                    name=name_pre,
                    text=self.precios[i]
                    )
                pre.grid(row=i,column=1,sticky="e",padx=(15,0))
                i+=1



                if i==len(self.servicios):
                    break

            if len(self.servicios)>0:
                #boton que elimina el último servicio añadido
                self.flecha=tk.PhotoImage(file="../img/flecha.png")
                eliminar=tk.Button(
                    self.frame_cliente,
                    image=self.flecha,
                    command=lambda:self.eliminar(serv,pre),
                    fg="red",activeforeground="white",activebackground="red"
                    )
                eliminar.grid(row=0,column=4,padx=5,sticky="w")
            

        except:
            messagebox.showinfo("Atención","Revise los datos ingresados")


        finally:
            self.actualizar_resultados()
            self.frame_derecho.update()#final de scroll
            self.c.config(scrollregion=self.c.bbox("all"))


    def actualizar_resultados(self):

        try:

            self.presupuesto_suma= sum(self.precios[:])
            self.suma.set(self.presupuesto_suma)


            calculo1=round((self.suma.get()*(self.descuento.get()/100)),2)
            self.descuento_calculado.set(calculo1)
            sinIva=round(self.suma.get()-self.descuento_calculado.get(),2)
            self.presupuesto_sinIva.set(sinIva)


            calculo2=round(((self.presupuesto_sinIva.get()/100)*self.iva.get()),2)
            self.iva_total.set(calculo2)
            total=round(self.iva_total.get()+self.presupuesto_sinIva.get(),2)
            self.presupuesto.set(total)

        except:
            messagebox.showinfo(
                "Atención",
                "Verificar datos, ejemplo de formato de decimales: 10.5"
                )

    def creaBotonGuardar(self,nombre_titulo):

        #boton para guardar nuevo trabajo

        boton_guardar=tk.Button(
                self.frame_final,
                text="Guardar",
                fg="blue",activebackground="blue",
                activeforeground="white",
                command=lambda:self.antesDeGuardar(nombre_titulo)
                )

        boton_guardar.grid(row=2,column=7,padx=(20,3))


    def creaBotonEditar(self,nombre_titulo):

        #boton para actualizar trabajo

        boton_editar=tk.Button(
                self.frame_final,
                text="Actualizar",
                fg="blue",activebackground="blue",
                activeforeground="white",
                command=lambda:self.guardar_trabajo(nombre_titulo)
                )

        boton_editar.grid(row=2,column=7,padx=(20,3))





    def antesDeGuardar(self,nombre_titulo):

        """Antes de guardar coprueba que el vehiculo ya no este en el taller,
        vuelve a calcular descuento e iva y resultado"""


        self.actualizar_resultados()


        id_vehiculo=self.vehiculo_elegido.get()

        try:
            self.miCursor = self.miBase.cursor()
            self.miCursor.execute(
                "SELECT id_trabajo,estado from trabajos where id_vehiculo=%s",id_vehiculo
                )
            ya_existe=self.miCursor.fetchone()


            if ya_existe and ya_existe[1]!="Terminado":
                #si ya hay un trabajo en proceso para ese vehiculo 
                messagebox.showinfo(
                    "Atención",
                    "Este vehículo ya esta en el taller\nPuede editar el trabajo nº{} vinculado".format(
                        ya_existe[0])
                    )

            else:
                self.guardar_trabajo(nombre_titulo)
        
        finally:
            self.miBase.commit()
            self.miCursor.close()

    def comprobar_trabajo(self,id_trabajo):

        """Comprobar si existe el trabajo y hacer la consulta 
        para poder mostrar los datos en el formulario"""

        try:
            self.miCursor=self.miBase.cursor()
            self.miCursor.execute(
                "SELECT * from trabajos where id_trabajo=%s",
                id_trabajo)
            resultado=self.miCursor.fetchone()

            self.fechaEditar=resultado[0]
            self.HoraEditar=resultado[1]
            
            self.trabajoEditar=resultado[2]
            self.clienteEditar=resultado[3]
            
       
            self.descuentoEditar=resultado[7]
            self.ivaEditar=resultado[9]
            self.seguroEditar=resultado[12]
            self.observacionesEditar=resultado[13]
            self.estadoEditar=resultado[15]

            self.miCursor.execute(#extraer datos del vehiculo para mostrarlos
                "SELECT * FROM vehiculos where id_vehiculo=%s",
                resultado[4]
                )
            vehiculo=self.miCursor.fetchone()
            self.vehiculoEditarNombre="{} {}".format(
                vehiculo[2],
                vehiculo[3]
                )
            self.vehiculoEditarMatricula=vehiculo[4]
            self.vehiculo_elegido.set(vehiculo[0])


            """separamos los servicios y precios para gusrdarlos 
            como lista e ir agregandolos al formulario"""
            self.serviciosEditar=resultado[5].split(",")
            self.preciosEditar=resultado[6].split(",")


            self.agregar_editar(#abre el formulario de trabajo para editarlo
                self.existe_cliente(self.clienteEditar),
                "Editar trabajo nº{}".format(self.trabajoEditar),
                self.clienteEditar
                )


        except:
            messagebox.showinfo("Aviso","Nº de trabajo no encontrado")

        finally:
            self.miCursor.close()


    def limpiezaDatos(self):

        del self.servicios[:]#dejar las listas vacias
        del self.precios[:]
        del self.precios_strings[:]

        self.suma.set(0.0)
        self.descuento.set(0.0)
        self.descuento_calculado.set(0.0)
        self.iva.set(0.0)
        self.presupuesto_sinIva.set(0.0)
        self.iva_total.set(0.0)
        self.presupuesto.set(0.0)    

            

    def guardar_trabajo(self,nombre_titulo):

        #guardar tranajo

        if self.fecha_guardar.get()!="" and self.vehiculo_elegido.get()!="" and self.servicios and self.precios and self.lista_seguros.get()!="" and self.iva.get()!="" and self.descuento.get()!="":

            if nombre_titulo=="Nuevo trabajo":
                pregunta= messagebox.askyesno("Nuevo trabajo","¿Desea guardar este trabajo?")

                if pregunta:

                    try:
                        self.miCursor = self.miBase.cursor()
                        insertar="INSERT INTO trabajos (fecha,hora,id_trabajo,cliente_n,id_vehiculo,servicios,precios,presupuesto,descuento,monto_descuento,iva,monto_iva,seguro,observaciones,fecha_fin,estado) values (%s,%s,null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        

                        self.miCursor.execute(
                            insertar,
                            (
                                self.fecha_guardar.get(),
                                self.hora_guardar,
                                self.trabajo_cliente.get(),
                                self.vehiculo_elegido.get(),
                                (",").join(self.servicios),#juntar lista para luego poder extraerla
                                (",").join(self.precios_strings),
                                self.presupuesto.get(),
                                self.descuento.get(),
                                self.descuento_calculado.get(),
                                self.iva.get(),
                                self.iva_total.get(),
                                self.lista_seguros.get(),
                                self.texto.get("1.0","end"),
                                "No establecida",
                                "Solicitado"
                                )
                            )
                        self.miBase.commit()

                        #consulta para obtener el ultimo trabajo añadido---
                        self.miCursor.execute("SELECT id_trabajo from trabajos order by asc")
                        resultados=self.miCursor.fetchall()

                        self.miCursor.execute("SELECT matricula from vehiculos where id_vehiculo=%s",resultados[-1])
                        matricula=self.miCursor.fetchone()
                        

                        #insertar en tabla actualizaciones el ultimo registro añadido
                        insertar2="INSERT INTO actualizaciones (id_trabajo,id_vehiculo,fecha,hora,servicios,precios,porcentaje_desc,descuento,porcentaje_iva,iva,descripcion) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        self.miCursor.execute(
                            insertar2,
                            (
                             matricula[0],
                                self.vehiculo_elegido.get(),
                                self.fecha_guardar.get(),
                                self.hora_guardar,
                                (",").join(self.servicios),#guardar en la bd cada servicio separado por comas
                                (",").join(self.precios_strings),
                                self.descuento.get(),
                                self.descuento_calculado.get(),
                                self.iva.get(),
                                self.iva_total.get(),
                                "Solicitado"
                                )
                            )
                        self.miBase.commit()

                        trabajo=str(resultados[-1]).split("(")
                        trabajo=str(trabajo[1]).split(")")
                        trabajo=str(trabajo[0])
                        messagebox.showinfo(
                            "Nuevo trabajo",
                            "Trabajo Nº {}\nguardado con éxito".format(trabajo)
                            )
                        self.limpiezaDatos()
                        self.ventana_agrega_t.destroy()
                    finally:

                        self.miBase.commit()
                        self.miCursor.close()

                        

            else:
                pregunta2= messagebox.askyesno("Editar trabajo","¿Desea guardar los cambios?")


                if pregunta2:
                    #si se trata de una actualizacion
                    self.actualizar_resultados()

                    try:
                        self.miCursor = self.miBase.cursor()
                        actualizar="UPDATE trabajos SET id_vehiculo=(%s),servicios=(%s),precios=(%s),descuento=(%s),monto_descuento=(%s),iva=(%s),monto_iva=(%s),presupuesto=(%s),seguro=(%s),observaciones=(%s),fecha_fin=(%s),estado=(%s) where id_trabajo=%s"
                        
                        if self.estado_desplegable.get()=="Terminado": 

                            fecha_fin=self.fecha.get()

                        else:

                            fecha_fin="No establecida"

                        self.miCursor.execute(
                            actualizar,
                            (
                            
                                self.vehiculo_elegido.get(),
                                (",").join(self.servicios),#juntar lista para luego poder extraerla
                                (",").join(self.precios_strings),
                                self.descuento.get(),
                                self.descuento_calculado.get(),
                                self.iva.get(),
                                self.iva_total.get(),
                                self.presupuesto.get(),
                                self.lista_seguros.get(),
                                self.texto.get("1.0","end"),
                                fecha_fin,
                                self.estado_desplegable.get(),
                                self.trabajoEditar
                                )
                            )
                        self.miBase.commit()
                        #consulta para obtener el ultimo trabajo añadido---
                        self.miCursor.execute(
                            "SELECT id_trabajo from trabajos where id_trabajo=%s",
                            self.trabajoEditar
                            )
                        resultado=self.miCursor.fetchone()
                        self.miCursor.execute(
                            "SELECT matricula from vehiculos where id_vehiculo=%s",
                            self.vehiculo_elegido.get()
                            )
                        matricula=self.miCursor.fetchone()
                        

                        #insertar en tabla actualizaciones el ultimo registro añadido
                        insertar2="INSERT INTO actualizaciones (id_trabajo,id_vehiculo,fecha,hora,servicios,precios,porcentaje_desc,descuento,porcentaje_iva,iva,descripcion) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        

                        self.miCursor.execute(
                            insertar2,
                            (
                                self.trabajoEditar,
                                matricula[0],
                                self.fecha_guardar.get(),
                                self.hora_guardar,
                                (",").join(self.servicios),
                                (",").join(self.precios_strings),
                                self.descuento.get(),
                                self.descuento_calculado.get(),
                                self.iva.get(),
                                self.iva_total.get(),
                                self.estado_desplegable.get()
                                
                                )
                            )
                        
                        messagebox.showinfo(
                            "Trabajo",
                            "Trabajo Nº {}\nactualizado con éxito".format(resultado[0])
                            )
                        self.ventana_agrega_t.destroy()

                    except pymysql.err.DataError:

                        messagebox.showinfo("Atención", "Revise los datos")
                    finally:
                        self.miBase.commit()
                        self.miCursor.close()

                        self.limpiezaDatos()

                

        else:
            messagebox.showinfo("Atención","Faltan datos")


    def mostrarTrabajos(self,frameGrande,filtro,lista2):

        if filtro.get():

            try:
                self.miCursor = self.miBase.cursor()
                self.miCursor.execute(
                    "SELECT estado FROM trabajos where estado=%s",
                    filtro.get()
                    )
                resultado=self.miCursor.fetchall()

                if resultado:

                    siHayFrame(lista2)

                    self.mostrar_trabajos(frameGrande,filtro.get(),filtro,lista2)

                else:

                    messagebox.showinfo(
                        "Atención",
                        "No hay registros de trabajos {}s".format(
                            filtro.get()
                            )
                        )


            finally:

                self.miCursor.close()


        else:

            messagebox.showinfo("Atención","Filtro no especificado")



    
    def mostrar_trabajos(self,frameGrande,estado,combobox,lista2):


        try:

            self.miCursor = self.miBase.cursor()

            self.miCursor.execute(
                "SELECT t.Fecha,t.id_trabajo,v.marca,v.modelo,v.matricula,t.servicios,t.observaciones,t.estado from trabajos t join vehiculos v where t.id_vehiculo=v.id_vehiculo and t.estado=%s",
                estado

                )
            datos=self.miCursor.fetchall()

            if datos:


                self.frameDinamico=tk.Frame(frameGrande)
                self.frameDinamico.grid(row=0,column=0,sticky="n")
                frameGrande.rowconfigure(0,weight=4)
                frameGrande.columnconfigure(0,weight=4)
                agregaFrame(self.frameDinamico,lista2)

                frameTitulo=tk.Frame(self.frameDinamico)
                frameTitulo.grid(row=0,column=0,sticky="nsew",pady=(20,0))



                frame_trabajos=tk.Frame(self.frameDinamico)
                frame_trabajos.grid(row=1,column=0)

                """ hay un label que está más abajo que iría acá
                pero necesito otras variables de abajo para el titulo """

                botonCerrar=tk.Button(
                frameTitulo,
                text="x",
                bg="red",
                fg="white",
                font=("verdana",12,"bold"),
                relief="flat",
                command=lambda:cerrarFrame(lista2)
                )
                botonCerrar.grid(row=0,column=1,ipadx=2,sticky="nsew")
                frameTitulo.columnconfigure(1, weight=1)

                frame_campos=tk.Frame(frame_trabajos)
                frame_campos.grid(row=1,column=0)

                columnas=(
                    "Fecha",
                    "ID",
                    "Vehículo",
                    "Matrícula",
                    "Servicios",
                    "Observaciones"
                    )
                col=0
                width=10
                row=1
                for c in columnas:
                    label=tk.Label(
                        frame_campos,
                        text=c,
                        borderwidth=2,
                        relief="groove",
                        width=width,
                        background="#5a98c4",
                        fg="white"
                        )
                    label.grid(row=0,column=col,ipady=5)
                    col+=1

                    if col==1:
                        width=6
                    elif col==2 or col==4:
                        width=25
                    elif col==3:
                        width=10
                    elif col==5:
                        width=23
                seleccionar=tk.Button(
                    frame_campos,
                    text="Todos"
                    )
                seleccionar.grid(row=0,column=6,ipady=5)

                if len(datos) > 5: 

                # si hay mas de 5 aparece scroll   

                    frame_scroll=tk.Frame(frame_trabajos)
                    frame_scroll.grid(row=2,column=2,sticky="e")

                    scroll=tk.Scrollbar(frame_scroll)
                    c=tk.Canvas(frame_trabajos,yscrollcommand=scroll.set,bg="white")
                    scroll.config(command=c.yview)
                    scroll.grid(sticky="e",ipady=240)
                    
                    linea= tk.Frame(frame_trabajos)
                    linea.grid(sticky="nse",column=1,row=2)
                                
                    contenedor = tk.Frame(c, width=150)
                    contenedor.grid()

                    c.create_window(0,0,window=contenedor,anchor="nw")
                    c.grid(sticky="nsew",row=2,column=0)

                else:

                    contenedor = tk.Frame(frame_trabajos)
                    contenedor.grid(row=2)

                widget = {}
                row=0
                for fecha,trabajo,marca,modelo,matricula,servicios,observaciones,estado in datos:

                    verFecha=tk.StringVar()

                    verDiaMesAnio(fecha,verFecha)
                    lista=servicios.split(",")
                    juntos=("\n").join(lista)#para que cada elemento de la lista tenga un salto de linea

                    if len(datos)!=1:

                        texto="{} trabajos {}s".format(len(datos),estado)

                    else:

                        texto="{} trabajo {}".fotmat(len(datos),estado)

                    labelTitulo=tk.Label(
                        frameTitulo,
                        bg="black",
                        fg="white",
                        text=texto,
                        font=("verdana",12)
                        )
                    labelTitulo.grid(row=0,column=0,sticky="nsew")
                    frameTitulo.columnconfigure(0,weight=30)



                    widget[fecha] ={
                    "Fecha": tk.Label(
                        contenedor,
                        text=verFecha.get(),
                        borderwidth=2,
                        relief="groove",
                        width=10
                        ),
                    "ID": tk.Label(
                        contenedor,
                        text=trabajo,
                        borderwidth=2,
                        relief="groove",
                        width=6
                        ),
                    "Vehículo": tk.Label(
                        contenedor,
                        text="{}\n{}".format(marca,modelo),
                        borderwidth=2,
                        relief="groove",
                        width=25
                        ),
                    "Matricula": tk.Label(
                        contenedor,
                        text=matricula,
                        borderwidth=2,
                        relief="groove",
                        width=10
                        ),
                    "Servicios": tk.Label(
                        contenedor,
                        text=juntos,
                        borderwidth=2,
                        relief="groove",
                        width=25
                        ),
                    "Observaciones": tk.Text(
                        contenedor,
                        borderwidth=2,
                        relief="groove",
                        width=23,
                        height=6,
                        wrap="word",
                        bg="#f3f3f3",
                        font=("Arial",10)
                        ),
                    "Ver": tk.Label(
                        contenedor,
                        borderwidth=2,
                        relief="groove",
                        width=6
                        ) 
                    }
                    tk.Checkbutton(
                        widget[fecha]["Ver"],
                        name="trabajo{}".format(trabajo)
                        ).grid()
                    widget[fecha]["Fecha"].grid(row=row, column=0, sticky="nsew",ipady=5)
                    widget[fecha]["ID"].grid(row=row, column=1, sticky="nsew",ipady=5) 
                    widget[fecha]["Vehículo"].grid(row=row, column=2, sticky="nsew",ipady=5)
                    widget[fecha]["Matricula"].grid(row=row, column=3, sticky="nsew",ipady=5) 
                    widget[fecha]["Servicios"].grid(row=row, column=4, sticky="nsew",ipady=5) 
                    
                    widget[fecha]["Observaciones"].grid(row=row, column=5, sticky="nsew",ipady=5)
                    widget[fecha]["Observaciones"].configure(state="normal")
                    widget[fecha]["Observaciones"].insert("insert", observaciones)
                    widget[fecha]["Observaciones"].configure(state="disabled")

                    widget[fecha]["Ver"].grid(row=row, column=6, sticky="nsew",ipady=5,ipadx=8) 
                    
                    

                    row+=1

                if len(datos) > 5:

                    frame_trabajos.update()
                    c.config(scrollregion=c.bbox("all"))





            else:
                messagebox.showinfo("Atención","No hay registros")
            

        finally:

            self.miBase.commit()
            self.miCursor.close()
            combobox.set("")

            
            





