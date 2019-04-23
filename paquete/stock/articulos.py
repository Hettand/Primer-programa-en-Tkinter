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
siHayFrame=funcionalidades.siHayFrame
agregaFrame=funcionalidades.agregaFrame
cerrarFrame=funcionalidades.cerrarFrame
desactivar=funcionalidades.desactivar
activar=funcionalidades.activar
posicionar=funcionalidades.posicionar
cerrarToplevel=funcionalidades.cerrarToplevel
configuraToplevel=funcionalidades.configuraToplevel


class Articulos(Conexion,tk.Frame):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        
    def pantallaArticulos(self,frameGrande,lista):

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


        formArticulos=tk.Frame(frameIzquierdo)
        formArticulos.grid(row=2,column=0,sticky="nw")

        titArticulos=tk.Label(
            formArticulos,
            text="Gestión de artículos",
            bg="black",
            fg="white",
            bd=1
            )
        titArticulos.grid(row=0,column=0,sticky="nsew",ipady=5)

        frameFormulario=tk.Frame(formArticulos,bd=0)
        frameFormulario.grid(row=1,column=0,sticky="nsew")

        labels=["ID:", "Categoría:","Nombre:","Proveedor:","´Vólumen:","Medida:","Costo:"]
        i=0
        for l in labels:

            label=tk.Label(frameFormulario,text=labels[i])
            label.grid(row=i,column=0,sticky="e",pady=10,padx=10)

            i += 1


        self.IdVar=tk.StringVar()
        self.NomVar=tk.StringVar()
        self.presVar=tk.StringVar()
        self.costo=tk.StringVar()

        self.entryArt=tk.Entry(
            frameFormulario,
            width=8,
            textvariable=self.IdVar)
        self.entryArt.grid(row=0,column=1,sticky="w",padx=10)
        ArtId=tk.Button(
            frameFormulario,
            image=self.lupa,
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            command=lambda:self.buscar()
            )
        ArtId.grid(row=0,column=1)
        ToolTip(ArtId,"Buscar por ID")

        self.combo=ttk.Combobox(
            frameFormulario,
            values=self.selec_categoria(),
            state="readonly",
            width=18
            )
        self.combo.grid(row=1,column=1,sticky="w",padx=10)

        self.Cate=tk.Button(
            frameFormulario,
            image=self.gestionCat,
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            command=lambda:self.formularioCategorias()
            )
        self.Cate.grid(row=1,column=1,sticky="e",padx=(0,15))
        ToolTip(self.Cate,"Gestión de categorias")

        nombre=tk.Entry(
            frameFormulario,
            width=25,
            textvariable=self.NomVar
            )
        nombre.grid(row=2,column=1,sticky="w",padx=10)

        self.combo3=ttk.Combobox(
            frameFormulario,
            values=self.selec_proveedor(),
            state="readonly",
            width=18
            )
        self.combo3.grid(row=3,column=1,sticky="w",padx=10)

        self.Prov=tk.Button(
            frameFormulario,
            image=self.gestionProv,
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            command=lambda:self.FormularioProveedor()
            )
        self.Prov.grid(row=3,column=1,sticky="e",padx=(0,15))
        ToolTip(self.Prov,"Gestión de proveedores")

        presentacion=tk.Entry(
            frameFormulario,
            width=8,
            textvariable=self.presVar
            )
        presentacion.grid(row=4,column=1,sticky="w",padx=10)

        self.combo2=ttk.Combobox(
            frameFormulario,
            values=self.selec_medida(),
            state="readonly",
            width=18
            )
        self.combo2.grid(row=5,column=1,sticky="w",padx=10)

        self.Med=tk.Button(
            frameFormulario,
            image=self.gestionMed,
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            command=lambda:self.formularioMedida()
            )
        self.Med.grid(row=5,column=1,sticky="e",padx=(0,15))
        ToolTip(self.Med,"Gestión de medidas")

        elcosto=tk.Entry(frameFormulario,width=8,textvariable=self.costo)
        elcosto.grid(row=6,column=1,sticky="w",padx=10)

        frameBotones=tk.Frame(frameFormulario,bg="#214472")
        frameBotones.grid(row=8,column=0,columnspan=2,pady=(15,0),sticky="nsew")



        #botones
        
        funciones=(
            lambda:self.limpiar(),
            lambda:self.actualizar(),
            lambda:self.crear()
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

        

        # frame Tabla

        self.frameTabla=tk.Frame(self.frameDinamico,bg="")
        self.frameTabla.grid(row=0,column=2,sticky="nsew",padx=0)
        #self.frameDinamico.columnconfigure(1, weight=1)

        self.frame = tk.Frame(self.frameTabla)
        self.frame.grid(row=1,column=0)

        campos=tk.Frame(self.frame)
        campos.grid(row=0,column=0)

        listaCampos=["ID","Artículo","Categoría","Proveedor","Vólumen","Medida","Costo"]

        w=5
        n=0

        for l in listaCampos:

            labelCampo = tk.Label(
                campos,
                text=listaCampos[n],
                bd=1,
                width=w,
                bg="black",
                fg="white"
                )
            labelCampo.grid(row=0, column=n,ipady=5)

            n += 1

            if 1<=n<=3:
                w=25
            elif n==4:
                w=9
            elif n==5:
                w=12
            else:
                w=10
        

        self.crearFrame()
        

    def selec_categoria(self):

        #lista desplegable de categorias

        try:
            self.miCursor = self.miBase.cursor()
            self.miCursor.execute("SELECT * FROM categorias order by id")
            categorias=self.miCursor.fetchall()

            lista = []
            n=0
            for c in categorias:
                
                lista.append("{}.{}".format(categorias[n][0],categorias[n][1]))
                n += 1
            return lista


        finally:

            self.miCursor.close()


    def selec_medida(self):

        #lista desplegable de medidas

        try:
            self.miCursor = self.miBase.cursor()
            self.miCursor.execute("SELECT * FROM medidas order by id ASC")
            medidas=self.miCursor.fetchall()

            lista = []
            n=0
            for m in medidas:
                
                lista.append("{}.{}".format(medidas[n][0],medidas[n][1]))
                n += 1
            return lista


        finally:

            self.miCursor.close()

    def limpiar(self):

        self.entryArt.config(state="normal")

        self.IdVar.set("")
        self.combo.set("")
        self.NomVar.set("")
        self.combo2.set("")
        self.combo3.set("")
        self.presVar.set("")
        self.costo.set("")


    def buscar(self):

        if self.IdVar.get():

            try:
                
                self.miCursor = self.miBase.cursor()
                

                
                    
                self.miCursor.execute(# buscar por id
                    "SELECT * FROM articulos where idArt = %s;",
                    self.IdVar.get()
                    )
                resultado = self.miCursor.fetchone()
                self.IdVar.set(resultado[0])
                self.NomVar.set(resultado[1])
                self.presVar.set(resultado[4])
                self.costo.set(resultado[6])

                

                self.miCursor.execute(# según el resultado muestro categoria con su id
                    "SELECT * from categorias where id=%s",
                    resultado[2]
                    )
                resultado2=self.miCursor.fetchone()
                
                if resultado2:

                    self.combo.set("{}.{}".format(resultado2[0],resultado2[1]))

                self.miCursor.execute(# segun resultado muestro medida con su id
                    "SELECT id,distribuidora from proveedores where id=%s",resultado[3]
                    )
                resultado4=self.miCursor.fetchone()

                if resultado4:

                    self.combo3.set("{}.{}".format(resultado4[0],resultado4[1]))

                self.miCursor.execute(# segun resultado muestro medida con su id
                    "SELECT * from medidas where id=%s",resultado[5]
                    )
                resultado3=self.miCursor.fetchone()

                if resultado3:

                    self.combo2.set("{}.{}".format(resultado3[0],resultado3[1]))

                self.entryArt.config(state="disable")
            
            except pymysql.err.DataError:
                self.limpiar()
                messagebox.showerror("Error", "Datos incorrectos")
                

            except TypeError:
                self.limpiar()
                messagebox.showinfo("Atencion", "Artículo no encontrado")
           

            finally:
                
                self.miCursor.close()


    def actualizar(self):


        if self.combo.get() and self.NomVar.get() and self.combo2.get() and self.combo3.get() and self.presVar.get() and self.costo.get():

            try:
                
                self.miCursor = self.miBase.cursor()
                
                self.miCursor.execute(
                    "SELECT * FROM articulos where idArt = %s",
                    self.IdVar.get()
                    )
                encontrado=self.miCursor.fetchone()

                
                if encontrado:
                    consulta = "UPDATE articulos set nombre=(%s),idCat=(%s),idProv=(%s),cantidad=(%s),medida=(%s),costo=(%s) where idArt=(%s)"

                    # tomar el id de cada combobox para guardarlo
                    separados=self.combo.get().split(".")
                    separados2=self.combo2.get().split(".")
                    separados3=self.combo3.get().split(".")

                    self.miCursor.execute(
                        consulta,
                        (
                            self.NomVar.get(),
                            separados[0],
                            separados3[0],
                            self.presVar.get(),
                            separados2[0],
                            self.costo.get(),
                            self.IdVar.get()
                            )
                        )

                    medida="{} {}".format(self.presVar.get(),separados2[0])

                    consulta2="UPDATE existencias set cantidad=(%s) where id=%s"

                    self.miCursor.execute(
                        consulta2,
                        (medida,self.IdVar.get())
                        )

                    messagebox.showinfo(
                        "Información", 
                        "{}\nActualizado con éxito".format(
                            self.NomVar.get()
                            )
                        )

                    self.miCursor.execute("SELECT idArt FROM articulos")
                    cantidad=self.miCursor.fetchall()

                    self.limpiar()

                    if len(cantidad) > 1:

                        self.eliminaFrame(cantidad)

                    self.crearFrame()
                else:
                    messagebox.showinfo("Atencion","Ingrese un registro válido")

            except pymysql.err.IntegrityError:

                messagebox.showerror("Error","Registro duplicado")

            finally:

                self.miBase.commit()
                self.miCursor.close()

        else:

            messagebox.showinfo("Aviso","Faltan datos")


    def crear(self):



        if self.NomVar.get() and self.combo.get() and self.combo2.get() and self.combo3.get() and self.presVar.get().isdigit() and self.costo.get().isdigit():

            try:
                
                self.miCursor = self.miBase.cursor()


                consulta= "INSERT INTO articulos (nombre,idCat,idProv,cantidad,medida,costo) values(%s,%s,%s,%s,%s,%s)"

                separados=self.combo.get().split(".")
                separados2=self.combo2.get().split(".")
                separados3=self.combo3.get().split(".")

                


                self.miCursor.execute(consulta, 
                    (
                        self.NomVar.get(),
                        separados[0],
                        separados3[0],
                        self.presVar.get(),
                        separados2[0],
                        self.costo.get()
                        )
                    )

                messagebox.showinfo("Nuevo artículo","{}".format(self.NomVar.get()))

                self.miBase.commit()

                self.miCursor.execute("SELECT idArt FROM articulos where nombre=%s",self.NomVar.get())
                articulo=self.miCursor.fetchone()

                consulta2="INSERT INTO existencias (id,existencias,cantidad) values(%s,%s,%s)"

                self.miCursor.execute(
                    consulta2,
                    (
                        articulo[0],
                        0,
                        "{} {}".format(self.presVar.get(), separados2[0])
                    )
                    )

                self.miCursor.execute("SELECT idArt FROM articulos")
                cantidad=self.miCursor.fetchall()

                if len(cantidad) > 1:

                    self.eliminaFrame(cantidad)

                self.crearFrame()

                self.limpiar()




            except pymysql.err.IntegrityError:
                messagebox.showerror(
                    "Error", 
                    "Intenta ingresar un artículo ya existente\nVerifique"
                    )
                self.miCursor.execute("SELECT idArt from articulos")
                num = self.miCursor.fetchall()
                self.miCursor.execute("ALTER TABLE articulos auto_increment = %s",
                    len(num)
                    )

                


            finally:
                self.miBase.commit()
                self.miCursor.close()
                self.limpiar()

        else:

            messagebox.showerror("Error","Ingreso de datos incorrecto")
            
        


    def crearFrame(self):

        try:

            self.miCursor = self.miBase.cursor()
            self.miCursor.execute("SELECT * FROM articulos order by idArt ASC")
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
                for ide,nom,cat,prov,cant,med,costo in resultado:

                    self.miCursor.execute("SELECT nombre from categorias where id=%s",cat)
                    categoria=self.miCursor.fetchone()

                    self.miCursor.execute("SELECT distribuidora from proveedores where id=%s",prov)
                    proveedor=self.miCursor.fetchone()

                    self.miCursor.execute("SELECT medida from medidas where id=%s",med)
                    medida=self.miCursor.fetchone()
                
                    listado[ide] ={
                    "Id": tk.Label(
                        self.contenedor,
                        text=ide,
                        bd=1,
                        relief="sunken",
                        width=5
                        ),
                    "Articulo": tk.Label(
                        self.contenedor,
                        text=nom,
                        bd=1,
                        relief="sunken",
                        width=25
                        ),
                    "Categoria": tk.Label(
                        self.contenedor,
                        text=categoria,
                        bd=1,
                        relief="sunken",
                        width=25
                        ),
                    "Proveedor": tk.Label(
                        self.contenedor,
                        text=proveedor[0],
                        bd=1,
                        relief="sunken",
                        width=25
                        ),
                    "Cantidad": tk.Label(
                        self.contenedor,
                        text=cant,
                        bd=1,
                        relief="sunken",
                        width=9
                        ),
                    "Medida": tk.Label(
                        self.contenedor,
                        text=medida,
                        bd=1,
                        relief="sunken",
                        width=12
                        ),
                    "Costo": tk.Label(
                        self.contenedor,
                        text=costo,
                        bd=1,
                        relief="sunken",
                        width=10
                        )
                    
                    }
                    listado[ide]["Id"].grid(row=row, column=0,ipady=5)
                    listado[ide]["Articulo"].grid(row=row, column=1,ipady=5) 
                    listado[ide]["Categoria"].grid(row=row, column=2,ipady=5)
                    listado[ide]["Proveedor"].grid(row=row, column=3,ipady=5)
                    listado[ide]["Cantidad"].grid(row=row, column=4,ipady=5)
                    listado[ide]["Medida"].grid(row=row, column=5,ipady=5)
                    listado[ide]["Costo"].grid(row=row, column=6,ipady=5)
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
        except:
            messagebox.showinfo("Atencion","No hay datos")

        finally:

            self.miCursor.close()

    

    def eliminaFrame(self,cantidad):

        #para poder actualizar el frame cuando se hacen cambios

        self.contenedor.destroy()

        if len(cantidad) > 18:

                self.frameScroll.destroy()
                self.canvas.destroy()


    def formularioMedida(self):

        desactivar(self.Med)

        formMedidas=tk.Toplevel(self.frameDinamico)
        formMedidas.protocol(
                "WM_DELETE_WINDOW",
                lambda:cerrarToplevel(self.Med,self.lista,formMedidas)
                )
        configuraToplevel(formMedidas,self.lista,self,"Medidas")

        self.IdMedida=tk.StringVar()
        self.Tipo=tk.StringVar()

        titMedidas=tk.Label(
            formMedidas,
            text="Gestión de medidas",
            bg="black",
            fg="white"
            )
        titMedidas.grid(row=0,column=0,columnspan=5,sticky="nsew")

        medidaId=tk.Label(formMedidas,text="ID:")
        medidaId.grid(row=1,column=0,sticky="e",pady=10,padx=10)

        self.Mid=tk.Entry(
            formMedidas,
            width=5,
            textvariable=self.IdMedida)
        self.Mid.grid(row=1,column=1,sticky="w",padx=10)

        medidaId=tk.Button(
            formMedidas,
            image=self.lupa,
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            command=lambda:self.buscarMedida()
            )
        medidaId.grid(row=1,column=2)
        ToolTip(medidaId,"Buscar por ID")

        medtipo=tk.Label(formMedidas,text="Medida:")
        medtipo.grid(row=1,column=3,sticky="e",pady=10,padx=(25,10))

        Mtipo=tk.Entry(
            formMedidas,
            width=16,
            textvariable=self.Tipo)
        Mtipo.grid(row=1,column=4,sticky="w",padx=12)

        frameBotones2=tk.Frame(formMedidas,bg="#214472")
        frameBotones2.grid(row=2,column=0,columnspan=5,pady=(15,0),sticky="nsew")

        

        funciones2=(
            lambda:self.limpiaMedida(),
            lambda:self.actualizaMedida(),
            lambda:self.crearMedida()
            )
        n=0
        for i in self.imagenes:
            boton2=tk.Button(
                frameBotones2,
                image=self.imagenes[n],
                command=funciones2[n],
                cursor="hand2",
                relief="flat",
                bg="#214472",
                activebackground="black",
                activeforeground="white",
                text=self.texto[n],
                font=self.bold,
                fg="white",
                compound="left"
                )
            boton2.grid(row=0,pady=5,padx=10,column=n)
            n+=1

    def limpiaMedida(self):

        self.Med.config(state="normal")

        self.IdMedida.set("")
        self.Tipo.set("")
    


    def actualizaMedida(self):


        if self.IdMedida.get() and self.Tipo.get():

            responde=messagebox.askyesno("Cambiar","Estos cambios afectarán también a los articulos\n¿Hacer los cambios?")

            if responde:

                try:
                    
                    self.miCursor = self.miBase.cursor()
                    
                    self.miCursor.execute(
                        "SELECT * FROM medidas where id = %s",
                        self.IdMedida.get()
                        )
                    encontrado=self.miCursor.fetchone()

                    
                    if encontrado:

                        self.miCursor.execute("UPDATE medidas set medida=(%s) where id=(%s)",
                            (
                                self.Tipo.get(),
                                encontrado[0]
                            )
                        )

                        self.combo2.config(values=self.selec_medida())

                        

                        messagebox.showinfo(
                            "Información", 
                            "{}\nActualizado con éxito".format(
                                self.Tipo.get()
                                )
                            )

                        self.miCursor = self.miBase.cursor()

                        self.miCursor.execute("SELECT idArt FROM articulos")
                        cantidad=self.miCursor.fetchall()

                        self.limpiaMedida()
                        self.eliminaFrame(cantidad)
                        self.crearFrame()
                    else:
                        messagebox.showinfo("Atencion","Ingrese un registro válido")

                finally:

                    self.miBase.commit()
                    self.miCursor.close()

        else:

            messagebox.showinfo("Aviso","Faltan datos")
    

    def crearMedida(self):


        if self.Tipo.get():

            try:
                
                self.miCursor = self.miBase.cursor()
                self.miCursor.execute("INSERT INTO medidas (id,medida) values(null,%s)",self.Tipo.get())

                messagebox.showinfo("Nueva","Unidad de medida: {}".format(self.Tipo.get()))


            except pymysql.err.DataError:
                messagebox.showerror("Error","Datos incorrectos")

            except pymysql.err.InternalError:
                messagebox.showerror("Error","Datos incorrectos")
                
            except pymysql.err.IntegrityError:
                messagebox.showerror(
                    "Error", 
                    "Intenta ingresar un artículo ya existente\nVerifique"
                    )
              


            finally:
                self.miBase .commit()
                self.miCursor.close()
                self.limpiaMedida()
                self.combo2.config(values=self.selec_medida())

        else:

            messagebox.showerror("Error","Faltan datos")


    def buscarMedida(self):

        try:
            
            self.miCursor = self.miBase.cursor()
            

            if self.IdMedida.get():
                
                self.miCursor.execute(
                    "SELECT * FROM medidas where id = %s;",
                    self.IdMedida.get()
                    )
                resultado = self.miCursor.fetchone()
                self.IdMedida.set(resultado[0])
                self.Tipo.set(resultado[1])

                self.Mid.config(state="disable")
        
        except pymysql.err.DataError:
            self.limpiaMedida()
            messagebox.showerror("Error", "Datos incorrectos")
            

        except TypeError:
            self.limpiaMedida()
            messagebox.showinfo("Atencion", "Artículo no encontrado")
       

        finally:
            
            self.miCursor.close()


    def formularioCategorias(self):

        desactivar(self.Cate)

        formCategorias=tk.Toplevel(self.frameDinamico)
        formCategorias.protocol(
                "WM_DELETE_WINDOW",
                lambda:cerrarToplevel(self.Cate,self.lista,formCategorias)
                )
        configuraToplevel(formCategorias,self.lista,self,"Gestión de categorías")


        

        titCat=tk.Label(
            formCategorias,
            text="Categorías",
            bg="black",
            fg="white"
            )
        titCat.grid(row=0,column=0,columnspan=2,sticky="nsew")

        labelId=tk.Label(formCategorias,text="ID:")
        labelId.grid(row=1,column=0,sticky="e",pady=10,padx=10)
        labelNom=tk.Label(formCategorias,text="Nombre:")
        labelNom.grid(row=2,column=0,sticky="e",pady=10,padx=10)

        self.catVar=tk.StringVar()
        self.catNomVar=tk.StringVar()

        self.entryId=tk.Entry(
            formCategorias,
            width=5,
            textvariable=self.catVar)
        self.entryId.grid(row=1,column=1,sticky="w",padx=10)

        buscaCat=tk.Button(
            formCategorias,
            image=self.lupa,
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            command=lambda:self.buscarCategoria()
            )
        buscaCat.grid(row=1,column=1)
        ToolTip(buscaCat,"Buscar por ID")

        self.nombre=tk.Entry(
            formCategorias,
            width=25,
            textvariable=self.catNomVar
            )
        self.nombre.grid(row=2,column=1,sticky="w",padx=(10,30))

        frameBotones3=tk.Frame(formCategorias,bg="#214472")
        frameBotones3.grid(row=3,column=0,columnspan=2,sticky="nsew")

        #botones
        funciones3=(
            lambda:self.limpiaCategoria(),
            lambda:self.actualizaCategoria(),
            lambda:self.crearCategoria()
            )
        n=0
        for t in self.texto:
            boton3=tk.Button(
                frameBotones3,
                image=self.imagenes[n],
                command=funciones3[n],
                cursor="hand2",
                relief="flat",
                bg="#214472",
                activebackground="black",
                activeforeground="white",
                text=self.texto[n],
                font=self.bold,
                fg="white",
                compound="left"
                )
            boton3.grid(row=0,pady=5,padx=10,column=n)
            n+=1


    def limpiaCategoria(self):

        self.catVar.set("")
        self.catNomVar.set("")
        self.entryId.config(state="normal")


    def buscarCategoria(self):

        try:
            
            self.miCursor = self.miBase.cursor()
            

            if self.entryId.get():
                
                self.miCursor.execute(
                    "SELECT * FROM categorias where id = %s;",
                    self.entryId.get()
                    )
                resultado = self.miCursor.fetchone()
                self.catVar.set(resultado[0])
                self.catNomVar.set(resultado[1])
                self.entryId.config(state="disable")
        
        except pymysql.err.DataError:
            self.limpiaCategoria()
            messagebox.showerror("Error", "Datos incorrectos")
            

        except TypeError:
            self.limpiaCategoria()
            messagebox.showinfo("Atencion", "Categoría no encontrada")
       

        finally:
            
            self.miBase.commit()
            self.miCursor.close()


    def actualizaCategoria(self):

        
        if self.catNomVar.get() and self.catVar.get():

            responde=messagebox.askyesno("Cambiar","Estos cambios afectarán también a los articulos\n¿Hacer los cambios?")

            if responde:

                try:
                    
                    self.miCursor = self.miBase.cursor()
                    
                    buscado=self.miCursor.execute(
                        "SELECT * FROM categorias where id = %s",
                        self.catVar.get()
                        )
                    encontrado=self.miCursor.fetchone()

                    
                    if encontrado:

                        consulta = "UPDATE categorias set nombre=(%s) where id=(%s)"
                        self.miCursor.execute(
                            consulta,
                            (self.catNomVar.get(),self.catVar.get()
                                )
                            )

                        messagebox.showinfo(
                            "Información", 
                            "Categoría {}\nActualizada con éxito".format(
                                self.catNomVar.get()
                                )
                            )

                        self.miCursor.execute("SELECT id FROM categorias")
                        cantidad=self.miCursor.fetchall()

                        self.limpiaCategoria()
                        self.eliminaFrame(cantidad)
                        self.crearFrame()
                    else:
                        messagebox.showinfo("Atencion","Ingrese un registro válido")

                finally:

                    self.miBase.commit()
                    self.miCursor.close()
                    self.combo3.config(values=self.selec_categoria())

        else:
            messagebox.showinfo("Aviso","Faltan datos")


    def crearCategoria(self):

        try:
            
            self.miCursor = self.miBase.cursor()
            consulta= "INSERT INTO categorias (id,nombre) values(null,%s)"
            self.miCursor.execute(consulta, self.catNomVar.get())

            messagebox.showinfo("Nuevo servicio","{}".format(self.catNomVar.get()))

            self.miCursor.execute("SELECT * FROM categorias")
            cantidad=self.miCursor.fetchall()

    
            self.eliminaFrame(cantidad)
            self.crearFrame()

            self.limpiaCategoria()

        except pymysql.err.DataError:
            messagebox.showerror("Error","Datos incorrectos")

        except pymysql.err.InternalError:
            messagebox.showerror("Error","Datos incorrectos")
            
        except pymysql.err.IntegrityError:
            messagebox.showerror(
                "Error", 
                "Intenta ingresar una categoría ya existente\nVerifique"
                )
            self.miCursor.execute("SELECT id from categorias")
            num = self.miCursor.fetchall()
            self.miCursor.execute("ALTER TABLE categorias auto_increment = %s",
                len(num)
                )


        finally:
            self.miBase.commit()
            self.miCursor.close()
            self.limpiaCategoria()
            self.combo.config(values=self.selec_categoria())


# ------------------- Proveedores -----------------------------------------------

    def FormularioProveedor(self):

        desactivar(self.Prov)

        formProveedores=tk.Toplevel(self.frameDinamico)
        formProveedores.protocol(
                "WM_DELETE_WINDOW",
                lambda:cerrarToplevel(self.Prov,self.lista,formProveedores)
                )
        configuraToplevel(formProveedores,self.lista,self,"Proveedores")

        self.IdProveedor=tk.StringVar()
        self.distribuidora=tk.StringVar()
        self.elProveedor=tk.StringVar()
        self.contactoProveedor=tk.StringVar()

        titProveedores=tk.Label(
            formProveedores,
            text="Gestión de proveedores",
            bg="black",
            fg="white"
            )
        titProveedores.grid(row=0,column=0,columnspan=5,sticky="nsew")

        proveedorId=tk.Label(formProveedores,text="ID:")
        proveedorId.grid(row=1,column=0,sticky="e",pady=10,padx=10)

        self.Proved=tk.Entry(
            formProveedores,
            width=5,
            textvariable=self.IdProveedor
            )
        self.Proved.grid(row=1,column=1,sticky="w",padx=10)

        provId=tk.Button(
            formProveedores,
            image=self.lupa,
            cursor="hand2",
            relief="flat",
            activebackground="black",
            activeforeground="white",
            command=lambda:self.buscarProveedor()
            )
        provId.grid(row=1,column=1)
        ToolTip(provId,"Buscar por ID")

        nombreDistribuidora=tk.Label(formProveedores,text="Distribuidora:")
        nombreDistribuidora.grid(row=2,column=0,sticky="e",pady=10,padx=10)

        elEntry=tk.Entry(
            formProveedores,
            width=25,
            textvariable=self.distribuidora)
        elEntry.grid(row=2,column=1,sticky="w",padx=10)

        nombreContacto=tk.Label(formProveedores,text="Contacto:")
        nombreContacto.grid(row=3,column=0,sticky="e",pady=10,padx=10)

        elEntry2=tk.Entry(
            formProveedores,
            width=30,
            textvariable=self.elProveedor)
        elEntry2.grid(row=3,column=1,sticky="w",padx=10)

        numeroContacto=tk.Label(formProveedores,text="Teléfono:")
        numeroContacto.grid(row=4,column=0,sticky="e",pady=10,padx=10)

        elEntry3=tk.Entry(
            formProveedores,
            width=12,
            textvariable=self.contactoProveedor)
        elEntry3.grid(row=4,column=1,sticky="w",padx=10)


        frameBotones4=tk.Frame(formProveedores,bg="#214472")
        frameBotones4.grid(row=5,column=0,columnspan=3,pady=(15,0),sticky="nsew")

        

        funciones4=(
            lambda:self.limpiaProveedor(),
            lambda:self.actualizaProveedor(),
            lambda:self.crearProveedor()
            )
        n=0
        for i in self.imagenes:
            boton4=tk.Button(
                frameBotones4,
                image=self.imagenes[n],
                command=funciones4[n],
                cursor="hand2",
                relief="flat",
                bg="#214472",
                activebackground="black",
                activeforeground="white",
                text=self.texto[n],
                font=self.bold,
                fg="white",
                compound="left"
                )
            boton4.grid(row=0,pady=5,padx=10,column=n)
            n+=1

    def limpiaProveedor(self):

        self.Prov.config(state="normal")

        self.IdProveedor.set("")
        self.distribuidora.set("")
        self.elProveedor.set("")
        self.contactoProveedor.set("")
    


    def actualizaProveedor(self):


        if self.IdProveedor.get() and self.distribuidora.get() and self.elProveedor.get() and self.contactoProveedor.get():

            responde=messagebox.askyesno("Cambiar","Estos cambios afectarán también a los articulos\n¿Hacer los cambios?")

            if responde:

                try:
                    
                    self.miCursor = self.miBase.cursor()
                    
                    self.miCursor.execute(
                        "SELECT * FROM proveedores where id = %s",
                        self.IdProveedor.get()
                        )
                    encontrado=self.miCursor.fetchone()

                    
                    if encontrado:

                        self.miCursor.execute("UPDATE proveedores set distribuidora=(%s),contacto=(%s),tel=(%s) where id=(%s)",
                            (
                                self.distribuidora.get(),
                                self.elProveedor.get(),
                                self.contactoProveedor.get(),
                                encontrado[0]
                            )
                        )

                        self.combo3.config(values=self.selec_proveedor())

                        

                        messagebox.showinfo(
                            "Información", 
                            "{}\nActualizado con éxito".format(
                                self.elProveedor.get()
                                )
                            )

                        self.miCursor = self.miBase.cursor()

                        self.miCursor.execute("SELECT idArt FROM articulos")
                        cantidad=self.miCursor.fetchall()

                        self.limpiaMedida()
                        self.eliminaFrame(cantidad)
                        self.crearFrame()
                    else:
                        messagebox.showinfo("Atencion","Ingrese un registro válido")

                finally:

                    self.miBase.commit()
                    self.miCursor.close()

        else:

            messagebox.showinfo("Aviso","Faltan datos")
        

    def crearProveedor(self):


        if self.distribuidora.get() and self.elProveedor.get() and self.contactoProveedor.get():

            try:
                
                self.miCursor = self.miBase.cursor()
                insertar="INSERT INTO proveedores (id,distribuidora,contacto,tel) values(null,%s,%s,%s)"
                self.miCursor.execute(insertar,
                    (
                    self.distribuidora.get(),
                    self.elProveedor.get(),
                    self.contactoProveedor.get()
                    )
                    )

                messagebox.showinfo("Nuevo","Proveedor: {}".format(self.distribuidora.get()))


            except pymysql.err.DataError:
                messagebox.showerror("Error","Datos incorrectos")

            except pymysql.err.InternalError:
                messagebox.showerror("Error","Datos incorrectos")
                
            except pymysql.err.IntegrityError:
                messagebox.showerror(
                    "Error", 
                    "Intenta ingresar un artículo ya existente\nVerifique"
                    )
              


            finally:
                self.miBase .commit()
                self.miCursor.close()
                self.limpiaProveedor()
                self.combo3.config(values=self.selec_proveedor())

        else:

            messagebox.showerror("Error","Faltan datos")


    def buscarProveedor(self):

        if self.IdProveedor.get():

            try:
                
                self.miCursor = self.miBase.cursor()

                    
                self.miCursor.execute(
                    "SELECT * FROM proveedores where id = %s;",
                    self.IdProveedor.get()
                    )
                resultado = self.miCursor.fetchone()
                self.IdProveedor.set(resultado[0])
                self.distribuidora.set(resultado[1])
                self.elProveedor.set(resultado[2])
                self.contactoProveedor.set(resultado[3])

                self.Proved.config(state="disable")
        
            except pymysql.err.DataError:
                self.limpiaMedida()
                messagebox.showerror("Error", "Datos incorrectos")
                

            except TypeError:
                self.limpiaMedida()
                messagebox.showinfo("Atencion", "Proveedor no encontrado")
           

            finally:
                
                self.miCursor.close()



    def selec_proveedor(self):

        #lista desplegable de medidas

        try:
            self.miCursor = self.miBase.cursor()
            self.miCursor.execute("SELECT id,distribuidora FROM proveedores order by id ASC")
            proveedores=self.miCursor.fetchall()

            lista = []
            n=0
            for p in proveedores:
                
                lista.append("{}.{}".format(proveedores[n][0],proveedores[n][1]))
                n += 1
            return lista


        finally:

            self.miCursor.close()


