from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter, A4
from reportlab.graphics.barcode import code128
from reportlab.lib import colors
from PIL import Image
import random
import os
from etiqueta_pdf import Etiqueta

class GeneradorEtiquetas:
    """Clase para generar un PDF con múltiples etiquetas."""
    
    def __init__(self, output_file="etiquetas.pdf"):
        """Inicializa el generador de etiquetas.
        
        Args:
            output_file: Ruta del archivo PDF a generar
        """
        # Dimensiones de etiquetas (50x38 mm)
        self.etiqueta_width = 5.0 * cm   # 50 mm
        self.etiqueta_height = 3.8 * cm  # 38 mm
        
        # Sin espaciado entre etiquetas ya que solo generamos una
        self.padding_x = 0 * cm
        self.padding_y = 0 * cm
        
        # Margen mínimo de página
        self.margin_x = 0 * cm
        self.margin_y = 0 * cm
        
        # Tamaño de página igual al tamaño de la etiqueta
        self.page_width = self.etiqueta_width
        self.page_height = self.etiqueta_height

        print(f"[INFO] Dimensiones de etiqueta: {self.etiqueta_width/cm:.2f} cm x {self.etiqueta_height/cm:.2f} cm")

        # Crear un tamaño de página personalizado igual al tamaño de la etiqueta
        custom_page_size = (self.page_width, self.page_height)
        
        self.output_file = output_file
        self.page_size = custom_page_size
        self.canvas = canvas.Canvas(output_file, pagesize=custom_page_size)
        
        # Solo una etiqueta por página
        self.rows = 1
        self.cols = 1
        self.etiquetas_por_pagina = 1
    
    def generar_pdf(self, datos_etiquetas):
        """Genera un PDF con una sola etiqueta.
        
        Args:
            datos_etiquetas: Lista con un solo diccionario de datos para la etiqueta
        """
        if len(datos_etiquetas) > 1:
            print("[AVISO] Advertencia: Se proporcionó más de una etiqueta. Solo se generará la primera.")
        
        # Crear y dibujar la etiqueta en el origen de la página
        etiqueta = Etiqueta(datos_etiquetas[0])
        etiqueta.dibujar(self.canvas, 0, 0)
        
        # Guardar el PDF
        self.canvas.save()
        print(f"[OK] PDF generado: {self.output_file} con una etiqueta de {self.etiqueta_width/cm:.1f}x{self.etiqueta_height/cm:.1f} cm")
