"""
Módulo para la generación de etiquetas a partir de datos de Excel.
"""
import os
import pandas as pd
from utils.barcode_utils import generate_barcode
from utils.pdf_utils import create_label_pdf

class EtiquetaGenerator:
    """
    Clase para generar etiquetas a partir de datos de un archivo Excel.
    """
    
    def __init__(self):
        """Inicializa el generador de etiquetas."""
        self.data = None
        self.output_dir = os.path.join(os.path.dirname(__file__), 'output')
        
        # Crear directorio de salida si no existe
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def load_excel(self, excel_path):
        """
        Carga los datos desde un archivo Excel.
        
        Args:
            excel_path (str): Ruta al archivo Excel.
            
        Returns:
            bool: True si se cargó correctamente, False en caso contrario.
        """
        try:
            # Cargar el archivo Excel
            self.data = pd.read_excel(excel_path)
            
            # Verificar que existan las columnas requeridas
            required_columns = [
                'Nombre Producto/Servicio', 
                'Variante', 
                'Marca', 
                'Precio handtag',
                'SKU',
                'Stock'
            ]
            
            for column in required_columns:
                if column not in self.data.columns:
                    print(f"Error: La columna '{column}' no existe en el archivo Excel.")
                    return False
            
            return True
        except Exception as e:
            print(f"Error al cargar el archivo Excel: {str(e)}")
            return False
    
    def generate_labels(self, quantities=None, preview=False, use_stock=True):
        """
        Genera etiquetas para todos los productos en el archivo Excel.
        
        Args:
            quantities (dict, optional): Diccionario con SKU como clave y cantidad como valor.
                                        Si es None y use_stock es False, se genera una etiqueta por producto.
            preview (bool): Si es True, genera solo la primera etiqueta para previsualización.
            use_stock (bool): Si es True, se utilizará la columna Stock para determinar la cantidad
                             de etiquetas a generar, todas con el mismo código de barras para el mismo producto.
            
        Returns:
            str: Ruta al archivo PDF generado, o None si falla.
        """
        if self.data is None:
            print("Error: No se ha cargado ningún archivo Excel.")
            return None
        
        # Lista para almacenar los datos de las etiquetas
        labels_data = []
        
        # Para almacenar los códigos de barras ya generados por SKU
        barcode_cache = {}
        
        # Contador total de etiquetas
        total_etiquetas = 0
        
        # Procesar cada fila del Excel
        for _, row in self.data.iterrows():
            try:
                # Obtener datos del producto
                nombre = str(row['Nombre Producto/Servicio'])
                variante = str(row['Variante'])
                marca = str(row['Marca'])
                precio = str(row['Precio handtag'])
                sku = str(row['SKU'])
                
                # Determinar la cantidad de etiquetas a generar
                if use_stock and 'Stock' in row:
                    try:
                        stock = int(float(row['Stock']))
                        cantidad = stock if stock > 0 else 1
                    except (ValueError, TypeError):
                        cantidad = 1
                        print(f"Advertencia: No se pudo convertir el stock '{row['Stock']}' a número para el SKU {sku}. Usando 1.")
                elif quantities and sku in quantities:
                    cantidad = quantities[sku]
                else:
                    cantidad = 1
                
                # Generar o recuperar el código de barras para este SKU
                if sku in barcode_cache:
                    barcode_img, barcode_value = barcode_cache[sku]
                else:
                    barcode_img, barcode_value = generate_barcode(sku)
                    barcode_cache[sku] = (barcode_img, barcode_value)
                
                # Crear datos de la etiqueta
                label_data = {
                    'nombre': nombre,
                    'variante': variante,
                    'marca': marca,
                    'precio': precio,
                    'barcode_img': barcode_img,
                    'barcode_value': barcode_value,
                    'cantidad': cantidad
                }
                
                labels_data.append(label_data)
                total_etiquetas += cantidad
                
                print(f"Producto: {nombre} (SKU: {sku}) - Generando {cantidad} etiquetas con código: {barcode_value}")
                
                # Si es previsualización, solo procesar la primera fila
                if preview and len(labels_data) > 0:
                    break
                
            except Exception as e:
                print(f"Error al procesar producto {row.get('SKU', 'desconocido')}: {str(e)}")
        
        # Si no hay datos, salir
        if not labels_data:
            print("Error: No se encontraron datos válidos para generar etiquetas.")
            return None
        
        # Mostrar el total de etiquetas que se generarán
        if not preview:
            print(f"\nTotal de etiquetas a generar: {total_etiquetas}")
        
        # Generar el PDF con las etiquetas
        file_suffix = "_preview" if preview else ""
        output_file = os.path.join(self.output_dir, f"etiquetas{file_suffix}.pdf")
        
        try:
            pdf_path = create_label_pdf(labels_data, output_file, preview)
            print(f"Archivo PDF generado en: {pdf_path}")
            return pdf_path
        except Exception as e:
            print(f"Error al generar el PDF de etiquetas: {str(e)}")
            return None
