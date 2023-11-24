import tkinter as tk
from tkinter import scrolledtext
import sys

def imprimir_hola():
    for i in range(10):
        print('Hola')

# Redirigir la salida estándar al widget Text
class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, str, (self.tag,))
        self.widget.see(tk.END)
        self.widget.config(state=tk.DISABLED)

# Crear la ventana
ventana = tk.Tk()
ventana.title('Ventana con Botón y Consola')
ventana.geometry('500x500')

# Crear el botón
boton_hola = tk.Button(ventana, text='Imprimir Hola', command=imprimir_hola)
boton_hola.pack(pady=20)

# Crear el widget Text para la consola
consola_text = scrolledtext.ScrolledText(ventana, state=tk.DISABLED, height=10, wrap=tk.WORD)
consola_text.pack(expand=True, fill='both')

# Redirigir stdout al widget Text
sys.stdout = TextRedirector(consola_text, "stdout")

# Iniciar el bucle de eventos
ventana.mainloop()