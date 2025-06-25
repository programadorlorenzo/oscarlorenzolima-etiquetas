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
    
    def __init__(self, output_file="etiquetas.pdf", custom_width=10.02*cm):
        """Inicializa el generador de etiquetas.
        
        Args:
            output_file: Ruta del archivo PDF a generar
            custom_width: Ancho personalizado de la página (default: 10.02cm)
        """
        # Dimensiones de etiquetas (ajustado para optimizar el espacio)
        self.etiqueta_width = 3 * cm  # Ligeramente reducido para evitar advertencias
        self.etiqueta_height = 4 * cm
        
        # Espacio entre etiquetas (muy reducido para acercar las etiquetas)
        self.padding_x = 0.3 * cm   # Mínimo espacio horizontal
        self.padding_y = 0 * cm   # Reducido para acercar las etiquetas verticalmente
        
        # Margen de página (reducido al mínimo)
        self.margin_x = 0.18 * cm
        self.margin_y = 0.01 * cm    # Reducido casi a cero pero manteniendo un mínimo
        
        # Ancho fijo de 10.02cm como se solicitó
        self.page_width = custom_width
        
        # Para 3 etiquetas en horizontal, calculamos el espacio necesario
        etiquetas_width_total = (3 * self.etiqueta_width) + (2 * self.padding_x)
        if etiquetas_width_total + (2 * self.margin_x) > self.page_width:
            print(f"⚠️ Advertencia: El ancho de página ({self.page_width/cm:.2f} cm) podría ser insuficiente para 3 etiquetas de {self.etiqueta_width/cm:.2f} cm con margen de {self.margin_x/cm:.2f} cm y padding de {self.padding_x/cm:.2f} cm")
            # Ajustar automáticamente el margen para que encajen
            self.margin_x = max(0.01 * cm, (self.page_width - etiquetas_width_total) / 2)
            print(f"   Ajustando margen horizontal a {self.margin_x/cm:.2f} cm")
        
        # Fijar 1 fila por página (solo 3 etiquetas por página)
        self.rows = 1
        
        # Altura exacta de la página: altura de etiqueta + margen superior + margen inferior
        self.page_height = self.etiqueta_height + (2 * self.margin_y)
        print(f"📏 Dimensiones de página: {self.page_width/cm:.2f} cm × {self.page_height/cm:.2f} cm")
        
        # Crear un tamaño de página personalizado
        custom_page_size = (self.page_width, self.page_height)
        
        self.output_file = output_file
        self.page_size = custom_page_size
        self.canvas = canvas.Canvas(output_file, pagesize=custom_page_size)
        
        # Configuración fija para 3 columnas como se solicita
        self.cols = 3
        
        # Crear un tamaño de página personalizado
        custom_page_size = (self.page_width, self.page_height)
        
        self.output_file = output_file
        self.page_size = custom_page_size
        self.canvas = canvas.Canvas(output_file, pagesize=custom_page_size)
        
        # Configuración fija para 3 columnas como se solicita
        self.cols = 3
        
        # Calcular etiquetas por página
        self.etiquetas_por_pagina = self.cols * self.rows
    
    def generar_mockup_datos(self, cantidad=50):
        """Genera datos de ejemplo para etiquetas.
        
        Args:
            cantidad: Número de etiquetas a generar
            
        Returns:
            Lista de diccionarios con datos para etiquetas
        """
        # Posibles valores para los diferentes campos
        productos = [
            "Jean Renata Verde Menta", 
            "Jean Carolina Azul", 
            "Blusa Camila Blanco", 
            "Falda Patricia Negro",
            "Pantalón Claudia Gris",
            "Blusa Mariana Rosado",
            "Vestido Elena Dorado",
            "Short Valeria Celeste",
            "Conjunto María Beige"
        ]
        
        tallas = ["Talla 24", "Talla 26", "Talla 28", "Talla 30", "Talla 32", "Talla 34", "Talla 36"]
        tamanios = ["Petite", "Regular", "Tall"]
        posiciones = ["Cadera", "Cintura", "Muslo"]
        precios = ["S/ 89.90", "S/ 99.90", "S/ 115.00", "S/ 129.90", "S/ 149.90", "S/ 159.90"]
        
        datos = []
        for i in range(cantidad):
            # Genera un número de SKU único con formato similar al ejemplo
            sku_base = f"{random.randint(50000, 59999)}-"
            sku_letra = random.choice(['R', 'C', 'B', 'P', 'V'])
            sku_color = random.choice(['VM', 'AZ', 'BL', 'NG', 'GR', 'RS'])
            sku_num = f"{random.randint(20, 38)}{random.randint(1000, 9999)}"
            sku = f"{sku_base}{sku_letra}-{sku_color}{sku_num}"
            
            # Genera un código de barras de 12 dígitos
            barcode = ''.join([str(random.randint(0, 9)) for _ in range(12)])
            
            datos.append({
                'product_name': random.choice(productos),
                'talla': random.choice(tallas),
                'tamanio': random.choice(tamanios),
                'posicion': random.choice(posiciones),
                'precio': random.choice(precios),
                'sku': sku,
                'barcode_value': barcode,
                'image_path': 'assets/logo.png'
            })
        
        return datos
    
    def generar_pdf(self, datos_etiquetas):
        """Genera un PDF con las etiquetas especificadas.
        
        Args:
            datos_etiquetas: Lista de diccionarios con datos para etiquetas
        """
        total_etiquetas = len(datos_etiquetas)
        paginas_necesarias = (total_etiquetas + self.etiquetas_por_pagina - 1) // self.etiquetas_por_pagina
        
        etiqueta_index = 0
        
        for pagina in range(paginas_necesarias):
            if pagina > 0:
                self.canvas.showPage()  # Nueva página
            
            for fila in range(self.rows):
                for col in range(self.cols):
                    if etiqueta_index >= total_etiquetas:
                        break
                    
                    # Calcular la posición de la etiqueta en la página
                    x = self.margin_x + col * (self.etiqueta_width + self.padding_x)
                    y = self.page_height - self.margin_y - (fila + 1) * (self.etiqueta_height + self.padding_y)
                    
                    # Crear y dibujar la etiqueta
                    etiqueta = Etiqueta(datos_etiquetas[etiqueta_index])
                    etiqueta.dibujar(self.canvas, x, y)
                    
                    etiqueta_index += 1
                
                if etiqueta_index >= total_etiquetas:
                    break
        
        # Guardar el PDF
        self.canvas.save()
        print(f"✅ PDF generado: {self.output_file} con {total_etiquetas} etiquetas en {paginas_necesarias} páginas")
