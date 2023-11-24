import tkinter as tk
import pandas as pd
from CIE_10_Loader import CIE_10_Loader
from CIE_APP import CIE_APP
from Repairman import Repairman
from tkinter import scrolledtext
from tkinter import filedialog
import threading
import sys
import time

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert(tk.END, str, (self.tag,))
        self.widget.see(tk.END)
        self.widget.configure(state="disabled")

    def flush(self):
        pass


class Interfaz:
    def __init__(self):
        self.loaded = False
        self.df_a = None
        self.fixed_df_a = None
        self.CIE_10_DATA = None
        self.loader = CIE_10_Loader()
        self.cie_app = CIE_APP()
        self.repaired_df = None
        self.root = tk.Tk()
        self.root.title("Reparador de datos locales de CIE-10")
        self.root.iconbitmap("service_ico_repair.ico")
        self.repairman = None
        # Crear un marco para los botones
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=0, column=0, sticky="ns", padx=(20, 20), pady=(20, 0))

        # Crear los botones
        self.load_CIE_button = tk.Button(
            button_frame,
            text="Cargar registros de CIE_10",
            command=self.load_cie_10_web_data,
        )
        self.load_CIE_by_file_button = tk.Button(
            button_frame,
            text="Cargar registros de CIE_10 por archivo",
            command=self._load_CIE_by_file_button,
        )
        self.export_CIE_by_file_button = tk.Button(
            button_frame,
            text="Exportar registros de CIE_10",
            command=self._export_CIE_by_file_button,
            state=tk.DISABLED,
        )
        self.upload_button = tk.Button(
            button_frame,
            text="Subir Excel",
            command=self.upload_excel,
            state=tk.DISABLED,
        )
        self.train_IA = tk.Button(
            button_frame,
            text="Entrenar la IA",
            command=self._train_IA,
            state=tk.DISABLED,
        )
        self.repair_button = tk.Button(
            button_frame,
            text="Iniciar reparación",
            command=self.start_repair,
            state=tk.DISABLED,
        )
        self.export_button = tk.Button(
            button_frame,
            text="Exportar a Excel",
            command=self.export_to_excel,
            state=tk.DISABLED,
        )

        # Colocar los botones en el marco
        self.load_CIE_button.pack(side=tk.TOP, pady=10)
        self.load_CIE_by_file_button.pack(side=tk.TOP, pady=10)
        self.export_CIE_by_file_button.pack(side=tk.TOP, pady=10)

        self.upload_button.pack(side=tk.TOP, pady=10)
        self.train_IA.pack(side=tk.TOP, pady=10)
        self.repair_button.pack(side=tk.TOP, pady=10)
        self.export_button.pack(side=tk.TOP, pady=10)

        # Crear un widget de texto para la salida de la consola
        self.console_output = scrolledtext.ScrolledText(
            self.root, state="disabled", height=10, wrap=tk.WORD
        )
        self.console_output.grid(row=0, column=1, sticky="nsew")

        # Redirigir la salida de la consola al widget de texto
        sys.stdout = TextRedirector(self.console_output)

        self.root.grid_columnconfigure(1, weight=1)
        # Hacer que la fila 0 se expanda para llenar el espacio extra
        self.root.grid_rowconfigure(0, weight=1)

        self.root.geometry("600x600")
        # Iniciar el bucle principal de Tkinter
        self.root.mainloop()

    def load_cie_10_web_data(self):
        # Crear un hilo para cargar los datos
        load_thread0 = threading.Thread(target=self._load_cie_10_web_data)
        # Iniciar el hilo
        load_thread0.start()

    def _load_cie_10_web_data(self):
        try:
            print("Cargando datos de CIE-10 de la web...")
            self.CIE_10_DATA = self.cie_app.load_cie_10_data()

            self.loaded = True
            self.upload_button.config(state=tk.NORMAL)
            self.export_CIE_by_file_button.config(state=tk.NORMAL)

            print("\n\nDatos de CIE-10 de la web cargados con exito")
        except:
            print("Error al cargar los datos de CIE_10")
            self.loaded = False

    # Función para subir un archivo de Excel
    def upload_excel(self):
        filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        self.df_a = pd.read_excel(filename)
        print("\n\n")
        print("\n\n")
        print("Archivo de excel cargado con exito")
        print("\n\n")
        print('Puede iniciar el entrenamiento de la IA, esto puede casuar que la apliacion se vuelva lenta o deje de responder, porfavor espere, es normal que suceda')

        time.sleep(1)
        
        
        self.repairman=Repairman(self.df_a, self.CIE_10_DATA)
        #self.repair_button.config(state=tk.NORMAL)
        self.train_IA.config(state=tk.NORMAL)

    
    def Do_train_IA(self):
        print('Iniciando entrenamiento de la IA, esto puede casuar que la apliacion se vuelva lenta o deje de responder, porfavor espere, es normal que pase...')
        
        # load_thread6 = threading.Thread(target=self._train_IA)
        # # Iniciar el hilo
        # load_thread6.start()


    def _train_IA(self):
        
            # Comenzar a comprobar la cola de mensajes
        self.repairman.train()
        self.repair_button.config(state=tk.NORMAL)
    def _load_CIE_by_file_button(self):
        try:
            filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
            self.CIE_10_DATA = pd.read_excel(filename)
            print("\n\n")
            print("\n\n")
            print("Archivo de datos de CIE cargado con exito")
            print("\n\n")
            self.loaded = True
            # self.repair_button.config(state=tk.NORMAL)
            self.upload_button.config(state=tk.NORMAL)
            self.export_CIE_by_file_button.config(state=tk.NORMAL)
        except:
            print("Error al cargar los datos de CIE_10")
            self.loaded = False

    # Función para iniciar la reparación
    def start_repair(self):

        load_thread1 = threading.Thread(target=self._start_repair)
        # Iniciar el hilo
        load_thread1.start()
        # Comenzar a comprobar la cola de mensajes

    def _start_repair(self):
        try:

            # print('Iniciando reparación...')
            # Crear una instancia de Repairman

            # Llamar a la función agregar_columna_code_corregida
            self.repaired_df = self.repairman.agregar_columna_code_corregida()
            # Llamar a la función export_to_excel
            self.export_button.config(state=tk.NORMAL)

        except Exception as e:
            print(f"Error al reparar los datos: {e}")

    def export_to_excel(self):
        if self.repaired_df is not None:
            # Open file explorer window to choose save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")]
            )

            if filename:
                # Export the dataframe to the chosen file location
                self.repaired_df.to_excel(filename, index=False)
                print(f"Data exported to {filename} successfully.")
            else:
                print("No file selected.")

    def _export_CIE_by_file_button(self):
        if self.CIE_10_DATA is not None:
            # Open file explorer window to choose save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")]
            )

            if filename:
                # Export the dataframe to the chosen file location
                self.CIE_10_DATA.to_excel(filename, index=False)
                print(f"Data exported to {filename} successfully.")
            else:
                print("No file selected.")



