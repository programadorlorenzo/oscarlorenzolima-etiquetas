import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
import sys
from reportlab.lib.units import cm
from excel_manager import ExcelManager
from generador_etiqueta import GeneradorEtiquetas

class EtiquetasApp:
    """Aplicación de GUI para gestionar etiquetas de productos."""
    
    def __init__(self, root):
        """Inicializa la interfaz gráfica.
        
        Args:
            root: Ventana raíz de Tkinter
        """
        self.root = root
        self.root.title("Generador de Etiquetas")
        self.root.geometry("1000x700")
        
        # Variables para almacenar datos del formulario
        self.var_nombre = tk.StringVar()
        self.var_nombre_etiqueta = tk.StringVar()
        self.var_variante = tk.StringVar()
        self.var_tamanio = tk.StringVar()
        self.var_posicion = tk.StringVar()
        self.var_sku = tk.StringVar()
        self.var_precio = tk.DoubleVar(value=0.0)
        self.var_stock = tk.IntVar(value=1)
        self.var_costo = tk.DoubleVar(value=0.0)
        self.var_precio_mayor = tk.DoubleVar(value=0.0)
        self.var_precio_almacen = tk.DoubleVar(value=0.0)
        self.var_precio_handtag = tk.DoubleVar(value=0.0)
        
        # Variable para el código de barras (generado automáticamente)
        self.var_barcode = tk.StringVar()
        
        # DataFrame para almacenar productos
        self.productos_df = pd.DataFrame(columns=[
            'Clasificación', 'Tipo de producto o servicio', 'Nombre Producto/Servicio',
            'Nombre Etiqueta', 'Variante', 'Tamanio', 'Posicion', 'Marca', 
            'Permite Decimal', 'Código Barras', 'SKU', 'Controla Stock',
            'Stock', 'Costo Neto', 'Precio Unitario', 'Precio x mayor',
            'Precio almacen', 'Precio handtag'
        ])
        
        # Configuración de la interfaz
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea todos los widgets de la interfaz."""
        # Frame principal con pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña 1: Agregar Productos Manualmente
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Agregar Productos")
        
        # Pestaña 2: Importar Excel
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Importar Excel")
        
        # Configurar contenido de la pestaña 1
        self._configurar_tab_agregar(tab1)
        
        # Configurar contenido de la pestaña 2
        self._configurar_tab_importar(tab2)
    
    def _configurar_tab_agregar(self, tab):
        """Configura la pestaña para agregar productos manualmente."""
        # Frame para el formulario
        form_frame = ttk.LabelFrame(tab, text="Datos del Producto")
        form_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        
        # Organizar en 3 columnas
        for i in range(3):
            form_frame.columnconfigure(i, weight=1)
        
        # Primera fila
        ttk.Label(form_frame, text="Nombre Producto:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_nombre, width=30).grid(row=0, column=0, padx=(120, 5), pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Nombre Etiqueta:").grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_nombre_etiqueta, width=30).grid(row=0, column=1, padx=(120, 5), pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="SKU:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_sku, width=20).grid(row=0, column=2, padx=(50, 5), pady=5, sticky=tk.W)
        
        # Segunda fila
        ttk.Label(form_frame, text="Variante:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_variante, width=20).grid(row=1, column=0, padx=(120, 5), pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Tamaño:").grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_tamanio, width=20).grid(row=1, column=1, padx=(120, 5), pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Posición:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_posicion, width=20).grid(row=1, column=2, padx=(70, 5), pady=5, sticky=tk.W)
        
        # Tercera fila
        ttk.Label(form_frame, text="Precio Unitario:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_precio, width=15).grid(row=2, column=0, padx=(120, 5), pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Precio Handtag:").grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_precio_handtag, width=15).grid(row=2, column=1, padx=(120, 5), pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Stock:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(form_frame, from_=0, to=1000, textvariable=self.var_stock, width=10).grid(row=2, column=2, padx=(70, 5), pady=5, sticky=tk.W)
        
        # Cuarta fila
        ttk.Label(form_frame, text="Costo Neto:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_costo, width=15).grid(row=3, column=0, padx=(120, 5), pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Precio x Mayor:").grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_precio_mayor, width=15).grid(row=3, column=1, padx=(120, 5), pady=5, sticky=tk.W)
        
        ttk.Label(form_frame, text="Precio Almacén:").grid(row=3, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_precio_almacen, width=15).grid(row=3, column=2, padx=(120, 5), pady=5, sticky=tk.W)
        
        # Botón para agregar producto
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Agregar Producto", command=self._agregar_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Generar Etiquetas PDF", command=self._generar_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exportar Excel", command=self._exportar_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar Tabla", command=self._limpiar_tabla).pack(side=tk.LEFT, padx=5)
        
        # Tabla para mostrar productos
        table_frame = ttk.LabelFrame(tab, text="Productos Agregados")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear Treeview para la tabla
        self.tree = ttk.Treeview(table_frame, columns=(
            "nombre", "variante", "tamanio", "posicion", "precio", "precio_handtag", "sku", "stock", "barcode"
        ), show="headings")
        
        # Definir encabezados
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("variante", text="Variante")
        self.tree.heading("tamanio", text="Tamaño")
        self.tree.heading("posicion", text="Posición")
        self.tree.heading("precio", text="Precio Unit.")
        self.tree.heading("precio_handtag", text="Precio Handtag")
        self.tree.heading("sku", text="SKU")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("barcode", text="Código Barras")
        
        # Configurar anchos de columnas
        self.tree.column("nombre", width=150)
        self.tree.column("variante", width=80)
        self.tree.column("tamanio", width=80)
        self.tree.column("posicion", width=80)
        self.tree.column("precio", width=80)
        self.tree.column("precio_handtag", width=100)
        self.tree.column("sku", width=100)
        self.tree.column("stock", width=50)
        self.tree.column("barcode", width=120)
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Binding para eliminar productos con doble clic
        self.tree.bind("<Double-1>", self._eliminar_producto)
    
    def _configurar_tab_importar(self, tab):
        """Configura la pestaña para importar Excel."""
        frame = ttk.Frame(tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="Importar archivo Excel con productos:").pack(pady=10)
        ttk.Button(frame, text="Seleccionar Archivo Excel", command=self._importar_excel).pack(pady=5)
        
        # Campo para mostrar la ruta del archivo
        self.var_excel_path = tk.StringVar()
        ttk.Entry(frame, textvariable=self.var_excel_path, width=50, state="readonly").pack(pady=5, fill=tk.X, padx=50)
        
        # Botón para procesar el archivo importado
        ttk.Button(frame, text="Cargar Productos desde Excel", command=self._cargar_desde_excel).pack(pady=10)
        
        # Etiqueta para mostrar información
        self.lbl_info = ttk.Label(frame, text="")
        self.lbl_info.pack(pady=10)
    
    def _agregar_producto(self):
        """Agrega un producto a la tabla temporal y al DataFrame."""
        # Validar datos básicos
        if not self.var_nombre.get().strip() or not self.var_sku.get().strip():
            messagebox.showerror("Error", "El nombre del producto y SKU son obligatorios")
            return
        
        # Si no se proporciona nombre para etiqueta, usar el nombre del producto
        if not self.var_nombre_etiqueta.get().strip():
            self.var_nombre_etiqueta.set(self.var_nombre.get())
        
        # Generar código de barras
        excel_manager = ExcelManager()
        barcode = excel_manager.generar_barcode(self.var_sku.get())
        
        # Crear un nuevo registro para el DataFrame
        nuevo_producto = {
            'Clasificación': 'Producto',
            'Tipo de producto o servicio': '',
            'Nombre Producto/Servicio': self.var_nombre.get(),
            'Nombre Etiqueta': self.var_nombre_etiqueta.get(),
            'Variante': self.var_variante.get(),
            'Tamanio': self.var_tamanio.get(),
            'Posicion': self.var_posicion.get(),
            'Marca': '',
            'Permite Decimal': 'No',
            'Código Barras': barcode,
            'SKU': self.var_sku.get(),
            'Controla Stock': 'Si',
            'Stock': self.var_stock.get(),
            'Costo Neto': self.var_costo.get(),
            'Precio Unitario': self.var_precio.get(),
            'Precio x mayor': self.var_precio_mayor.get(),
            'Precio almacen': self.var_precio_almacen.get(),
            'Precio handtag': self.var_precio_handtag.get()
        }
        
        # Agregar al DataFrame
        self.productos_df = pd.concat([self.productos_df, pd.DataFrame([nuevo_producto])], ignore_index=True)
        
        # Agregar a la tabla visual
        self.tree.insert("", tk.END, values=(
            self.var_nombre_etiqueta.get(),
            self.var_variante.get(),
            self.var_tamanio.get(),
            self.var_posicion.get(),
            f"S/ {self.var_precio.get():.2f}",
            f"S/ {self.var_precio_handtag.get():.2f}",
            self.var_sku.get(),
            self.var_stock.get(),
            barcode
        ))
        
        # Limpiar el formulario para un nuevo ingreso
        self._limpiar_formulario()
        
        messagebox.showinfo("Éxito", "Producto agregado correctamente")
    
    def _eliminar_producto(self, event):
        """Elimina un producto de la tabla al hacer doble clic."""
        item = self.tree.selection()[0]
        if item:
            if messagebox.askyesno("Confirmar Eliminación", "¿Desea eliminar este producto?"):
                # Obtener el SKU del producto seleccionado
                valores = self.tree.item(item, "values")
                sku = valores[6]  # El SKU está en la posición 6
                
                # Eliminar del DataFrame
                self.productos_df = self.productos_df[self.productos_df['SKU'] != sku]
                
                # Eliminar de la tabla visual
                self.tree.delete(item)
    
    def _limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.var_nombre.set("")
        self.var_nombre_etiqueta.set("")
        self.var_variante.set("")
        self.var_tamanio.set("")
        self.var_posicion.set("")
        self.var_sku.set("")
        self.var_precio.set(0.0)
        self.var_stock.set(1)
        self.var_costo.set(0.0)
        self.var_precio_mayor.set(0.0)
        self.var_precio_almacen.set(0.0)
        self.var_precio_handtag.set(0.0)
    
    def _limpiar_tabla(self):
        """Limpia toda la tabla de productos."""
        if messagebox.askyesno("Confirmar", "¿Desea eliminar todos los productos de la tabla?"):
            # Limpiar DataFrame
            self.productos_df = pd.DataFrame(columns=self.productos_df.columns)
            
            # Limpiar tabla visual
            for item in self.tree.get_children():
                self.tree.delete(item)
    
    def _importar_excel(self):
        """Abre un diálogo para seleccionar un archivo Excel."""
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx *.xls")]
        )
        if filepath:
            self.var_excel_path.set(filepath)
    
    def _cargar_desde_excel(self):
        """Carga productos desde un archivo Excel seleccionado."""
        filepath = self.var_excel_path.get()
        if not filepath:
            messagebox.showerror("Error", "Primero seleccione un archivo Excel")
            return
        
        try:
            # Leer Excel
            excel_manager = ExcelManager(filepath)
            excel_manager.cargar_excel()
            
            # Actualizar DataFrame
            self.productos_df = excel_manager.data
            
            # Limpiar tabla visual
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Mostrar productos en la tabla
            total_productos = 0
            for _, row in self.productos_df.iterrows():
                self.tree.insert("", tk.END, values=(
                    row.get('Nombre Etiqueta', '') or row.get('Nombre Producto/Servicio', ''),
                    row.get('Variante', ''),
                    row.get('Tamanio', ''),
                    row.get('Posicion', ''),
                    f"S/ {row.get('Precio Unitario', 0):.2f}",
                    f"S/ {row.get('Precio handtag', 0):.2f}",
                    row.get('SKU', ''),
                    row.get('Stock', 0),
                    row.get('Código Barras', '')
                ))
                total_productos += 1
            
            self.lbl_info.config(text=f"Se cargaron {total_productos} productos desde el Excel")
            messagebox.showinfo("Éxito", f"Se cargaron {total_productos} productos desde el Excel")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {e}")
    
    def _generar_pdf(self):
        """Genera un PDF con las etiquetas de todos los productos."""
        if self.productos_df.empty:
            messagebox.showerror("Error", "No hay productos para generar etiquetas")
            return
        
        try:
            # Crear directorio de salida si no existe
            if not os.path.exists("output"):
                os.makedirs("output")
            
            # Crear un ExcelManager temporal con nuestros datos
            excel_manager = ExcelManager()
            excel_manager.data = self.productos_df
            
            # Generar datos para etiquetas
            datos_etiquetas = excel_manager.generar_datos_etiquetas()
            
            if not datos_etiquetas:
                messagebox.showerror("Error", "No hay productos con stock para generar etiquetas")
                return
            
            # Crear generador de etiquetas
            generador = GeneradorEtiquetas("output/etiquetas_productos.pdf", custom_width=10.02*cm)
            
            # Generar PDF
            generador.generar_pdf(datos_etiquetas)
            
            messagebox.showinfo("Éxito", f"PDF generado en: output/etiquetas_productos.pdf\nSe generaron {len(datos_etiquetas)} etiquetas")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {e}")
    
    def _exportar_excel(self):
        """Exporta los productos a un archivo Excel."""
        if self.productos_df.empty:
            messagebox.showerror("Error", "No hay productos para exportar")
            return
        
        filepath = filedialog.asksaveasfilename(
            title="Guardar Excel",
            defaultextension=".xlsx",
            filetypes=[("Archivos Excel", "*.xlsx")]
        )
        
        if not filepath:
            return
        
        try:
            # Crear directorio si no existe
            output_dir = os.path.dirname(filepath)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Exportar DataFrame a Excel
            self.productos_df.to_excel(filepath, index=False)
            messagebox.showinfo("Éxito", f"Excel exportado exitosamente en: {filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar Excel: {e}")


def main():
    """Función principal para iniciar la aplicación."""
    # Force light mode on macOS
    import os
    os.environ['DARK_MODE_DISABLE'] = '1'  # This disables dark mode for the app
    
    root = tk.Tk()
    # Set background to light color
    root.configure(bg="white")
    # Configure ttk style to use light theme elements
    style = ttk.Style()
    style.theme_use('default')  # Using the default theme which is typically light
    
    app = EtiquetasApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()