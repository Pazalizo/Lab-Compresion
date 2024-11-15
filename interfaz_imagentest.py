import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from scipy.fftpack import dct, idct

class AplicacionCompresionImagenTest:
    def __init__(self, root):
        self.root = root

        # Etiqueta de título
        self.titulo_etiqueta = tk.Label(root, text="Compresión de Imágenes", font=("Helvetica", 16, "bold"))
        self.titulo_etiqueta.grid(row=0, pady=20, padx=20, columnspan=2, sticky="nswe")

        # Botón para cargar la imagen
        self.boton_cargar_imagen = tk.Button(root, text="Cargar Imagen", command=self.cargar_imagen)
        self.boton_cargar_imagen.grid(row=1, column=0, pady=10, padx=10, sticky="nswe")

        # Entrada para ingresar la serie de porcentajes de compresión
        self.etiqueta_porcentaje_compresion = tk.Label(root, text="Porcentajes de Compresión (separados por coma):")
        self.etiqueta_porcentaje_compresion.grid(row=1, column=1, pady=10, padx=10, sticky="nswe")
        self.entrada_porcentaje_compresion = tk.Entry(root)
        self.entrada_porcentaje_compresion.grid(row=1, column=2, pady=10, padx=10, sticky="nswe")
        self.entrada_porcentaje_compresion.insert(0, "15, 50, 70")  # Valores predeterminados
        self.entrada_porcentaje_compresion.config(state=tk.DISABLED)

        # Botón para comprimir la imagen
        self.boton_comprimir = tk.Button(root, text="Comprimir", command=self.comprimir_imagen)
        self.boton_comprimir.grid(row=1, column=3, pady=10, padx=10, sticky="nswe")
        self.boton_comprimir.config(state=tk.DISABLED)

        # Configurar el área desplazable para las imágenes
        self.canvas = tk.Canvas(root, borderwidth=0)
        self.canvas.grid(row=2, column=0, columnspan=4, sticky="nsew")

        # Barra de desplazamiento vertical
        self.scrollbar_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.grid(row=2, column=4, sticky="ns")

        # Conectar el canvas con la barra de desplazamiento
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        # Frame interno dentro del canvas donde se colocarán las imágenes
        self.marco_imagen = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.marco_imagen, anchor="nw")

        # Ajustar el tamaño del contenido en el canvas automáticamente
        self.marco_imagen.bind("<Configure>", self.actualizar_scroll_region)

    def actualizar_scroll_region(self, event=None):
        """Actualizar la región desplazable del canvas para ajustarse al contenido."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def cargar_imagen(self):
        try:
            self.ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
            if self.ruta_archivo:
                self.imagen = cv2.imread(self.ruta_archivo, cv2.IMREAD_GRAYSCALE)
                self.entrada_porcentaje_compresion.config(state=tk.NORMAL)
                self.boton_comprimir.config(state=tk.NORMAL)
            else:
                messagebox.showwarning("Advertencia", "Por favor, carga una imagen antes de comprimirla.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la imagen: {str(e)}")

    def comprimir_imagen(self):
        """
        Comprime la imagen cargada con los porcentajes especificados y muestra cada compresión y descompresión en la misma fila.
        """
        if hasattr(self, 'imagen'):
            try:
                # Obtener la lista de porcentajes de compresión
                porcentajes = [int(p.strip()) for p in self.entrada_porcentaje_compresion.get().split(',')]

                # Limpiar el marco de imágenes si ya contiene resultados previos
                for widget in self.marco_imagen.winfo_children():
                    widget.destroy()

                # Mostrar la imagen original en la primera fila
                self.mostrar_imagen_original()

                # Para cada porcentaje de compresión, calcular y mostrar la compresión y descompresión en la misma fila
                for i, porcentaje in enumerate(porcentajes):
                    fila = i + 1  # Comienza en la fila 1
                    self.mostrar_imagen_comprimida(porcentaje, fila)
                    self.mostrar_imagen_descomprimida(porcentaje, fila)

                messagebox.showinfo("Información", "Imágenes comprimidas y descomprimidas mostradas correctamente.")
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa porcentajes de compresión válidos separados por coma.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al comprimir la imagen: {str(e)}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, carga una imagen antes de comprimirla.")

    def mostrar_imagen_original(self):
        """
        Muestra la imagen original en la primera fila.
        """
        marco = tk.Frame(self.marco_imagen)
        marco.grid(row=0, column=0, padx=10, pady=10, sticky="nswe", columnspan=2)
        
        imagen_original_pil = Image.fromarray(self.imagen)
        imagen_original_pil = self.escalar_imagen(imagen_original_pil, 300, 460)
        img_original_tk = ImageTk.PhotoImage(image=imagen_original_pil)
        
        etiqueta_imagen_original = tk.Label(marco, image=img_original_tk)
        etiqueta_imagen_original.image = img_original_tk
        etiqueta_imagen_original.grid(row=0, column=0)
        
        etiqueta_titulo_original = tk.Label(marco, text="Original")
        etiqueta_titulo_original.grid(row=1, column=0)

    def mostrar_imagen_comprimida(self, porcentaje_compresion, fila):
        """
        Comprime y muestra la imagen con el porcentaje especificado en la columna 0 de la fila indicada.
        """
        # Aplicar la Transformada Discreta del Coseno (DCT)
        dct_tipo2 = dct(self.imagen, type=2, norm='ortho')

        # Comprimir eliminando los coeficientes menos significativos
        posiciones_necesarias, dct_comprimida = self.calcular_porcentaje(dct_tipo2, porcentaje_compresion)

        # Aplicar escala logarítmica para mejorar el contraste visual
        dct_comprimida_log = np.log1p(np.abs(dct_comprimida))
        max_val = np.max(dct_comprimida_log)
        if max_val > 0:  # Normalizar al rango 0-255
            dct_comprimida_normalizada = (dct_comprimida_log / max_val) * 255
        else:
            dct_comprimida_normalizada = dct_comprimida_log

        img_comprimida = dct_comprimida_normalizada.astype(np.uint8)

        # Crear un marco para la imagen comprimida en la fila actual
        marco = tk.Frame(self.marco_imagen)
        marco.grid(row=fila, column=0, padx=10, pady=10, sticky="nswe")

        # Mostrar la imagen comprimida
        img_comprimida_pil = Image.fromarray(img_comprimida)
        img_comprimida_pil = self.escalar_imagen(img_comprimida_pil, 300, 460)
        img_comprimida_tk = ImageTk.PhotoImage(image=img_comprimida_pil)
        
        etiqueta_imagen_comprimida = tk.Label(marco, image=img_comprimida_tk)
        etiqueta_imagen_comprimida.image = img_comprimida_tk
        etiqueta_imagen_comprimida.grid(row=0, column=0)
        
        # Calcular el total de elementos en la imagen original
        total_elementos = np.prod(self.imagen.shape)
        
        # Mostrar el texto informativo de compresión
        etiqueta_titulo_comprimida = tk.Label(marco, text=f"Comprimida al {porcentaje_compresion}%\n{posiciones_necesarias} elementos eliminados de {total_elementos} totales")
        etiqueta_titulo_comprimida.grid(row=1, column=0)

    def mostrar_imagen_descomprimida(self, porcentaje_compresion, fila):
        """
        Descomprime y muestra la imagen con el porcentaje especificado en la columna 1 de la misma fila.
        """
        # Aplicar la Transformada Discreta del Coseno (DCT)
        dct_tipo2 = dct(self.imagen, type=2, norm='ortho')

        # Comprimir eliminando los coeficientes menos significativos
        _, dct_comprimida = self.calcular_porcentaje(dct_tipo2, porcentaje_compresion)

        # Convertir de nuevo al dominio de la imagen
        idct_tipo2 = idct(dct_comprimida, type=2, norm='ortho')
        img_descomprimida = np.clip(idct_tipo2, 0, 255).astype(np.uint8)

        # Crear un marco para la imagen descomprimida en la fila actual
        marco = tk.Frame(self.marco_imagen)
        marco.grid(row=fila, column=1, padx=10, pady=10, sticky="nswe")

        # Mostrar la imagen descomprimida
        img_descomprimida_pil = Image.fromarray(img_descomprimida)
        img_descomprimida_pil = self.escalar_imagen(img_descomprimida_pil, 300, 460)
        img_descomprimida_tk = ImageTk.PhotoImage(image=img_descomprimida_pil)
        
        etiqueta_imagen_descomprimida = tk.Label(marco, image=img_descomprimida_tk)
        etiqueta_imagen_descomprimida.image = img_descomprimida_tk
        etiqueta_imagen_descomprimida.grid(row=0, column=0)
        
        etiqueta_titulo_descomprimida = tk.Label(marco, text=f"Descomprimida al {porcentaje_compresion}%")
        etiqueta_titulo_descomprimida.grid(row=1, column=0)

    def calcular_porcentaje(self, datos, porcentaje):
        elementos_totales = np.prod(datos.shape)
        posiciones_necesarias = int(elementos_totales * (porcentaje / 100))
        indices_menores = np.argsort(np.abs(datos), axis=None)
        datos_modificados = datos.flatten()
        datos_modificados[indices_menores[:posiciones_necesarias]] = 0
        return posiciones_necesarias, datos_modificados.reshape(datos.shape)

    def escalar_imagen(self, image, max_width, max_height):
        width, height = image.size
        ratio_width = max_width / width
        ratio_height = max_height / height
        ratio = min(ratio_width, ratio_height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        return image.resize((new_width, new_height))
