from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from PIL import Image

# Datos
pdf_file = "etiqueta_jean.pdf"
barcode_value = "123456789012"
product_name = "Jean Ballion Grenish Blue Pet. Cad."
talla = "Talla 26"
precio = "S/ 115.00"
sku = "52505-R-VM268840"  # Añadimos el SKU
image_path = "logo.png"  # Cambia esto a tu imagen

# Dimensiones del PDF (3 cm x 3 cm)
width = 3 * cm
height = 3 * cm

# Crear canvas
c = canvas.Canvas(pdf_file, pagesize=(width, height))

# Insertar imagen (arriba del código de barras) - más pequeña
try:
    img = Image.open(image_path)
    img_width = 1.8 * cm  # Reducido de 2.5 cm a 1.8 cm
    img_height = img.size[1] * (img_width / img.size[0])
    img_x = (width - img_width) / 2
    img_y = height - img_height - 0.1 * cm
    c.drawImage(image_path, img_x, img_y, img_width, img_height, preserveAspectRatio=True)
except Exception as e:
    print("Error al cargar imagen:", e)

# Nombre del producto (debajo de imagen)
text_y = img_y - 0.3 * cm
c.setFont("Helvetica", 5)
c.drawCentredString(width / 2, text_y, product_name)

# Talla (debajo del nombre) - mismo formato que el nombre del producto
talla_y = text_y - 0.25 * cm  # Reducido el espacio
c.setFont("Helvetica", 5)  # Mismo formato que el nombre
c.drawCentredString(width / 2, talla_y, talla)

# Precio (ahora arriba del código de barras) en un cuadro
precio_y = talla_y - 0.45 * cm
c.setFont("Helvetica-Bold", 7)

# Calcular dimensiones del cuadro para el precio
price_box_width = c.stringWidth(precio, "Helvetica-Bold", 7) + 10  # Aumentamos un poco el ancho
price_box_height = 0.3 * cm
price_x = (width - price_box_width) / 2

# Establece las posiciones del rectángulo
rect_y = precio_y - 0.05 * cm
rect_height = price_box_height

# Dibuja el rectángulo para el precio
c.setStrokeColor(colors.black)
c.setLineWidth(0.3)
c.rect(price_x, rect_y, price_box_width, rect_height)

# Para centrar perfectamente el texto, calculamos el centro exacto del rectángulo
rect_center_y = rect_y + (rect_height / 2)

# En ReportLab, el texto se dibuja desde la línea base, así que necesitamos ajustar:
# Para una fuente de tamaño 7, un offset de aproximadamente 2.5 puntos funciona bien
font_offset = 2.5
c.drawCentredString(width / 2, rect_center_y - font_offset, precio)

# Código de barras (centro)
barcode = code128.Code128(barcode_value, barHeight=0.6 * cm, barWidth=0.025 * cm)  # Altura reducida
barcode_x = (width - barcode.width) / 2
barcode_y = precio_y - 0.85 * cm  # Ajustado para dar espacio al cuadro del precio
barcode.drawOn(c, barcode_x, barcode_y)

# Número del código de barras debajo del código
c.setFont("Helvetica", 4)
c.drawCentredString(width / 2, barcode_y - 0.18 * cm, barcode_value)

# SKU (al final con letra pequeña)
c.setFont("Helvetica", 3.5)  # Letra muy pequeña
sku_y = 0.15 * cm  # En la parte inferior
c.drawCentredString(width / 2, sku_y, sku)

# Dibujar un borde alrededor de toda la etiqueta
c.setStrokeColor(colors.black)
c.setLineWidth(0.25)
c.rect(0.05 * cm, 0.05 * cm, width - 0.1 * cm, height - 0.1 * cm)

# Finalizar PDF
c.showPage()
c.save()

print(f"✅ PDF generado: {pdf_file}")
