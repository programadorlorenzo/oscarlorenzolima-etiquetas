import pandas as pd
import os

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
            
            # Para cada unidad en stock, crear una etiqueta
            for _ in range(max(0, stock)):
                etiqueta_data = {
                    'product_name': row.get('Nombre Producto/Servicio', ''),
                    'talla': row.get('Variante', ''),
                    'tamanio': row.get('Tamanio', ''),
                    'posicion': row.get('Posicion', ''),
                    'precio': f"S/ {row.get('Precio handtag', 0):.2f}",
                    'sku': str(row.get('SKU', '')),
                    'barcode_value': str(row.get('Código Barras', '')),
                    'image_path': 'assets/logo.png'
                }
                datos_etiquetas.append(etiqueta_data)
            
            total_etiquetas += stock
        
        print(f"✅ Generados datos para {total_etiquetas} etiquetas a partir de {len(self.data)} productos")
        return datos_etiquetas