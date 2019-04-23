from screeninfo import get_monitors
import tkinter as tk

def agregaFrame(frame,lista):

    lista.append(frame)


def siHayFrame(lista):

    if lista:

        n=0

        for l in lista:

            lista[n].destroy()
            lista.pop(n)
            n += 1

def cerrarFrame(lista):

    siHayFrame(lista)


        




def verDiaMesAnio(fecha_guardada,variable):

    #mostrar en formato dd-mm-aaaa la fecha guardada como aaaa-mm-dd 

    cadena=str(fecha_guardada)
    lista=cadena.split("-")
    ver_fecha="{}-{}-{}".format(lista[2],lista[1],lista[0])
    variable.set(ver_fecha)


def guardaAnioMesDia(fecha_ingresada,auxiliar):


    lista=fecha_ingresada.split("-")
    lista2="{}-{}-{}".format(lista[2],lista[1],lista[0])
    auxiliar.set(lista2)


def adaptable(elemento,fila,columna):

    elemento.rowconfigure(fila,weight=1)
    elemento.columnconfigure(columna,weight=1)





def posicionar(root):

    w = root.winfo_reqwidth()
    h = root.winfo_reqheight()
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/3) - (w/2)
    y = (hs/3) - (h/2)
    root.geometry('+%d+%d' % (x, y))


def desactivar(boton):

    boton.config(state="disabled")

def activar(boton):

    boton.config(state="normal")


def cerrarToplevel(boton,lista,frame):

    #cerrar top level y eliminarlo de la lista, activar el boton

    activar(boton)

    if frame in lista:

        indice=lista.index(frame)
        lista.pop(indice)
        frame.destroy()


def configuraToplevel(Toplevel,lista,root,titulo):

    #hacer que el toplevel se posicione y se agregue a la lista

    Toplevel.resizable(0,0)
    Toplevel.transient(root)
    Toplevel.title(titulo)
    posicionar(Toplevel)
    agregaFrame(Toplevel,lista)












