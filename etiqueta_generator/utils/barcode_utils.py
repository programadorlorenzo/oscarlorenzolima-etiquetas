"""
Utilidades para generar códigos de barras para las etiquetas.
"""
import random
import barcode
from barcode.writer import ImageWriter
from io import BytesIO

def generate_barcode(sku, size=None):
    """
    Genera un código de barras a partir del SKU más un número aleatorio único.
    
    Args:
        sku (str): El SKU del producto.
        size (tuple): Tamaño del código de barras (ancho, alto).
    
    Returns:
        BytesIO: Imagen del código de barras.
    """
    # Agregar un número aleatorio de 4 dígitos al SKU para hacerlo único
    random_number = random.randint(1000, 9999)
    barcode_value = f"{sku}{random_number}"
    
    # Asegurar que el código de barras tenga una longitud adecuada para Code128
    if len(barcode_value) < 6:
        barcode_value = barcode_value.zfill(6)
    
    # Crear un código de barras Code128
    code128 = barcode.get_barcode_class('code128')
    
    # Configurar opciones del código de barras
    options = {
        'module_height': 5.0,  # Altura de las barras
        'module_width': 0.2,   # Ancho de las barras
        'font_size': 7,        # Tamaño de la fuente
        'text_distance': 1.0,  # Distancia entre el código y el texto
        'quiet_zone': 1.0      # Zona sin barras alrededor del código
    }
    
    # Generar el código de barras
    buffer = BytesIO()
    code128_barcode = code128(barcode_value, writer=ImageWriter())
    code128_barcode.write(buffer, options=options)
    buffer.seek(0)
    
    return buffer, barcode_value
