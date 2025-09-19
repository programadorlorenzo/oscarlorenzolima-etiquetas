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
        self.codigos_actualizados = False
    
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
            print(self.data.head())  # Mostrar las primeras filas para verificar la carga
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
        first_digit = 6
        
        # Formatear el resto para que tenga 11 dígitos (total 12 con el primer dígito)
        rest_digits = str(combined_num).zfill(11)[-11:]
        
        # Combinar el primer dígito con el resto
        barcode = str(first_digit) + rest_digits
        
        return barcode
    
    def generar_datos_etiquetas(self):
        """Genera los datos para las etiquetas, replicando cada producto según su stock.
        También actualiza los códigos de barras en el DataFrame original.
        
        Returns:
            Lista de diccionarios con los datos para generar las etiquetas
        """
        if self.data is None:
            raise ValueError("Primero debe cargar los datos con el método cargar_excel()")
            
        datos_etiquetas = []
        total_etiquetas = 0
        codigos_nuevos = {}  # Para registrar nuevos códigos generados
        
        # Iterar por cada fila (producto) en el DataFrame
        for indice, row in self.data.iterrows():
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
            codigo_generado = False
            
            if not barcode or barcode.lower() == 'nan':
                barcode = self.generar_barcode(sku)
                codigo_generado = True
                codigos_nuevos[indice] = barcode  # Guardar para actualizar después
            
            # Para cada unidad en stock, crear una etiqueta con el mismo código de barras
            for _ in range(max(0, stock)):
                etiqueta_data = {
                    'product_name': row.get('Nombre Etiqueta', '') or row.get('Nombre Producto/Servicio', ''),
                    'talla': row.get('Variante', ''),
                    'tamanio': row.get('Tamanio', ''),
                    'posicion': row.get('Posicion', ''),
                    'fit': row.get('Fit', ''),
                    'precio': f"S/ {row.get('Precio handtag', 0):.2f}",
                    'sku': sku,
                    'barcode_value': barcode,
                    'image_path': 'assets/logo.png'
                }
                datos_etiquetas.append(etiqueta_data)
            
            total_etiquetas += stock
        
        # Actualizar los códigos de barras nuevos en el DataFrame
        if codigos_nuevos:
            for indice, codigo in codigos_nuevos.items():
                self.data.at[indice, 'Código Barras'] = codigo
            self.codigos_actualizados = True
            print(f"✅ Se generaron {len(codigos_nuevos)} nuevos códigos de barras")
        
        print(f"✅ Generados datos para {total_etiquetas} etiquetas a partir de {len(self.data)} productos")
        return datos_etiquetas
    
    def guardar_excel(self, output_path=None):
        """Guarda los datos actualizados con los nuevos códigos de barras al archivo Excel.
        
        Args:
            output_path: Ruta para guardar el Excel actualizado (si es None, sobrescribe el original)
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        if self.data is None or not self.codigos_actualizados:
            print("⚠️ No hay datos o códigos de barras actualizados para guardar")
            return False
        
        # Si no se especifica ruta de salida, usar la original
        if output_path is None:
            output_path = self.file_path
        
        try:
            # Crear el directorio de salida si no existe
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Guardar el DataFrame actualizado al archivo Excel
            self.data.to_excel(output_path, index=False)
            print(f"✅ Archivo Excel actualizado guardado en: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Error al guardar el archivo Excel: {e}")
            return False