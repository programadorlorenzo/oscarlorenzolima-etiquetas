from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter, A4
from reportlab.graphics.barcode import code128
from reportlab.lib import colors
from PIL import Image
import random
import os

class Etiqueta:
    """Clase para generar etiquetas de ropa."""
    
    def __init__(self, datos):
        """Inicializa los datos de la etiqueta.
        
        Args:
            datos: Diccionario con los datos de la etiqueta
        """
        self.barcode_value = datos.get('barcode_value', '')
        self.product_name = datos.get('product_name', '')
        self.talla = datos.get('talla', '')
        self.tamanio = datos.get('tamanio', '')
        self.posicion = datos.get('posicion', '')
        self.precio = datos.get('precio', '')
        self.sku = datos.get('sku', '')
        self.image_path = datos.get('image_path', 'assets/logo.png')
        
        # Dimensiones estándar de la etiqueta (3.05x4 cm)
        self.width = 3.05 * cm
        self.height = 4 * cm
    
    def dibujar(self, c, x_offset=0, y_offset=0):
        """Dibuja la etiqueta en un objeto canvas en la posición especificada.
        
        Args:
            c: Objeto canvas de ReportLab
            x_offset: Desplazamiento horizontal en puntos
            y_offset: Desplazamiento vertical en puntos
        """
        # Guardar el estado actual del canvas
        c.saveState()
        
        # Aplicar la traslación al canvas
        c.translate(x_offset, y_offset)
        
        # Dibujar borde de la etiqueta
        # c.setStrokeColor(colors.black)
        # c.setLineWidth(0.25)
        # c.rect(0.05 * cm, 0.05 * cm, self.width - 0.1 * cm, self.height - 0.1 * cm)
        
        # Insertar imagen (logo)
        try:
            if os.path.exists(self.image_path):
                img = Image.open(self.image_path)
                img_width = 1.8 * cm
                img_height = img.size[1] * (img_width / img.size[0])
                img_x = (self.width - img_width) / 2
                img_y = self.height - img_height - 0.1 * cm
                c.drawImage(self.image_path, img_x, img_y, img_width, img_height, preserveAspectRatio=True)
            else:
                # Espacio para la imagen sin imagen real
                img_height = 0.6 * cm
                img_y = self.height - img_height - 0.1 * cm
        except Exception as e:
            print(f"Error al cargar imagen {self.image_path}: {e}")
            img_height = 0.6 * cm
            img_y = self.height - img_height - 0.1 * cm
            
        # Nombre del producto (debajo de imagen)
        text_y = img_y - 0.3 * cm
        c.setFont("Helvetica", 6)
        c.drawCentredString(self.width / 2, text_y, self.product_name)
        
        # Tamaño y Posición (centrados y separados por guión)
        tam_pos_y = text_y - 0.25 * cm
        c.setFont("Helvetica", 5.5)
        combined_text = self.tamanio + " - " + self.posicion
        c.drawCentredString(self.width / 2, tam_pos_y, combined_text)
        
        # Talla (debajo del nombre y tamaño/posición)
        talla_y = tam_pos_y - 0.45 * cm
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(self.width / 2, talla_y, self.talla)
        
        # Distribución del espacio vertical restante
        espacio_vertical_restante = talla_y - 0.6 * cm
        espacio_para_precio = 0.35 * cm
        espacio_para_barcode = 0.65 * cm
        espacio_entre_elementos = (espacio_vertical_restante - espacio_para_precio - espacio_para_barcode) / 3
        
        # Precio (en un cuadro, entre la talla y el código de barras)
        precio_y = talla_y - espacio_entre_elementos - 0.5 * cm
        c.setFont("Helvetica-Bold", 9.5)
        
        # Calcular dimensiones del cuadro para el precio
        price_box_width = c.stringWidth(self.precio, "Helvetica-Bold", 7) + 20
        price_box_height = 0.45 * cm
        price_x = (self.width - price_box_width) / 2
        
        # Establece las posiciones del rectángulo
        rect_y = precio_y - 0.05 * cm
        rect_height = price_box_height
        
        # Dibuja el rectángulo para el precio
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.3)
        c.rect(price_x, rect_y, price_box_width, rect_height)
        
        # Para centrar perfectamente el texto, calculamos el centro exacto del rectángulo
        rect_center_y = rect_y + (rect_height / 2.3)
        
        # En ReportLab, el texto se dibuja desde la línea base, así que necesitamos ajustar:
        font_offset = 2.5
        c.drawCentredString(self.width / 2, rect_center_y - font_offset, self.precio)
        
        # Código de barras (ahora más abajo con mejor distribución)
        barcode = code128.Code128(self.barcode_value, barHeight=0.7 * cm, barWidth=0.025 * cm)
        barcode_x = (self.width - barcode.width) / 2
        barcode_y = rect_y - espacio_entre_elementos - 0.7 * cm
        barcode.drawOn(c, barcode_x, barcode_y)
        
        # Número del código de barras debajo del código
        c.setFont("Helvetica", 4)
        c.drawCentredString(self.width / 2, barcode_y - 0.18 * cm, self.barcode_value)
        
        # SKU (al final con letra más pequeña)
        c.setFont("Helvetica", 3)
        sku_y = 0.15 * cm
        c.drawCentredString(self.width / 2, sku_y, self.sku)
        
        # Restaurar el estado del canvas
        c.restoreState()
