# Generador de Etiquetas para Ropa

Una aplicación para generar etiquetas de ropa a partir de un archivo Excel, creando un PDF listo para impresión.

## Características

- Interfaz gráfica fácil de usar
- Carga de datos desde archivos Excel
- Generación de códigos de barras únicos
- Previsualización de etiquetas antes de generación final
- Control del número de etiquetas por producto
- Diseño limpio y legible, formato 3x3 cm
- Exportación a PDF multipágina listo para impresión

## Requisitos del Sistema

- Python 3.6 o superior
- Las dependencias listadas en `requirements.txt`

## Instalación

1. Clone o descargue este repositorio
2. Cree un entorno virtual (opcional pero recomendado):
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows use: venv\Scripts\activate
   ```
3. Instale las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso

1. Ejecute la aplicación:
   ```
   python main.py
   ```
2. En la interfaz:
   - Haga clic en "Buscar" para seleccionar un archivo Excel
   - Elija si desea usar el stock del Excel para generar las etiquetas (una etiqueta por cada unidad en stock)
     * Si esta opción está activada, se generará una etiqueta por cada unidad en stock, todas con el mismo código de barras para el mismo producto
     * Si esta opción está desactivada, puede ajustar manualmente las cantidades de etiquetas para cada producto
   - Use "Previsualizar Etiquetas" para ver una muestra antes de generar todas
   - Haga clic en "Generar Etiquetas" para crear el PDF final con todas las etiquetas
   - Abra el PDF generado cuando se le solicite

3. Nota sobre los códigos de barras:
   - Si usa el stock para generar etiquetas, todas las unidades del mismo producto tendrán el mismo código de barras
   - Cada etiqueta se generará en una página separada del PDF para facilitar la impresión individual

## Formato del Archivo Excel

El archivo Excel debe contener las siguientes columnas:
- Clasificación
- Tipo de producto o servicio
- Nombre Producto/Servicio (requerido)
- Variante (requerido)
- Marca (requerido)
- Permite Decimal
- Código Barras
- SKU (requerido)
- Controla Stock
- Stock (requerido) - Se usa para generar una etiqueta por cada unidad en stock
- Costo Neto
- Precio Unitario
- Precio x mayor
- Precio almacen
- Precio handtag (requerido)

## Estructura del Proyecto

```
etiqueta_generator/
├── main.py
├── gui.py
├── etiquetas.py
├── utils/
│   ├── barcode_utils.py
│   └── pdf_utils.py
├── assets/
│   └── fonts/
├── output/
├── requirements.txt
└── README.md
```

## Personalización

Si desea personalizar el diseño de las etiquetas, puede modificar el archivo `pdf_utils.py` en la función `create_label_pdf()`.
