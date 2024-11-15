import tkinter as tk
from tkinter import ttk 
from interfaz_audio import InterfazCompresionAudio
from interfaz_imagen import AplicacionCompresionImagen
from interfaz_imagentest import AplicacionCompresionImagenTest
from interfaz_aufiotest import InterfazCompresionAudioTest

class AplicacionPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación de Compresión")
        self.tabControl = ttk.Notebook(self)
        self.tabControl.pack(expand=1, fill="both")
        
        self.tab_audio = tk.Frame(self.tabControl)
        self.tabControl.add(self.tab_audio, text="Audio")
        self.interfaz_audio = InterfazCompresionAudio(self.tab_audio)

        self.tab_audio = tk.Frame(self.tabControl)
        self.tabControl.add(self.tab_audio, text="AudioTEST")
        self.interfaz_audio = InterfazCompresionAudioTest(self.tab_audio)
        
        self.tab_imagen = tk.Frame(self.tabControl)
        self.tabControl.add(self.tab_imagen, text="Imagen")
        self.interfaz_imagen = AplicacionCompresionImagen(self.tab_imagen)

        self.tab_imagen = tk.Frame(self.tabControl)
        self.tabControl.add(self.tab_imagen, text="ImagenTEST")
        self.interfaz_imagen = AplicacionCompresionImagenTest(self.tab_imagen)

if __name__ == "__main__":
    app = AplicacionPrincipal()
    app.geometry("+0+0")
    app.mainloop()
