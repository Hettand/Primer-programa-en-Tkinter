import sys
sys.path.insert(1,"../conexion")
import conexion
sys.path.insert(2,"../panel")
import funcionalidades
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import pymysql
import ficha_cliente
import vehiculo_cliente
import formulario_cliente
from belfrywidgets import ToolTip
import smtplib



Conexion=conexion.Conexion
desactivar=funcionalidades.desactivar
reactivar=funcionalidades.reactivar


class PantallaCliente(Conexion,tk.Frame):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		frame=tk.Frame(self,bg="blue")
		frame.grid(row=0,column=0,ipady=90,ipadx=90)

