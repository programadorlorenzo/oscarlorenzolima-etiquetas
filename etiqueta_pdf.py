from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm
from reportlab.lib.pagesizes import letter, A4
from reportlab.graphics.barcode import code128
from reportlab.lib import colors
from PIL import Image
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
        self.precio = datos.get('precio', '')
        self.sku = datos.get('sku', '')
        self.image_path = datos.get('image_path','assets/logo.jpeg')
        
        # Dimensiones de la etiqueta: 50 x 38 mm
        self.width = 50 * mm
        self.height = 38 * mm
    
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
                img_width = 2.8 * cm  # Logo más grande para el nuevo ancho
                img_height = img.size[1] * (img_width / img.size[0])
                img_x = (self.width - img_width) / 2
                img_y = self.height - img_height - 0.1 * cm
                c.drawImage(self.image_path, img_x, img_y, img_width, img_height, preserveAspectRatio=True)
            else:
                # Espacio para la imagen sin imagen real
                img_height = 1.0 * cm  # Mayor espacio reservado
                img_y = self.height - img_height - 0.1 * cm
        except Exception as e:
            print(f"Error al cargar imagen {self.image_path}: {e}")
            img_height = 0.6 * cm
            img_y = self.height - img_height - 0.1 * cm
            
        # FIT - inmediatamente debajo del logo
        text_y = img_y - 0.35 * cm
        
        # Nombre del producto (más grande y destacado)
        c.setFont("Helvetica-Bold", 11)  # Aumentado para el nuevo ancho
        text_lines = self.product_name.split(' ')
        if len(text_lines) > 2:  # Si el nombre es largo, dividirlo en dos líneas
            first_line = ' '.join(text_lines[:len(text_lines)//2])
            second_line = ' '.join(text_lines[len(text_lines)//2:])
            c.drawCentredString(self.width / 2, text_y + 0.12 * cm, first_line)
            c.drawCentredString(self.width / 2, text_y - 0.12 * cm, second_line)
            text_y = text_y - 0.24 * cm  # Ajuste más compacto para nombres en dos líneas
        else:
            c.drawCentredString(self.width / 2, text_y, self.product_name)
        
        # Talla (directamente debajo del nombre del producto)
        talla_y = text_y - 0.4 * cm  # Reducido el espacio entre nombre y talla
        
        c.setFont("Helvetica-Bold", 14)  # Talla más grande y prominente
        c.drawCentredString(self.width / 2, talla_y, self.talla)
        
        # Precio (en un cuadro más compacto pero visible)
        precio_y = talla_y - 0.55 * cm  # Reducido el espacio entre talla y precio
        c.setFont("Helvetica-Bold", 11)
        
        # Calcular dimensiones del cuadro para el precio
        price_box_width = c.stringWidth(self.precio, "Helvetica-Bold", 11) + 15
        price_box_height = 0.5 * cm
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
        
        target_w = self.width - 0.20 * cm
        bar_height = 0.75 * cm


        # --- Código de barras (Code128) - Ocupando el espacio restante ---
        espacio_disponible = rect_y - 0.3 * cm  # Espacio desde el precio hasta el borde inferior
        bar_height = min(1.2 * cm, espacio_disponible * 0.85)  # Usar 85% del espacio disponible
        target_w = self.width - 0.2 * cm  # Margen horizontal para el nuevo ancho

        barcode = code128.Code128(
            self.barcode_value,
            barHeight=bar_height,
            barWidth=0.35 * mm,  # Módulos más anchos para el nuevo formato
            humanReadable=False
        )

        # Posición vertical base del código (debajo del precio)
        barcode_y = rect_y - 0.35 * cm - bar_height  # Menos espacio entre precio y código

        # Escala horizontal para encajar en target_w
        scale_x = min(1.0, target_w / barcode.width)

        c.saveState()
        # Centrado horizontal teniendo en cuenta la escala
        barcode_x = (self.width - barcode.width * scale_x) / 2.0
        c.translate(barcode_x, barcode_y)
        c.scale(scale_x, 1.0)
        barcode.drawOn(c, 0, 0)
        c.restoreState()

        # Número del código de barras debajo del código
        c.setFont("Helvetica", 6.5)  # Ligeramente más pequeño pero legible
        c.drawCentredString(self.width / 2, barcode_y - 0.2 * cm, self.barcode_value)

        # Restaurar el estado del canvas
        c.restoreState()


