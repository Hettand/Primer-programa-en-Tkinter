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
import articulos
import existencias
import movimientos

Conexion=conexion.Conexion
adaptable=funcionalidades.adaptable
siHayFrame=funcionalidades.siHayFrame
agregaFrame=funcionalidades.agregaFrame
cerrarFrame=funcionalidades.cerrarFrame
Articulos=articulos.Articulos
Existencias=existencias.Existencias
Movimientos=movimientos.Movimientos


class Stock(Conexion,tk.Frame):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        
    def articulosStock(self,frameGrande,lista):

        self.Articulos=Articulos(frameGrande)
        self.Articulos.grid()

        siHayFrame(lista)
        self.Articulos.pantallaArticulos(frameGrande,lista)


    def existenciasStock(self,frameGrande,lista):

        self.Existencias=Existencias(frameGrande)
        self.Existencias.grid()

        siHayFrame(lista)
        self.Existencias.pantallaExistencias(frameGrande,lista)



    def movimientosStock(self,frameGrande,lista):

        self.Movimientos=Movimientos(frameGrande)
        self.Movimientos.grid()

        siHayFrame(lista)
        self.Movimientos.pantallaMovimientos(frameGrande,lista)

