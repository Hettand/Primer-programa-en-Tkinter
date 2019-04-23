import sys
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import pymysql


sys.path.insert(1,"../conexion")
import conexion
sys.path.insert(2,"../panel")
import panel
import funcionalidades
sys.path.insert(1,"../trabajos")
import trabajos
sys.path.insert(1,"../servicios")
import servicios



Conexion=conexion.Conexion
Panel=panel.Panel
Trabajo=trabajos.Trabajo
Servicio=servicios.Servicio
adaptable=funcionalidades.adaptable

        

class Aplicacion(Conexion,tk.Frame):



    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        # -------------------------------- formulario de acceso ------------------------------------------------

        self.frame_inicio = tk.Frame(self,bg="black")
        self.frame_inicio.grid(row=0,column=0)

        logo=tk.Label(self.frame_inicio,bg="black",image=self.taller2)
        logo.grid(row=0,column=0,pady=20)

        label_usuario=tk.Label(
            self.frame_inicio,
            text="Usuario",
            bg="black",
            fg="white"
            )
        label_usuario.grid(row=1,column=0,sticky="nsew",pady=10)
        entry_usuario=tk.Entry(self.frame_inicio,font=self.font)
        entry_usuario.grid(row=2,column=0,pady=5,padx=60)

        label_contra=tk.Label(
            self.frame_inicio,
            text="Contraseña",
            bg="black",
            fg="white"
            )
        label_contra.grid(row=3,column=0,sticky="nsew",pady=10)
        entry_contra=tk.Entry(self.frame_inicio,font=self.font,show="*")
        entry_contra.grid(row=4,column=0,pady=5)


        boton_panel = tk.Button(
            self.frame_inicio,
            text="Acceder",
            bd=2,
            cursor="hand2",
            command=lambda:self.panel_c(),
            bg="#5a98c4",
            fg="white",
            activebackground="black",
            activeforeground="white"            
            )
        boton_panel.grid(row=5,column=0,pady=30)

        

        #------------------------ fin de formulario de acceso -------------------------------------------------------------------------

        self.pack(expand=1)



    def panel_c(self):

        """

        def progress(currentValue):
            progressbar["value"]=currentValue

        maxValue=100

        s = ttk.Style()
        s.theme_use('clam')
        s.configure("blue.Horizontal.TProgressbar", foreground='blue', background='blue')

        progressbar=ttk.Progressbar(self.frame_inicio,style="blue.Horizontal.TProgressbar",orient="horizontal",length=300,mode="determinate")
        progressbar.grid(row=5,padx=20)

        currentValue=0
        progressbar["value"]=currentValue
        progressbar["maximum"]=maxValue

        divisions=10
        for i in range(divisions):
            currentValue=currentValue+10
            progressbar.after(500, progress(currentValue))
            progressbar.update()

        progressbar.destroy()

        """
        self.frame_inicio.grid_forget()
        #panel de gestion de los datos

        self.panel = Panel(self)
        self.panel.grid(row=0,column=0)        

        self.Usuario=tk.Frame(self.panel,bg="black")
        self.Usuario.grid(row=0,column=0,sticky="nsew")
        self.panel.rowconfigure(0, weight=2)

        labelFoto=tk.Label(self.Usuario,image=self.femenino,fg="white",bg="black")
        labelFoto.grid(row=0,column=0,padx=22,pady=5)
        adaptable(self.Usuario,0,0)


        labelUsu=tk.Label(
            self.Usuario,
            fg="white",
            bg="black",
            text=self.elUsuario
            )
        labelUsu.grid(row=1,column=0)
        adaptable(self.Usuario,1,0)




        cerrar_c =tk.Button(
            self.Usuario,
            text="Cerrar sesión",
            font=("verdana",9),
            command=lambda:self.cerrar_panel(),
            background="#5a98c4",
            fg="white"
            )
        cerrar_c.grid(row=2,column=0,pady=8)
        adaptable(self.Usuario,2,0)

       
            
    def cerrar_panel(self):

        #cerrar panel
        self.panel.grid_forget()

        self.Usuario.grid_forget()
        self.frame_inicio.grid()


    
#------------raiz y  aplicacion dentro de la raiz-------------------



if __name__ == "__main__":

    raiz = tk.Tk()
    raiz.title("Gestor de datos")
    raiz.iconbitmap("../img/icono.ico")
    raiz.geometry("+%d+%d" % (0,0)) 
    fuente=("verdana",12)
    raiz.option_add("*Font",fuente)
    fondo="#fff"
    raiz.option_add("*Background",fondo)



    


    

    """def preguntar():

        if messagebox.askokcancel("Salir", "Salir del programa?"):
            raiz.destroy()

    raiz.protocol(
        "WM_DELETE_WINDOW",
        preguntar
        )"""

    app = Aplicacion(raiz)
    app.mainloop()