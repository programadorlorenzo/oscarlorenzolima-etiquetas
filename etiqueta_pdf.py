from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
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
        self.tamanio = str(datos.get('tamanio', ''))
        self.posicion = str(datos.get('posicion', ''))
        self.fit = str(datos.get('fit', ''))
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
            
        # FIT - inmediatamente debajo del logo (solo si tiene datos válidos)
        fit_y = img_y - 0.35 * cm  # Aumentado margen de 0.25 a 0.35
        tiene_fit = False
        
        if self.fit and self.fit != "NAN" and self.fit != "":
            c.setFont("Helvetica-BoldOblique", 7.2)  # Aumentado de 6.5 a 7.2 y cambiado a cursiva
            c.drawCentredString(self.width / 2, fit_y, self.fit)
            tiene_fit = True
            
        # Nombre del producto (debajo del FIT o del logo si no hay FIT)
        if tiene_fit:
            text_y = fit_y - 0.35 * cm  # Aumentado margen de 0.3 a 0.35
        else:
            text_y = img_y - 0.4 * cm  # Aumentado margen de 0.3 a 0.4
        
        c.setFont("Helvetica-Bold", 8)  # Aumentado de 7 a 8 puntos
        c.drawCentredString(self.width / 2, text_y, self.product_name)
        
        # Tamaño y Posición (debajo del nombre del producto)
        tam_pos_y = text_y - 0.35 * cm  # Aumentado margen de 0.3 a 0.35
            
        tiene_tamanio_posicion = False
        
        if (self.tamanio and self.tamanio != "NAN" and self.tamanio != "") or \
           (self.posicion and self.posicion != "NAN" and self.posicion != ""):
            c.setFont("Helvetica", 6.5)  # Cambiado de Helvetica-BoldOblique a Helvetica (normal, sin cursiva ni negrita)
            if self.posicion == "NAN" or self.posicion == "" or not self.posicion:
                combined_text = self.tamanio
            elif self.tamanio == "NAN" or self.tamanio == "" or not self.tamanio:
                combined_text = self.posicion
            else:
                combined_text = self.tamanio + " - " + self.posicion
            c.drawCentredString(self.width / 2, tam_pos_y, combined_text)
            tiene_tamanio_posicion = True
        
        # Talla (debajo de tamaño/posición o del nombre)
        if tiene_tamanio_posicion:
            talla_y = tam_pos_y - 0.4 * cm  # Reducido margen de 0.5 a 0.4 (sube la talla)
        else:
            talla_y = text_y - 0.4 * cm  # Reducido margen de 0.5 a 0.4 (sube la talla)
        
        c.setFont("Helvetica-Bold", 9.2)
        c.drawCentredString(self.width / 2, talla_y, self.talla)
        
        # Distribución del espacio vertical restante
        espacio_vertical_restante = talla_y - 0.6 * cm
        espacio_para_precio = 0.35 * cm
        espacio_para_barcode = 0.65 * cm
        espacio_entre_elementos = (espacio_vertical_restante - espacio_para_precio - espacio_para_barcode) / 3
        
        # Precio (en un cuadro, entre la talla y el código de barras)
        precio_y = talla_y - espacio_entre_elementos - 0.45 * cm  # Aumentado de 0.35 a 0.45 para bajar el precio
        c.setFont("Helvetica-Bold", 10.5)  # Aumentado tamaño de 9.7 a 10.5
        
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
        # Código de barras optimizado para mejor escaneo
        barcode = code128.Code128(
            self.barcode_value,
            width=self.width - 0.2 * cm,  # Ancho de barra ajustado
            barHeight=0.75 * cm,     # Mayor altura para mejor lectura
            barWidth=0.028 * cm,      # Ancho de barra optimizado
            checksum=1,              # Incluir checksum para validación
            quiet=True               # Incluir zona silenciosa (quiet zone)
        )
        barcode_x = (self.width - barcode.width) / 2
        barcode_y = rect_y - espacio_entre_elementos - 0.75 * cm  # Reducido de 0.85 a 0.75 para subir el código
        barcode.drawOn(c, barcode_x, barcode_y)
        
        # Número del código de barras debajo del código
        c.setFont("Helvetica", 5.2)
        c.drawCentredString(self.width / 2, barcode_y - 0.18 * cm, self.barcode_value)
        
        # SKU (al final con letra más pequeña)
        c.setFont("Helvetica-Bold", 4.5)
        sku_y = 0.05 * cm  # Reducido de 0.1 a 0.05 para bajar un poquito el SKU
        c.drawCentredString(self.width / 2, sku_y, self.sku)
        
        # Restaurar el estado del canvas
        c.restoreState()
