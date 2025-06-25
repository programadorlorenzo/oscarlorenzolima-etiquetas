import pandas as pd
import os
import random
import hashlib

class ExcelManager:
    """Clase para manejar la importación y procesamiento de datos desde Excel."""
    
    def __init__(self, file_path=None):
        """Inicializa el manejador de Excel.
        
        Args:
            file_path: Ruta al archivo Excel a procesar
        """
        self.file_path = file_path
        self.data = None
    
    def cargar_excel(self, file_path=None):
        """Carga los datos desde un archivo Excel.
        
        Args:
            file_path: Ruta al archivo Excel (opcional si ya se proporcionó en __init__)
            
        Returns:
            DataFrame con los datos cargados
        """
        if file_path:
            self.file_path = file_path
            
        if not self.file_path:
            raise ValueError("No se ha especificado la ruta del archivo Excel")
            
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"El archivo Excel no existe en la ruta: {self.file_path}")
            
        try:
            # Leer el archivo Excel, asumiendo que la primera fila son encabezados
            self.data = pd.read_excel(self.file_path)
            print(f"✅ Archivo Excel cargado correctamente con {len(self.data)} productos")
            return self.data
        except Exception as e:
            print(f"❌ Error al cargar el archivo Excel: {e}")
            raise
    
    def generar_barcode(self, sku):
        """Genera un código de barras basado en el SKU.
        
        Args:
            sku: El SKU del producto
            
        Returns:
            String con el código de barras numérico que nunca comienza con cero
        """
        # Asegurarse de que el SKU sea un string
        sku_str = str(sku).strip()
        
        # Generar un hash MD5 basado en el SKU
        hash_object = hashlib.md5(sku_str.encode())
        hash_hex = hash_object.hexdigest()
        
        # Convertir parte del hash hexadecimal a un número
        hash_num = int(hash_hex[:8], 16)
        
        # Añadir un factor aleatorio pero consistente para el mismo SKU
        # Usamos el mismo SKU como semilla para el generador aleatorio
        random.seed(sku_str)
        random_factor = random.randint(1000, 9999)
        
        # Restaurar la semilla global después de usarla localmente
        random.seed()
        
        # Combinar el hash del SKU con el factor aleatorio para generar un código de barras
        combined_num = (hash_num + random_factor) % 999999999999  # 12 dígitos máximo
        
        # Asegurarnos de que el primer dígito no sea cero (1-9)
        first_digit = 7
        
        # Formatear el resto para que tenga 11 dígitos (total 12 con el primer dígito)
        rest_digits = str(combined_num).zfill(11)[-11:]
        
        # Combinar el primer dígito con el resto
        barcode = str(first_digit) + rest_digits
        
        return barcode
    
    def generar_datos_etiquetas(self):
        """Genera los datos para las etiquetas, replicando cada producto según su stock.
        
        Returns:
            Lista de diccionarios con los datos para generar las etiquetas
        """
        if self.data is None:
            raise ValueError("Primero debe cargar los datos con el método cargar_excel()")
            
        datos_etiquetas = []
        total_etiquetas = 0
        
        # Iterar por cada fila (producto) en el DataFrame
        for _, row in self.data.iterrows():
            # Obtener el stock del producto (asumiendo que es un entero positivo)
            stock = row.get('Stock', 0)
            try:
                stock = int(stock)
            except (ValueError, TypeError):
                print(f"⚠️ Advertencia: Stock no válido para {row.get('Nombre Producto/Servicio', '')}, utilizando 0")
                stock = 0
            
            # Obtener el SKU
            sku = str(row.get('SKU', ''))
            
            # Generar un único código de barras para este producto
            # Si ya tiene un código de barras, usarlo; si no, generarlo basado en el SKU
            barcode = str(row.get('Código Barras', '')).strip()
            if not barcode or barcode.lower() == 'nan':
                barcode = self.generar_barcode(sku)
            
            # Para cada unidad en stock, crear una etiqueta con el mismo código de barras
            for _ in range(max(0, stock)):
                etiqueta_data = {
                    'product_name': row.get('Nombre Producto/Servicio', ''),
                    'talla': row.get('Variante', ''),
                    'tamanio': row.get('Tamanio', ''),
                    'posicion': row.get('Posicion', ''),
                    'precio': f"S/ {row.get('Precio Unitario', 0):.2f}",
                    'sku': sku,
                    'barcode_value': barcode,
                    'image_path': 'assets/logo.png'
                }
                datos_etiquetas.append(etiqueta_data)
            
            total_etiquetas += stock
        
        print(f"✅ Generados datos para {total_etiquetas} etiquetas a partir de {len(self.data)} productos")
        return datos_etiquetas