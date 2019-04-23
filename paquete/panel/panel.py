import sys
sys.path.insert(1,"../conexion")
import conexion
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import time
import locale
import pymysql
from belfrywidgets import ToolTip

sys.path.insert(2,"../clientes")
import clientes
import ficha
sys.path.insert(1,"../trabajos")
import trabajos
sys.path.insert(2,"../servicios")
import servicios
import seguros
sys.path.insert(2,"../stock")
import stock
import funcionalidades
import formulario_cliente




Conexion=conexion.Conexion
Cliente=clientes.Cliente
Trabajo=trabajos.Trabajo
Servicio=servicios.Servicio
guardaAnioMesDia=funcionalidades.guardaAnioMesDia
verDiaMesAnio=funcionalidades.verDiaMesAnio
adaptable=funcionalidades.adaptable
Stock=stock.Stock
FormularioCliente=formulario_cliente.FormularioCliente
Ficha=ficha.Ficha
siHayFrame=funcionalidades.siHayFrame
agregaFrame=funcionalidades.agregaFrame


class Panel(Conexion,tk.Frame):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        self.frame_contenedor=tk.Frame(self)
        self.frame_contenedor.grid(
            row=0,
            column=1,
            sticky="nsew"
            )
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1,weight=10)

        # ------------------ frame del reloj ---------------------------

        frame_reloj=tk.Frame(self.frame_contenedor)
        frame_reloj.grid(
            row=0,
            column=0,
            sticky="nsew"
            )
        
        label_logo=tk.Label(
            frame_reloj,
            bg="black",
            image=self.taller
            )
        label_logo.grid(row=0,column=0,sticky="nsew",ipady=5)
        adaptable(frame_reloj,0,0)

        self.fecha=tk.Label(frame_reloj,bg="black",fg="white")
        self.fecha.grid(row=1,column=0,sticky="nsew",ipadx=5)
        adaptable(frame_reloj,1,0)

        self.clock = tk.Label(frame_reloj, font=('Consolas', 18), bg="Black", fg="white")
        self.clock.grid(row=2,column=0,sticky="nsew")
        adaptable(frame_reloj,2,0)

        self.actual=''
        self.time1=''
        self.reloj()
 



        # -------------- Clientes ---------------------------------------------------

        self.cliente=Cliente(self.frame_contenedor)
        self.cliente.grid(row=0,column=1,sticky="nsew")
        

        clientes_cabecera1=tk.Label(
            self.cliente,
            text="Clientes",
            bg="black",
            fg="white"
            )
        clientes_cabecera1.grid(row=0,column=0,sticky="new")

        frameCliente = tk.Frame(self.cliente)
        frameCliente.grid(row=1,column=0,pady=10)

        self.botonClientes=tk.Button(
            frameCliente,
            image=self.imgClientes,
            cursor="hand2",
            relief="flat",
            command=lambda:self.cliente.ver_todos(self.frameGrande,self.lista),
            activebackground="black",
            activeforeground="white",
            text=" Todos",
            font=self.bold,
            compound="left",
            fg="#27455b"
            )
        self.botonClientes.grid(row=0,column=0,padx=10)
        ToolTip(self.botonClientes,"Ver todos los clientes")
        


        self.form = tk.Button(
            frameCliente,
            image=self.formClientes,
            cursor="hand2",
            relief="flat",
            command=lambda:self.cliente.abrirFormularioCliente(self.form),
            activebackground="black",
            activeforeground="white",
            text=" Formulario",
            font=self.bold,
            compound="left",
            fg="#27455b"
            )
        self.form.grid(row=0,column=1,padx=10)
        ToolTip(self.form,"Formulario Clientes")

        frameCliente2=tk.Frame(self.cliente,bd=1,relief="sunken")
        frameCliente2.grid(
            row=2,
            column=0,
            padx=20,
            pady=5,
            sticky="w"
            )

        self.label_id=tk.Label(
            frameCliente2,
            text="Doc.:",
            font=self.bold,
            fg="#27455b"
            )
        self.label_id.grid(
            row=0,
            column=0,
            padx=(10,5)
            )

        self.boton10=tk.Button(
            frameCliente2,
            image=self.fichaCliente,
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            command=lambda:self.laficha()
            )
        self.boton10.grid(
            row=0,
            column=2
            )
        ToolTip(self.boton10,"Ver ficha")
        
        

        self.entry_id=tk.Entry(
            frameCliente2,
            width=12,
            textvariable=self.cliente.var_entry_id
            )
        self.entry_id.grid(
            row=0,
            column=1,
            padx=10,
            pady=5

            )
        ToolTip(self.entry_id,"Documento")

        escobita=tk.Button(
            frameCliente2,
            image=self.escoba,
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            command=lambda:self.cliente.var_entry_id.set("")
            )
        escobita.grid(row=0,column=1,sticky="e")
        ToolTip(escobita,"Limpiar")



        farmeCleinte3=tk.Frame(self.cliente)
        farmeCleinte3.grid(row=3,column=0,padx=10)

        self.selec = ttk.Combobox(
            farmeCleinte3,
            values=[
            "Matrícula",
            "Marca",
            "Modelo",
            "Nombre",
            "1er Apellido",
            "2do Apellido"
            ],
            state="readonly",
            width=12
            )
        self.selec.grid(row=0,column=0,padx=5)

        self.abc=ttk.Combobox(
            farmeCleinte3,
            values=["A","B","C","D","E","F","G","H","I",
            "J","K","L","M","N","Ñ","O","P","Q",
            "R","S","T","U","V","W","X","Y","Z"
            ],
            state="readonly",
            width=3
            )
        self.abc.grid(row=0,column=1,padx=5)
        self.abc_boton=tk.Button(
            farmeCleinte3,
            image=self.filtro,
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            command=lambda:self.cliente.ver_inicial(
                self.abc.get(),
                self.frameGrande,
                self.abc,
                self.selec,
                self.lista
                )
            )
        self.abc_boton.grid(row=0,column=2,padx=5)
        ToolTip(self.abc_boton,"Filtro alfabético")

        

        


        # --------------------- Trabajos -------------------------------------------------------------------------

        self.trabajo=Trabajo(self.frame_contenedor)
        self.trabajo.grid(row=0,column=2,sticky="nsew")
        trabajos_cabecera=tk.Label(
            self.trabajo,
            text="Trabajos",
            bg="black",
            fg="white"
            )
        trabajos_cabecera.grid(row=0,column=0,sticky="new")

        frame_trabajo=tk.Frame(self.trabajo)
        frame_trabajo.grid(row=1,column=0)
 

        boton_trabajos=tk.Button(#boton para crear trabajo
            frame_trabajo,
            image=self.imagen_t,
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            command=lambda:self.trabajo.agregar_editar(
                self.trabajo.existe_cliente(self.trabajo.trabajo_cliente.get()),
                "Nuevo trabajo",
                self.trabajo.trabajo_cliente
                ),
            text=" Nuevo",
            font=self.bold,
            compound="left",
            fg="#27455b"
            )
        boton_trabajos.grid(row=0,column=2,padx=5)
        ToolTip(boton_trabajos,"Añadir trabajo")

        trabajo_label=tk.Label(frame_trabajo,text="ID:",font=self.bold,fg="#27455b")
        trabajo_label.grid(row=1,column=0,padx=5)

        trabajo_entry=tk.Entry(frame_trabajo,textvariable=self.trabajo.trabajo_cliente,width=5)
        trabajo_entry.grid(row=1,column=1,padx=5,sticky="w")
        ToolTip(trabajo_entry,"Id cliente para añadir trabajo\nId trabajo para editar trabajo")

        boton_editar=tk.Button(#boton para editar trabajo
            frame_trabajo,
            image=self.editartrabajo,
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            command=lambda:self.trabajo.comprobar_trabajo(self.trabajo.trabajo_cliente.get()),
            text=" Editar ",
            font=self.bold,
            compound="left",
            fg="#27455b"
            )
        boton_editar.grid(row=1,column=2,padx=5)
        ToolTip(boton_editar,"Editar trabajo")



        frameFiltros=tk.Frame(self.trabajo)
        frameFiltros.grid(row=2,column=0)

        self.filtroTrabajos=ttk.Combobox(#filtro de trabajos llama a "../trabajos/cargar_trabajos"
            frameFiltros,
            values=["Solicitado","Iniciado","Terminado","Despachado"],
            state="readonly",
            width=12
            )
        self.filtroTrabajos.grid(row=1,column=1,sticky="e")

        btnTrabajos=tk.Button(
            frameFiltros,
            image=self.filtro,
            cursor="hand2",
            relief="flat",
            command=lambda:self.trabajo.mostrarTrabajos(self.frameGrande,self.filtroTrabajos,self.lista)
            )
        btnTrabajos.grid(row=1,column=2,padx=5)
        ToolTip(btnTrabajos,"Filtrar trabajos")


        # ---------------------------- Servicios y Seguros  ---------------------------------------------------------

        self.servicio=Servicio(self.frame_contenedor)
        self.servicio.grid(row=0,column=3,sticky="nsew")
        self.frame_contenedor.rowconfigure(0,weight=2)
        self.frame_contenedor.columnconfigure(4,weight=1)

        servicios_cabecera=tk.Label(
            self.servicio,
            text="Servicios     Seguros",
            bg="black",
            fg="white"
            )
        servicios_cabecera.grid(row=0,column=0,sticky="new")

        servyseg=tk.Frame(self.servicio)
        servyseg.grid(row=1,column=0)
        self.servicio.rowconfigure(1,weight=2)
        self.servicio.columnconfigure(0,weight=1)

        frame_vertodos= tk.Frame(servyseg)
        frame_vertodos.grid(
            row=0,
            column=0,
            pady=(0,5)
            )


        self.verlos = tk.Button(
            frame_vertodos,
            image=self.verServicios,
            cursor="hand2",
            relief="flat",
            command=lambda:self.servicio.cargar(),
            activebackground="black",
            activeforeground="white",
            text=" Todos",
            font=self.bold,
            compound="left",
            fg="#27455b"
            )
        self.verlos.grid(row=0,column=0,padx=(0,20))
        ToolTip(self.verlos,"Servicios registrados")

        self.verSeguros = tk.Button(
            frame_vertodos,
            image=self.verSegurosImg,
            cursor="hand2",
            relief="flat",
            command=lambda:self.servicio.cargarSeguros(),
            activebackground="black",
            activeforeground="white",
            text=" Todos",
            font=self.bold,
            compound="left",
            fg="#27455b"
            )
        self.verSeguros.grid(row=0,column=1)
        ToolTip(self.verSeguros,"Seguros registrados")

        frame_formularios=tk.Frame(servyseg)
        frame_formularios.grid(row=1,column=0)
        adaptable(servyseg,1,0)

        self.agrega = tk.Button(
            frame_formularios,
            image=self.service,
            cursor="hand2",
            relief="flat",
            command=lambda:self.servicio.agregar(),
            activebackground="black",
            activeforeground="white",
            text=" Formulario",
            font=self.bold,
            compound="left",
            fg="#27455b"
            )
        self.agrega.grid(row=0,column=0,pady=5,padx=(0,20))
        ToolTip(self.agrega,"Formulario Servicios")

        self.agregaSeguro = tk.Button(
            frame_formularios,
            image=self.seguro,
            cursor="hand2",
            relief="flat",
            command=lambda:seguros.agregar(self.taller, self.servicio, self.miBase),
            activebackground="black",
            activeforeground="white",
            text=" Formulario",
            font=self.bold,
            compound="left",
            fg="#27455b"
            )
        self.agregaSeguro.grid(row=0,column=1,pady=5)
        ToolTip(self.agregaSeguro,"Formulario Seguros")

        # ------------------------ stock -----------------------------------------------------

        self.stock=Stock(self.frame_contenedor)
        self.stock.grid(row=0,column=4,sticky="nsew")
        adaptable(self.frame_contenedor,0,3)

        stock_cabecera=tk.Label(
            self.stock,
            text="Stock",
            bg="black",
            fg="white"
            )
        stock_cabecera.grid(row=0,column=0,sticky="new")
        adaptable(self.stock,0,0)

        frame_stock=tk.Frame(self.stock)
        frame_stock.grid(row=1,column=0)
        adaptable(self.stock,1,0)

        self.verArticulos = tk.Button(
            frame_stock,
            image=self.categorias,
            cursor="hand2",
            relief="flat",
            command=lambda:self.stock.articulosStock(self.frameGrande,self.lista),
            activebackground="black",
            activeforeground="white",
            text=" Gestionar",
            font=self.bold,
            compound="left",
            fg="#27455b"
            )
        self.verArticulos.grid(row=0,column=0,padx=10,pady=(0,10),sticky="w")
        ToolTip(self.verArticulos,"Artículos, categorías, medidas y proveedores")

        self.verExistencias = tk.Button(
            frame_stock,
            image=self.existencias,
            cursor="hand2",
            relief="flat",
            command=lambda:self.stock.existenciasStock(self.frameGrande,self.lista),
            activebackground="black",
            activeforeground="white",
            text=" Existencias",
            font=self.bold,
            compound="left",
            fg="#27455b"
            )
        self.verExistencias.grid(row=1,column=0,padx=10,pady=(0,10),sticky="w")
        ToolTip(self.verExistencias,"Existencias")

        

        self.verMovimientos = tk.Button(
            frame_stock,
            image=self.movi,
            cursor="hand2",
            relief="flat",
            command=lambda:self.stock.movimientosStock(self.frameGrande,self.lista),
            activebackground="black",
            activeforeground="white",
            text=" Movimientos",
            font=self.bold,
            compound="left",
            fg="#27455b"
            )
        self.verMovimientos.grid(row=2,column=0,padx=10,pady=(0,10),sticky="w")
        ToolTip(self.verMovimientos,"Egresos e ingresos")

        
        # ------------------------- Frame pantalla ----------------------------------------

        self.frameGrande=tk.Frame(self,bd=2,relief="groove")
        self.frameGrande.grid(row=1,column=0,columnspan=5)
        self.rowconfigure(1,weight=4)

        self.frameDinamico=tk.Frame(self.frameGrande)
        self.frameDinamico.grid(row=0,column=0)

        label=tk.Label(self.frameDinamico,image=self.taller2,bg="white")
        label.grid(ipadx=700,ipady=290)


        """
        self.agregar=tk.PhotoImage(file="../img/agregar.png")
        self.editar=tk.PhotoImage(file="../img/editar.png")
        self.eliminar=tk.PhotoImage(file="../img/eliminar.png")
            

        self.botonAgregar=tk.Button(frame,image=self.agregar)
        self.botonAgregar.grid(row=1,column=0,padx=5,pady=10)
        ToolTip(self.botonAgregar,"Agregar")
        adaptable(frame,1,0)

        self.botonEditar=tk.Button(frame,image=self.editar)
        self.botonEditar.grid(row=1,column=1,padx=5,pady=10)
        ToolTip(self.botonEditar,"Editar")
        adaptable(frame,1,1)

        self.botonEliminar=tk.Button(frame,image=self.eliminar)
        self.botonEliminar.grid(row=1,column=2,padx=5,pady=10)
        ToolTip(self.botonEliminar,"Eliminar")
        adaptable(frame,1,2)"""


    def laficha(self):

        if self.cliente.var_entry_id.get():

            try:

                self.miCursor = self.miBase.cursor()
                consulta="SELECT * FROM datos_usuarios2 where documento=%s"
                self.miCursor.execute(consulta,self.cliente.var_entry_id.get())
                resultado = self.miCursor.fetchone()
            
                self.cliente.verLaFicha(resultado,self.lista,self.frameGrande)
               

            finally:

                self.miCursor.close()

        else:

            messagebox.showinfo("Atención","Ingrese un número válido")




    def reloj(self):

        dt=datetime.datetime.now()
        locale.setlocale(locale.LC_ALL,'es-ES')
        fecha=dt.strftime("%A %d de %B de %Y").capitalize()

        if fecha != self.actual:
            self.actual=fecha
            self.fecha.configure(text=fecha)


        time2 = time.strftime ('%H:%M:%S')
        if time2 != self.time1:
            self.time1 = time2
            self.clock.configure(text=time2)
        self.clock.after(500,self.reloj)

    


        

    def pantallaStock(self):



        """
        self.frameDinamico=ttk.Notebook(self.frameGrande)
        self.frameDinamico.grid(row=0,column=0,sticky="nsew")
        adaptable(self.frameGrande,0,0)

        self.existencias=tk.Frame(self.frameDinamico)
        self.frameDinamico.add(self.existencias,text="Existencias")

        
        self.categorias=tk.Frame(self.frameDinamico)
        self.frameDinamico.add(self.categorias,text="Categorías")

        self.articulos=tk.Frame(self.frameDinamico)
        self.frameDinamico.add(self.articulos,text="Artículos")

        self.movimientos=tk.Frame(self.frameDinamico)
        self.frameDinamico.add(self.movimientos,text="Movimientos")"""

        frameDinamico=tk.Frame(self.frameGrande)
        frameDinamico.grid(row=0,column=0,sticky="nsew")
        adaptable(self.frameGrande,0,0)

        self.existencias=tk.Frame(frameDinamico)
        self.existencias.grid(row=0,column=0,sticky="nsew")
        adaptable(frameDinamico,0,0)


        try:
            self.miCursor=self.miBase.cursor()

            self.miCursor.execute("SELECT * from articulos")
            resultado=self.miCursor.fetchall()

            if resultado:

                """frameContiene=tk.Frame(self.existencias)
                frameContiene.grid(row=0,column=0,sticky="nsew")
                adaptable(self.existencias,0,0)

                frameCampos=tk.Frame(frameContiene)
                frameCampos.grid(row=0,column=0,sticky="nsew")
                frameContiene.columnconfigure(0,weight=1)"""

                contenedor=tk.Frame(self.existencias)
                contenedor.grid(row=1,column=0,sticky="nsew")
                self.existencias.columnconfigure(0, weight=1)



                campos=("ID", "Categoría", "Nombre", "Medida","Precio","Existencias","Último\ningreso","Último\negreso")

                col=0
                for c in campos:

                    campo = tk.Label(
                        contenedor,
                        text=campos[col],
                        borderwidth=2,
                        relief="groove",
                        background="#5a98c4",
                        fg="white",
                        font=("verdana",11)
                        )

                    campo.grid(row=0,
                        column=col,
                        sticky="nsew"
                        )

                    contenedor.columnconfigure(col, weight=1)
                    col+=1



                    

                ingVar=tk.StringVar()
                egrVar=tk.StringVar()
                listado = {}
                row=1
                for ide,cat,nom,vol,med,pre,exi,ing,egr in resultado:

                    verDiaMesAnio(ing,ingVar)
                    verDiaMesAnio(egr,egrVar)
                    listado[ide] ={
                    "Id": tk.Label(
                        contenedor,
                        text=ide,
                        borderwidth=2,
                        relief="groove",
                        #width=6,
                        font=("verdana",11)
                        ),
                    "Categoria": tk.Label(
                        contenedor,
                        text=cat,
                        borderwidth=2,
                        relief="groove",
                        #width=30,
                        font=("verdana",11),
                        anchor="w"
                        ),
                    "Nombre": tk.Label(
                        contenedor,
                        text=nom,
                        borderwidth=2,
                        relief="groove",
                        #width=30,
                        font=("verdana",11)
                        ),
                    "Medida": tk.Label(
                        contenedor,
                        text="{} {}".format(vol,med),
                        borderwidth=2,
                        relief="groove",
                        #width=12,
                        font=("verdana",11)
                        ),
                    "Precio": tk.Label(
                        contenedor,
                        text=pre,
                        borderwidth=2,
                        relief="groove",
                        #width=10,
                        font=("verdana",11)
                        ),
                    "Existencias": tk.Label(
                        contenedor,
                        text=exi,
                        borderwidth=2,
                        relief="groove",
                        #width=10,
                        font=("verdana",11)
                        ),
                    "Ingreso": tk.Label(
                        contenedor,
                        text=ingVar.get(),
                        borderwidth=2,
                        relief="groove",
                        #width=11,
                        font=("verdana",11)
                        ),
                    "Egreso": tk.Label(
                        contenedor,
                        text=egrVar.get(),
                        borderwidth=2,
                        relief="groove",
                        #width=11,
                        font=("verdana",11)
                        )
                    }
                    listado[ide]["Id"].grid(row=row, column=0,ipady=5,sticky="nsew") 
                    listado[ide]["Categoria"].grid(row=row, column=1,ipady=5,sticky="nsew")
                    listado[ide]["Nombre"].grid(row=row, column=2,ipady=5,sticky="nsew")
                    listado[ide]["Medida"].grid(row=row, column=3,ipady=5,sticky="nsew")
                    listado[ide]["Precio"].grid(row=row, column=4,ipady=5,sticky="nsew")
                    listado[ide]["Existencias"].grid(row=row, column=5,ipady=5,sticky="nsew")
                    listado[ide]["Ingreso"].grid(row=row, column=6,ipady=5,sticky="nsew")
                    listado[ide]["Egreso"].grid(row=row, column=7,ipady=5,sticky="nsew")
                    row+=1
                    if row==4:
                        row=5

                    linea= tk.Frame(self.existencias)
                    linea.grid(
                        sticky="nse",
                        column=3,
                        row=1
                        )
                    self.existencias.rowconfigure(1, weight=1)




            else:

                self.pantallaLogo(self.frameGrande)
                   

        finally:
            self.miCursor.close()



    def pantallaStock2(self):


        frameDinamico=tk.Frame(self.frameGrande)
        frameDinamico.grid(row=0,column=0,sticky="nsew")
        adaptable(self.frameGrande,0,0)

        existencias=tablaExistencias(frameDinamico)
        existencias.grid(row=0,column=0)


    



