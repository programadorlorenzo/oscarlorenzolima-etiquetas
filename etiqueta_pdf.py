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
        self.image_path = datos.get('image_path', 'assets/logo.jpeg')

        # Dimensiones de la etiqueta: 50 x 38 mm
        self.width = 50 * mm
        self.height = 38 * mm

        # Márgenes internos para evitar que algo se salga de los bordes
        self.margin = 0.12 * cm
        # Área disponible para contenido (ancho útil)
        self.content_width = self.width - 2 * self.margin
        # Espacio vertical reservado entre elementos
        self.v_spacing = 0.12 * cm
    
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

        # Paleta en blanco y negro (sin colores)
        bg_color = colors.white
        gold = colors.black
        dark = colors.black

        # Fondo redondeado (sin bordes)
        c.setFillColor(bg_color)
        # Dibujar fondo con esquinas redondeadas, sin trazo (solo fondo)
        c.roundRect(0, 0, self.width, self.height, 3 * mm, stroke=0, fill=1)

        # Insertar imagen (logo)
        try:
            if os.path.exists(self.image_path):
                img = Image.open(self.image_path)
                # Ajustar ancho del logo al ancho de contenido
                max_logo_width = min(2.8 * cm, self.content_width)
                img_width = max_logo_width
                img_height = img.size[1] * (img_width / img.size[0])
                img_x = self.margin + (self.content_width - img_width) / 2
                img_y = self.height - img_height - self.margin
                c.drawImage(self.image_path, img_x, img_y, img_width, img_height, preserveAspectRatio=True, mask='auto')
            else:
                # Espacio para la imagen sin imagen real
                img_height = 1.0 * cm  # Mayor espacio reservado
                img_y = self.height - img_height - self.margin
        except Exception as e:
            print(f"Error al cargar imagen {self.image_path}: {e}")
            img_height = 0.6 * cm
            img_y = self.height - img_height - 0.1 * cm

        # FIT - inmediatamente debajo del logo
        text_y = img_y - self.v_spacing

        # Pequeño separador dorado decorativo
        sep_w = self.content_width * 0.6
        sep_x = self.margin + (self.content_width - sep_w) / 2
        c.setStrokeColor(gold)
        c.setLineWidth(0.9)
        c.line(sep_x, text_y + 0.2 * cm, sep_x + sep_w, text_y + 0.2 * cm)
        text_y -= 0.18 * cm

        # Nombre del producto (más grande y destacado) - estilo serif
        # Ajustar tamaño de fuente o dividir en hasta 2 líneas para que quepa en content_width
        max_font = 12
        min_font = 8
        font = max_font
        # util: medida en puntos del string
        while font >= min_font:
            w = c.stringWidth(self.product_name, "Helvetica-Bold", font)
            if w <= self.content_width:
                # cabe en una sola línea
                c.setFont("Times-Bold", font)
                c.setFillColor(dark)
                c.drawCentredString(self.margin + self.content_width / 2, text_y, self.product_name)
                text_y -= (font / 72.0) * cm + self.v_spacing
                break
            else:
                # probar dividir en dos líneas: buscar punto de corte por palabras
                words = self.product_name.split()
                for split_index in range(1, len(words)):
                    first = ' '.join(words[:split_index])
                    second = ' '.join(words[split_index:])
                    w1 = c.stringWidth(first, "Helvetica-Bold", font)
                    w2 = c.stringWidth(second, "Helvetica-Bold", font)
                    if w1 <= self.content_width and w2 <= self.content_width:
                        c.setFont("Times-Bold", font)
                        c.setFillColor(dark)
                        c.drawCentredString(self.margin + self.content_width / 2, text_y + (font * 0.35), first)
                        c.drawCentredString(self.margin + self.content_width / 2, text_y - (font * 0.35), second)
                        text_y -= (font / 72.0) * cm * 2 + self.v_spacing
                        font = None
                        break
                if font is None:
                    break
            font -= 1
        else:
            # Si baja del min_font, cortar y mostrar primera parte con '...'
            display = self.product_name
            # recortar para que el ancho de display con min_font quepa
            while c.stringWidth(display + '...', "Helvetica-Bold", min_font) > self.content_width and len(display) > 0:
                display = display[:-1]
            c.setFont("Times-Bold", min_font)
            c.setFillColor(dark)
            c.drawCentredString(self.margin + self.content_width / 2, text_y, display + '...')
            text_y -= (min_font / 72.0) * cm + self.v_spacing

        # Talla (directamente debajo del nombre del producto)
        talla_y = text_y - self.v_spacing

        # Ajustar tamaño de fuente para la talla según ancho disponible
        talla_font = 14
        while talla_font > 8 and c.stringWidth(self.talla, "Helvetica-Bold", talla_font) > self.content_width:
            talla_font -= 1
        c.setFont("Helvetica-Bold", talla_font)
        c.setFillColor(dark)
        c.drawCentredString(self.margin + self.content_width / 2, talla_y, self.talla)
        text_y = talla_y - (talla_font / 72.0) * cm - self.v_spacing

        # Precio (en un cuadro más compacto pero visible)
        precio_y = text_y - self.v_spacing
        # Ajuste de fuente del precio
        precio_font = 11
        while precio_font > 6 and c.stringWidth(self.precio, "Helvetica-Bold", precio_font) > self.content_width - (0.3 * cm):
            precio_font -= 1
        c.setFont("Helvetica-Bold", precio_font)

        # Calcular dimensiones del cuadro para el precio, no mayor que content_width
        padding_px = 6  # puntos
        price_box_width = min(self.content_width, c.stringWidth(self.precio, "Helvetica-Bold", precio_font) + padding_px)
        price_box_height = 0.5 * cm
        price_x = self.margin + (self.content_width - price_box_width) / 2

        # Establece las posiciones del rectángulo
        rect_y = precio_y - 0.05 * cm
        rect_height = price_box_height

        # Dibuja un recuadro de precio estilo 'pill' con fondo negro y texto dorado
        pill_x = price_x
        pill_y = rect_y
        pill_w = price_box_width
        pill_h = rect_height
        c.setFillColor(dark)
        c.setStrokeColor(gold)
        c.setLineWidth(0.6)
        c.roundRect(pill_x, pill_y, pill_w, pill_h, 1.5 * mm, stroke=1, fill=1)

        # Texto del precio en blanco sobre fondo oscuro (blanco/negro)
        c.setFillColor(colors.white)
        rect_center_y = pill_y + (pill_h / 2.3)
        font_offset = 2.5
        c.drawCentredString(self.margin + self.content_width / 2, rect_center_y - font_offset, self.precio)

        target_w = self.content_width
        bar_height = 0.75 * cm

        # --- Código de barras (Code128) - Ocupando el espacio restante ---
        espacio_disponible = rect_y - 0.3 * cm  # Espacio desde el precio hasta el borde inferior
        bar_height = min(1.2 * cm, espacio_disponible * 0.85)  # Usar 85% del espacio disponible
        target_w = self.width - 0.2 * cm  # Margen horizontal para el nuevo ancho

        # Código de barras: restaurado al estilo funcional original
        barcode = code128.Code128(
            self.barcode_value,
            barHeight=bar_height,
            barWidth=0.35 * mm,
            humanReadable=False
        )

        # Posición vertical base del código (debajo del precio)
        barcode_y = rect_y - 0.35 * cm - bar_height

        # Escala horizontal para encajar en target_w
        scale_x = min(1.0, target_w / barcode.width)

        # Centrado horizontal y dibujo del barcode escalado
        c.saveState()
        barcode_x = (self.width - barcode.width * scale_x) / 2.0
        c.translate(barcode_x, barcode_y)
        c.scale(scale_x, 1.0)
        barcode.drawOn(c, 0, 0)
        c.restoreState()

        # Número del código de barras debajo del código (legible)
        c.setFont("Helvetica", 6.5)
        c.setFillColor(dark)
        c.drawCentredString(self.width / 2, barcode_y - 0.2 * cm, self.barcode_value)

        # Restaurar el estado del canvas
        c.restoreState()


