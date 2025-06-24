"""
Utilidades para generar archivos PDF con etiquetas.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Image, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Definir tamaño de etiqueta
LABEL_WIDTH = 3 * cm
LABEL_HEIGHT = 3 * cm
MARGIN = 0.5 * cm

# Registrar fuentes personalizadas
def register_fonts():
    """Registra las fuentes personalizadas para las etiquetas."""
    font_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'fonts')
    
    # Registrar la fuente Arial (o similar) si está disponible
    try:
        pdfmetrics.registerFont(TTFont('Arial', os.path.join(font_dir, 'arial.ttf')))
    except:
        # Si no está disponible, usamos Helvetica que viene por defecto
        pass

# Crear estilos para el texto
def get_styles():
    """Define y retorna estilos para los textos en la etiqueta."""
    styles = getSampleStyleSheet()
    
    # Estilo para el título del producto
    title_style = ParagraphStyle(
        name='ProductTitle',
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=8,
        alignment=1,  # Centrado
    )
    
    # Estilo para la marca
    brand_style = ParagraphStyle(
        name='Brand',
        fontName='Helvetica',
        fontSize=9,
        leading=10,
        alignment=1,  # Centrado
    )
    
    # Estilo para la talla
    size_style = ParagraphStyle(
        name='Size',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=12,
        alignment=1,  # Centrado
    )
    
    # Estilo para el precio
    price_style = ParagraphStyle(
        name='Price',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=11,
        alignment=1,  # Centrado
    )
    
    return {
        'title': title_style,
        'brand': brand_style,
        'size': size_style,
        'price': price_style
    }

def create_label_pdf(labels_data, output_path, preview=False):
    """
    Crea un archivo PDF con las etiquetas de productos, una etiqueta por página.
    
    Args:
        labels_data (list): Lista de diccionarios con datos para cada etiqueta.
            Cada diccionario debe contener: {
                'nombre': str,
                'variante': str,
                'marca': str,
                'precio': str,
                'barcode_img': BytesIO,
                'barcode_value': str,
                'cantidad': int
            }
        output_path (str): Ruta donde guardar el PDF.
        preview (bool): Si es True, genera solo la primera etiqueta para previsualización.
    
    Returns:
        str: Ruta del archivo PDF generado.
    """
    # Registrar fuentes
    register_fonts()
    
    # Obtener estilos
    styles = get_styles()
    
    # Crear documento PDF con tamaño de página igual al tamaño de una etiqueta más márgenes
    from reportlab.lib.pagesizes import portrait
    pagesize = (LABEL_WIDTH + 2*MARGIN, LABEL_HEIGHT + 2*MARGIN)
    
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
    
    # Contador para mostrar progreso
    label_count = 0
    total_labels = sum(label_data['cantidad'] for label_data in labels_data if not preview)
    
    # Procesar cada etiqueta
    for label_data in labels_data:
        # Si es una previsualización, solo generar una etiqueta
        quantity = 1 if preview else label_data['cantidad']
        
        for _ in range(quantity):
            # Actualizar contador
            label_count += 1
            if label_count % 100 == 0:
                print(f"Procesando etiqueta {label_count} de {total_labels}...")
            
            # Crear la etiqueta
            label_elements = []
            
            # Marca (en grande)
            brand = Paragraph(f"<b>{label_data['marca']}</b>", styles['brand'])
            
            # Nombre del producto (reducido si es muy largo)
            nombre = label_data['nombre']
            if len(nombre) > 25:
                nombre = nombre[:22] + "..."
            product_name = Paragraph(nombre, styles['title'])
            
            # Talla/Variante
            size = Paragraph(f"<b>Talla {label_data['variante']}</b>", styles['size'])
            
            # Precio
            price = Paragraph(f"S/ {label_data['precio']}", styles['price'])
            
            # Código de barras como imagen
            barcode_img = Image(label_data['barcode_img'])
            barcode_img.drawHeight = 0.8 * cm
            barcode_img.drawWidth = 2.5 * cm
            
            # Valor del código de barras como texto
            barcode_text = Paragraph(label_data['barcode_value'], styles['title'])
            
            # Crear tabla para esta etiqueta
            label_table = Table(
                [[brand], [product_name], [size], [price], [barcode_img], [barcode_text]],
                colWidths=[LABEL_WIDTH],
                rowHeights=[LABEL_HEIGHT/6] * 6  # Dividir altura para 6 elementos
            )
            
            # Estilo para la etiqueta
            label_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ]))
            
            # Añadir la etiqueta a la lista de elementos
            elements.append(label_table)
            
            # Salto de página después de cada etiqueta
            if not (preview and len(elements) >= 1) and _ < quantity - 1 or label_data != labels_data[-1]:
                elements.append(PageBreak())
            
            # Si es previsualización, salir después de la primera etiqueta
            if preview:
                break
        
        if preview and len(elements) > 0:
            break
    
    # Generar el PDF
    doc.build(elements)
    
    return output_path
