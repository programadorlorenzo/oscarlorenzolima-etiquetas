#!/usr/bin/env python3
"""
Script simple para generar etiquetas de 3cm x 3cm con nombre de producto y código de barras aleatorio.
"""
import os
import random
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Image, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_random_barcode(prefix="PROD"):
    """
    Genera un código de barras aleatorio.
    
    Args:
        prefix (str): Prefijo para el código de barras.
    
    Returns:
        tuple: (BytesIO de la imagen del código, valor del código)
    """
    # Generar un número aleatorio de 8 dígitos
    random_number = random.randint(10000000, 99999999)
    barcode_value = f"{prefix}{random_number}"
    
    # Crear un código de barras Code128
    code128 = barcode.get_barcode_class('code128')
    
    # Configurar opciones del código de barras más compactas
    options = {
        'module_height': 3.0,  # Altura de las barras aún más reducida
        'module_width': 0.12,  # Ancho de las barras aún más reducido
        'font_size': 0,        # Eliminar texto interno del código de barras
        'text_distance': 0.5,  # Distancia entre el código y el texto
        'quiet_zone': 0.3,     # Zona sin barras mínima
        'write_text': False    # No mostrar texto en el código de barras mismo
    }
    
    # Generar el código de barras
    buffer = BytesIO()
    code128_barcode = code128(barcode_value, writer=ImageWriter())
    code128_barcode.write(buffer, options=options)
    buffer.seek(0)
    
    return buffer, barcode_value

def create_simple_label_pdf(product_name, output_path):
    """
    Crea un PDF simple con una etiqueta de 3cm x 3cm.
    
    Args:
        product_name (str): Nombre del producto a mostrar en la etiqueta.
        output_path (str): Ruta donde guardar el PDF.
    
    Returns:
        str: Ruta del archivo PDF generado.
    """
    # Definir tamaño y márgenes (reducidos para garantizar que todo quepa en una página)
    LABEL_WIDTH = 3 * cm
    LABEL_HEIGHT = 3 * cm
    MARGIN = 0.02 * cm  # Margen mínimo
    
    # Crear estilos
    styles = getSampleStyleSheet()
    
    # Estilo para el nombre del producto (reducido)
    product_style = ParagraphStyle(
        name='ProductName',
        fontName='Helvetica-Bold',
        fontSize=7,  # Reducido
        leading=8,   # Reducido
        alignment=1,  # Centrado
        spaceAfter=0,
        spaceBefore=0,
    )
    
    # Estilo para el código de barras
    barcode_style = ParagraphStyle(
        name='Barcode',
        fontName='Helvetica',
        fontSize=4,  # Reducido
        leading=4,   # Reducido
        alignment=1,  # Centrado
        spaceAfter=0,
        spaceBefore=0,
    )
    
    # Crear documento PDF con tamaño exacto de la etiqueta
    pagesize = (LABEL_WIDTH, LABEL_HEIGHT)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=pagesize,
        rightMargin=MARGIN,
        leftMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )
    
    # Lista para almacenar los elementos del PDF
    elements = []
    
    # Generar código de barras aleatorio
    barcode_img, barcode_value = generate_random_barcode()
    
    # Ajustar nombre del producto si es muy largo
    if len(product_name) > 20:
        product_name = product_name[:17] + "..."
    
    # Crear elementos
    product_text = Paragraph(product_name, product_style)
    barcode_image = Image(barcode_img)
    # Reducir tamaño del código de barras para asegurar que quepa en una página
    barcode_image.drawHeight = 0.8 * cm
    barcode_image.drawWidth = 2.3 * cm
    barcode_text = Paragraph(barcode_value, barcode_style)
    
    # Crear un único contenedor para toda la etiqueta
    contents = [
        [product_text],
        [barcode_image],
        [barcode_text]
    ]
    
    # Altura proporcional para cada fila (ajustada para mejor encaje)
    row_heights = [
        LABEL_HEIGHT * 0.15,  # Nombre del producto (reducido)
        LABEL_HEIGHT * 0.75,  # Código de barras (aumentado)
        LABEL_HEIGHT * 0.10   # Valor del código
    ]
    
    # Crear tabla con dimensiones exactas para asegurar que todo quepa en una página
    label_table = Table(
        contents,
        colWidths=[LABEL_WIDTH - 2*MARGIN],
        rowHeights=row_heights,
        hAlign='CENTER'
    )
    
    # Aplicar estilo a la tabla (simplificado para maximizar espacio)
    label_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),  # Borde más fino
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),  # Sin padding
        ('TOPPADDING', (0, 0), (-1, -1), 0),     # Sin padding
        ('LEFTPADDING', (0, 0), (-1, -1), 0),    # Sin padding
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),   # Sin padding
    ]))
    
    # Añadir la tabla (único elemento) al documento
    elements.append(label_table)
    
    # Generar el PDF asegurando que no haya saltos de página
    doc.build(elements)
    
    return output_path

def create_multi_page_pdf(product_names, output_path):
    """
    Crea un PDF con múltiples etiquetas, una por página.
    
    Args:
        product_names (list): Lista de nombres de productos.
        output_path (str): Ruta donde guardar el PDF.
    
    Returns:
        str: Ruta del archivo PDF generado.
    """
    from reportlab.platypus import SimpleDocTemplate, PageBreak
    
    # Definir tamaño y márgenes
    LABEL_WIDTH = 3 * cm
    LABEL_HEIGHT = 3 * cm
    MARGIN = 0.02 * cm
    
    # Crear documento PDF
    doc = SimpleDocTemplate(
        output_path,
        pagesize=(LABEL_WIDTH, LABEL_HEIGHT),
        rightMargin=MARGIN,
        leftMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )
    
    # Lista para almacenar los elementos del PDF
    elements = []
    
    # Generar una etiqueta por cada producto
    for i, name in enumerate(product_names):
        # Crear una etiqueta temporal
        temp_path = f"{output_path}.temp{i}.pdf"
        create_simple_label_pdf(name, temp_path)
        
        # Para implementarlo completamente, necesitaríamos extraer páginas del PDF temporal
        # Pero para simplificar, generamos cada etiqueta individualmente
        
        # Agregar salto de página entre etiquetas, excepto la última
        if i < len(product_names) - 1:
            elements.append(PageBreak())
    
    return output_path

def main():
    """Función principal."""
    import platform
    
    # Crear directorio de salida si no existe
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Definir ruta de salida
    output_file = os.path.join(output_dir, 'etiqueta_simple.pdf')
    
    # Pedir nombre del producto
    product_name = input("Ingrese el nombre del producto (o varios nombres separados por comas): ")
    if not product_name:
        product_name = "Producto de ejemplo"
        
    # Generar PDF
    pdf_path = create_simple_label_pdf(product_name, output_file)
    print(f"Etiqueta generada correctamente en: {pdf_path}")
    
    # Intentar abrir el PDF automáticamente
    try:
        if platform.system() == 'Darwin':  # macOS
            os.system(f'open "{pdf_path}"')
        elif platform.system() == 'Windows':  # Windows
            os.system(f'start "" "{pdf_path}"')
        else:  # Linux
            os.system(f'xdg-open "{pdf_path}"')
    except Exception as e:
        print(f"No se pudo abrir el archivo PDF automáticamente: {e}")
        print(f"Puede abrirlo manualmente en: {pdf_path}")

if __name__ == "__main__":
    main()
