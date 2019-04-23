import sys
sys.path.insert(1,"../conexion")
import conexion
import panel
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import pymysql



def crear(
    miBase,var_ingreso,var_doc,var_nacimiento,
    var_nombre,var_apellido,var_apellido_dos,
    var_tel,var_direccion,var_dire_num,doc):

    
    #crear cliente
    
    try:
        
        miCursor = miBase.cursor()
        dt= datetime.datetime.now()
        actual=dt.strftime("%Y/%m/%d")
        var_ingreso.set(actual)
        consulta= "INSERT INTO datos_usuarios2 (id_cliente,ingreso,documento,nacimiento,nombre,apellido,apellido_dos,telefono,direccion,numero) values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        miCursor.execute(
            consulta,
            (
                var_ingreso.get(),
                var_doc.get(),
                var_nacimiento.get(),
                var_nombre.get(),
                var_apellido.get(),
                var_apellido_dos.get(),
                var_tel.get(),
                var_direccion.get(),
                var_dire_num.get()
                )
            )
        
        miCursor.execute(
            "SELECT * FROM datos_usuarios2 where documento = %s",
            doc.get()
            )
        
        resultado = miCursor.fetchone()

        messagebox.showinfo(
            "Creación de cliente",
            "Nuevo cliente nº {}\n{} {}\nDocumento: {}".format(
                resultado[0],
                resultado[4],
                resultado[5],
                resultado[2]
                )
            )
        
    except pymysql.err.IntegrityError:
        messagebox.showerror(
            "Error",
            "Intenta ingresar un documento ya existente\nVerifique el documento"
            )

    except pymysql.err.DataError:
        messagebox.showerror(
            "Error",
            "Datos incorrectos"
            )

    except pymysql.err.InternalError:
        messagebox.showerror(
            "Error",
            "Datos incorrectos"
            )


    finally:

        miBase.commit()
        miCursor.close()
        clientes.limpiar()



def actualizar(
    miBase,var_id,var_ingreso,
    var_doc,var_nacimiento,
    var_nombre,var_apellido,
    var_apellido_dos,var_tel,
    var_direccion,var_dire_num,id_cliente):
    
    #actualizar datos personales del cliente


    num = var_id.get()
    ingr = var_ingreso.get()
    doc = var_doc.get()
    na = var_nacimiento.get()
    nom = var_nombre.get()
    ape = var_apellido.get()
    ape_dos = var_apellido_dos.get()
    tel = var_tel.get()
    dire = var_direccion.get()
    dire_num = var_dire_num.get()

    if num!="" and ingr!="" and doc!="" and nom!="" and  ape!="" and tel!="":

        try:


            miCursor = miBase.cursor()
            consulta = "UPDATE datos_usuarios2 set ingreso=(%s), documento=(%s), nacimiento=(%s), nombre=(%s) ,apellido=(%s),apellido_dos=(%s), telefono=(%s) ,direccion=(%s),numero=(%s) where id_cliente=(%s)"
            miCursor.execute(
                consulta,
                [ingr, doc, na, nom, ape, ape_dos, tel, dire, dire_num, num]
                )
            miCursor.execute(
                "SELECT * FROM datos_usuarios2 where id_cliente = %s",
                id_cliente.get()
                )


            resultado = miCursor.fetchone()
           

            messagebox.showinfo(
                "Información",
                "El cliente Nº {}\n{} {}\nha sido actualizado con éxito".format(
                    resultado[0],
                    resultado[4],
                    resultado[5]
                    )
                )    
            
            

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
                "Intenta ingresar un documento o número de cliente ya existente"
                )

        finally:
            
            miBase.commit()
            miCursor.close()
            clientes.limpiar()
    else:

        messagebox.showinfo(
            "Atención",
            "Datos mínimos requeridos:\n*Nº de Cliente\n*Fecha de ingreso\n*Documento\n*Nombre y 1er Apellido\n*Teléfono de contacto"
            )
