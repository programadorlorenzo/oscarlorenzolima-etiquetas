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
        self.image_path = datos.get('image_path', 'logo.png')
        
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
        c.setFont("Helvetica", 5)
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


class GeneradorEtiquetas:
    """Clase para generar un PDF con múltiples etiquetas."""
    
    def __init__(self, output_file="etiquetas.pdf", custom_width=10.02*cm):
        """Inicializa el generador de etiquetas.
        
        Args:
            output_file: Ruta del archivo PDF a generar
            custom_width: Ancho personalizado de la página (default: 10.02cm)
        """
        # Dimensiones de etiquetas (ajustado para optimizar el espacio)
        self.etiqueta_width = 3.05 * cm  # Ligeramente reducido para evitar advertencias
        self.etiqueta_height = 4 * cm
        
        # Espacio entre etiquetas (muy reducido para acercar las etiquetas)
        self.padding_x = 0.2 * cm   # Mínimo espacio horizontal
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
                'image_path': 'logo.png'
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


# Función principal
def main():
    """Función principal para generar las etiquetas."""
    # Crear generador de etiquetas con página de 10.02cm de ancho
    generador = GeneradorEtiquetas("etiquetas_multiple.pdf", custom_width=10.02*cm)
    
    # Generar datos de ejemplo (múltiplos de 3 para páginas completas)
    datos_etiquetas = generador.generar_mockup_datos(51)  # 17 páginas con 3 etiquetas cada una
    
    # Generar PDF con etiquetas
    generador.generar_pdf(datos_etiquetas)


if __name__ == "__main__":
    main()
