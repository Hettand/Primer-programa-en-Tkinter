import tkinter as tk
# botones

def botonNegro(boton,frame,img):

    boton=tk.Button(
                frame,
                image=img,
                cursor="hand2",
                relief="flat",
                activebackground="#fff",
                bg="#000"
                )
    return boton