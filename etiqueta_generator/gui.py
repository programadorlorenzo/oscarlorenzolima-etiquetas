"""
Interfaz gráfica para el generador de etiquetas.
"""
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import subprocess
import platform
import pandas as pd
from etiquetas import EtiquetaGenerator

# Configuración para compatibilidad con sistemas operativos
def check_system_compatibility():
    """Comprueba la compatibilidad con el sistema operativo y hace ajustes si es necesario."""
    # Silenciar advertencia de deprecación de Tk en macOS
    if platform.system() == "Darwin":
        os.environ['TK_SILENCE_DEPRECATION'] = '1'
        
        # Solución para problemas de visualización en macOS con pantallas Retina
        os.environ['PYTHONCOERCECLOCALE'] = '0'
        os.environ['LANG'] = 'en_US.UTF-8'
        
        # Configuración específica para dark mode en macOS
        if os.system('defaults read -g AppleInterfaceStyle 2>/dev/null') == 0:
            # El sistema está en dark mode, configurar variables para compatibilidad
            os.environ['DARK_MODE'] = '1'
    
    # Ajustes para Windows
    elif platform.system() == "Windows":
        # Configuraciones específicas para Windows si son necesarias
        pass

# Llamar a la función al importar el módulo
check_system_compatibility()

class EtiquetaGeneratorGUI:
    """
    Clase para la interfaz gráfica del generador de etiquetas.
    """
    
    def __init__(self, root):
        """
        Inicializa la interfaz gráfica.
        
        Args:
            root (tk.Tk): La ventana principal de Tkinter.
        """
        self.root = root
        self.root.title("Generador de Etiquetas")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        
        # Configurar colores para asegurar visibilidad
        self.bg_color = '#f0f0f0'  # Color de fondo estándar
        self.fg_color = '#000000'  # Color de texto negro
        self.accent_color = '#4a7abc'  # Color de acento para elementos destacados
        
        # Configurar estilo para widgets ttk
        self.style = ttk.Style()
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.fg_color)
        self.style.configure('TButton', background=self.bg_color)
        self.style.configure('TLabelframe', background=self.bg_color)
        self.style.configure('TLabelframe.Label', background=self.bg_color, foreground=self.fg_color)
        
        # Aplicar el color de fondo a la ventana principal
        self.root.configure(background=self.bg_color)
        
        # Generador de etiquetas
        self.etiqueta_generator = EtiquetaGenerator()
        
        # Variables
        self.excel_path = tk.StringVar()
        self.status_var = tk.StringVar(value="Esperando selección de archivo Excel...")
        self.preview_pdf_path = None
        self.final_pdf_path = None
        
        # Configurar la interfaz
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura los elementos de la interfaz gráfica."""
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="10", style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Generador de Etiquetas para Ropa", 
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para selección de archivo
        file_frame = ttk.LabelFrame(main_frame, text="Selección de Archivo Excel", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campo para ruta del archivo
        excel_entry = ttk.Entry(file_frame, textvariable=self.excel_path, width=50)
        excel_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        # Botón para buscar archivo
        browse_button = ttk.Button(
            file_frame, 
            text="Buscar", 
            command=self._browse_excel
        )
        browse_button.pack(side=tk.RIGHT)
        
        # Frame para opciones
        options_frame = ttk.LabelFrame(main_frame, text="Opciones de Generación", padding="10")
        options_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Variable para la opción de usar stock
        self.use_stock_var = tk.BooleanVar(value=True)
        
        # Checkbox para usar el stock del Excel
        self.use_stock_check = ttk.Checkbutton(
            options_frame,
            text="Usar el stock del Excel para generar cantidad de etiquetas",
            variable=self.use_stock_var
        )
        self.use_stock_check.pack(anchor=tk.W, pady=(0, 10))
        
        # Aquí se agregarán las opciones para cantidad de etiquetas
        # Este frame se actualizará cuando se cargue un archivo Excel
        self.options_content_frame = ttk.Frame(options_frame)
        self.options_content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.loading_label = ttk.Label(
            self.options_content_frame, 
            text="Seleccione un archivo Excel para ver las opciones de productos.",
            font=("Helvetica", 10, "italic")
        )
        self.loading_label.pack(pady=20)
        
        # Frame para acciones
        actions_frame = ttk.Frame(main_frame)
        actions_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botón para previsualizar
        preview_button = ttk.Button(
            actions_frame, 
            text="Previsualizar Etiquetas", 
            command=self._preview_labels
        )
        preview_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón para generar todas las etiquetas
        generate_button = ttk.Button(
            actions_frame, 
            text="Generar Etiquetas", 
            command=self._generate_labels
        )
        generate_button.pack(side=tk.LEFT)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 5))
        
        # Etiqueta de estado
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Helvetica", 9))
        status_label.pack(fill=tk.X)
    
    def _browse_excel(self):
        """Abre un diálogo para seleccionar un archivo Excel."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar Archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx *.xls")]
        )
        
        if file_path:
            self.excel_path.set(file_path)
            self.status_var.set("Cargando archivo Excel...")
            self.progress.start()
            
            # Usar un hilo para no bloquear la UI
            threading.Thread(target=self._load_excel_data, args=(file_path,)).start()
    
    def _load_excel_data(self, file_path):
        """
        Carga los datos del archivo Excel.
        
        Args:
            file_path (str): Ruta al archivo Excel.
        """
        success = self.etiqueta_generator.load_excel(file_path)
        
        # Actualizar la interfaz en el hilo principal
        self.root.after(0, lambda: self._update_ui_after_load(success))
    
    def _update_ui_after_load(self, success):
        """
        Actualiza la interfaz después de cargar el Excel.
        
        Args:
            success (bool): True si se cargó correctamente, False en caso contrario.
        """
        self.progress.stop()
        
        if success:
            self.status_var.set("Archivo Excel cargado correctamente.")
            self._update_options_frame()
        else:
            self.status_var.set("Error al cargar el archivo Excel.")
            messagebox.showerror(
                "Error", 
                "No se pudo cargar el archivo Excel o no contiene las columnas requeridas."
            )
        
        # Asegurar que la interfaz se muestra correctamente
        self._ensure_proper_display()
    
    def _update_options_frame(self):
        """Actualiza el frame de opciones con los productos del Excel."""
        # Limpiar el frame de opciones
        for widget in self.options_content_frame.winfo_children():
            widget.destroy()
        
        if self.etiqueta_generator.data is None or len(self.etiqueta_generator.data) == 0:
            self.loading_label = ttk.Label(
                self.options_content_frame, 
                text="No hay datos de productos disponibles.",
                font=("Helvetica", 10, "italic")
            )
            self.loading_label.pack(pady=20)
            return
        
        # Crear un frame con scrollbar para la lista de productos
        scroll_frame = ttk.Frame(self.options_content_frame)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas para el scroll
        canvas = tk.Canvas(scroll_frame, yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configurar scrollbar
        scrollbar.config(command=canvas.yview)
        
        # Frame interno para los productos
        products_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=products_frame, anchor=tk.NW)
        
        # Etiquetas de encabezado
        ttk.Label(products_frame, text="SKU", font=("Helvetica", 9, "bold")).grid(row=0, column=0, padx=5, sticky=tk.W)
        ttk.Label(products_frame, text="Producto", font=("Helvetica", 9, "bold")).grid(row=0, column=1, padx=5, sticky=tk.W)
        ttk.Label(products_frame, text="Stock", font=("Helvetica", 9, "bold")).grid(row=0, column=2, padx=5, sticky=tk.W)
        ttk.Label(products_frame, text="Cantidad Manual", font=("Helvetica", 9, "bold")).grid(row=0, column=3, padx=5, sticky=tk.W)
        
        # Crear entradas para cada producto
        self.quantity_vars = {}
        self.quantity_spinboxes = []  # Para almacenar los spinboxes
        
        for i, (_, row) in enumerate(self.etiqueta_generator.data.iterrows(), 1):
            sku = str(row['SKU'])
            product_name = str(row['Nombre Producto/Servicio'])
            
            # Truncar el nombre si es muy largo
            if len(product_name) > 30:
                product_name = product_name[:27] + "..."
            
            # SKU
            ttk.Label(products_frame, text=sku).grid(row=i, column=0, padx=5, pady=2, sticky=tk.W)
            
            # Nombre del producto
            ttk.Label(products_frame, text=product_name).grid(row=i, column=1, padx=5, pady=2, sticky=tk.W)
            
            # Stock
            stock = row.get('Stock', 0)
            try:
                stock_value = int(float(stock)) if pd.notna(stock) else 0
            except (ValueError, TypeError):
                stock_value = 0
                
            ttk.Label(products_frame, text=str(stock_value)).grid(row=i, column=2, padx=5, pady=2, sticky=tk.W)
            
            # Cantidad manual
            quantity_var = tk.StringVar(value="1")
            self.quantity_vars[sku] = quantity_var
            
            quantity_entry = ttk.Spinbox(
                products_frame,
                from_=1,
                to=100,
                width=5,
                textvariable=quantity_var,
                state="disabled" if self.use_stock_var.get() else "normal"  # Estado inicial según la opción
            )
            quantity_entry.grid(row=i, column=3, padx=5, pady=2)
            self.quantity_spinboxes.append(quantity_entry)
        
        # Actualizar scrollregion después de agregar todos los widgets
        products_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox(tk.ALL))
        
        # Configurar la función de callback para la casilla de verificación
        self.use_stock_var.trace_add("write", self._toggle_quantity_entries)
        
    def _toggle_quantity_entries(self, *args):
        """
        Activa o desactiva las entradas de cantidad según la opción de usar stock.
        """
        use_stock = self.use_stock_var.get()
        state = "disabled" if use_stock else "normal"
        
        # Actualizar estado de los spinboxes
        if hasattr(self, 'quantity_spinboxes'):
            for spinbox in self.quantity_spinboxes:
                spinbox.configure(state=state)
        
        # Mensaje informativo
        if use_stock:
            self.status_var.set("Se utilizará el stock del Excel para generar las etiquetas")
        else:
            self.status_var.set("Se utilizarán las cantidades especificadas manualmente")
    
    def _get_quantities(self):
        """
        Obtiene las cantidades de etiquetas especificadas por el usuario.
        
        Returns:
            dict: Diccionario con SKU como clave y cantidad como valor.
        """
        quantities = {}
        
        for sku, var in self.quantity_vars.items():
            try:
                qty = int(var.get())
                if qty > 0:
                    quantities[sku] = qty
            except ValueError:
                # Si no es un número válido, usar 1 por defecto
                quantities[sku] = 1
        
        return quantities
    
    def _preview_labels(self):
        """Genera una previsualización de las etiquetas."""
        if self.etiqueta_generator.data is None:
            messagebox.showwarning(
                "Advertencia", 
                "Debe cargar un archivo Excel primero."
            )
            return
        
        self.status_var.set("Generando previsualización...")
        self.progress.start()
        
        # Usar un hilo para no bloquear la UI
        threading.Thread(target=self._generate_preview).start()
    
    def _generate_preview(self):
        """Genera la previsualización en un hilo separado."""
        # Generar una etiqueta de muestra
        pdf_path = self.etiqueta_generator.generate_labels(preview=True)
        
        # Actualizar la interfaz en el hilo principal
        self.root.after(0, lambda: self._open_pdf(pdf_path, is_preview=True))
    
    def _generate_labels(self):
        """Genera todas las etiquetas."""
        if self.etiqueta_generator.data is None:
            messagebox.showwarning(
                "Advertencia", 
                "Debe cargar un archivo Excel primero."
            )
            return
        
        self.status_var.set("Generando etiquetas...")
        self.progress.start()
        
        # Obtener las cantidades especificadas
        quantities = self._get_quantities()
        
        # Usar un hilo para no bloquear la UI
        threading.Thread(target=self._generate_all_labels, args=(quantities,)).start()
    
    def _generate_all_labels(self, quantities):
        """
        Genera todas las etiquetas en un hilo separado.
        
        Args:
            quantities (dict): Diccionario con SKU como clave y cantidad como valor.
        """
        # Obtener el estado de la opción de usar stock
        use_stock = self.use_stock_var.get()
        
        # Mostrar mensaje informativo
        if use_stock:
            print("Generando etiquetas usando el stock del Excel")
        else:
            print("Generando etiquetas usando las cantidades especificadas en la interfaz")
        
        # Generar todas las etiquetas
        pdf_path = self.etiqueta_generator.generate_labels(
            quantities=quantities if not use_stock else None,
            use_stock=use_stock
        )
        
        # Actualizar la interfaz en el hilo principal
        self.root.after(0, lambda: self._open_pdf(pdf_path))
    
    def _open_pdf(self, pdf_path, is_preview=False):
        """
        Abre el PDF generado.
        
        Args:
            pdf_path (str): Ruta al archivo PDF.
            is_preview (bool): True si es una previsualización, False si es el PDF final.
        """
        self.progress.stop()
        
        if pdf_path:
            if is_preview:
                self.status_var.set("Previsualización generada correctamente.")
                self.preview_pdf_path = pdf_path
            else:
                self.status_var.set("Etiquetas generadas correctamente.")
                self.final_pdf_path = pdf_path
            
            # Preguntar si desea abrir el PDF
            if messagebox.askyesno(
                "PDF Generado", 
                f"El PDF se ha generado correctamente en:\n{pdf_path}\n\n¿Desea abrirlo ahora?"
            ):
                self._open_file(pdf_path)
        else:
            status = "Error al generar la previsualización." if is_preview else "Error al generar las etiquetas."
            self.status_var.set(status)
            messagebox.showerror(
                "Error", 
                "No se pudo generar el archivo PDF de etiquetas."
            )
    
    def _open_file(self, file_path):
        """
        Abre un archivo con la aplicación predeterminada del sistema.
        
        Args:
            file_path (str): Ruta al archivo.
        """
        try:
            # Abrir el archivo con la aplicación predeterminada según el sistema operativo
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', file_path))
            elif platform.system() == 'Windows':  # Windows
                os.startfile(file_path)
            else:  # Linux
                subprocess.call(('xdg-open', file_path))
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"No se pudo abrir el archivo:\n{str(e)}"
            )
    
    def _ensure_proper_display(self):
        """
        Asegura que los elementos de la interfaz se muestren correctamente.
        Se llama después de completar operaciones importantes.
        """
        # Forzar actualización de la interfaz
        self.root.update_idletasks()
        
        # Asegurar que todos los widgets tienen los colores correctos
        self.root.configure(background=self.bg_color)
        
        # Recorrer todos los frames y asegurar que mantienen el color correcto
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                self.style.configure("TFrame", background=self.bg_color)
            elif isinstance(widget, ttk.LabelFrame):
                self.style.configure("TLabelframe", background=self.bg_color)
                self.style.configure("TLabelframe.Label", background=self.bg_color)


def main():
    """Función principal para iniciar la aplicación."""
    # Verificar compatibilidad antes de iniciar
    check_system_compatibility()
    
    # Crear la ventana principal
    root = tk.Tk()
    
    # Configuración básica de la ventana
    root.title("Generador de Etiquetas")
    root.geometry("600x450")
    
    try:
        # Intentar establecer un icono si existe
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
        if os.path.exists(icon_path):
            img = tk.PhotoImage(file=icon_path)
            root.iconphoto(True, img)
    except Exception:
        # Ignorar errores si no se puede cargar el icono
        pass
    
    # Configurar tema para evitar problemas de visualización
    style = ttk.Style()
    
    # Seleccionar un tema confiable que funcione en todos los sistemas
    available_themes = style.theme_names()
    
    # Preferir temas nativos si están disponibles
    if platform.system() == "Darwin" and 'aqua' in available_themes:
        style.theme_use('aqua')
    elif platform.system() == "Windows" and 'vista' in available_themes:
        style.theme_use('vista')
    elif 'clam' in available_themes:
        style.theme_use('clam')  # Un tema que funciona bien en todos los sistemas
    
    # Colores base
    bg_color = '#f5f5f5'  # Un gris muy claro para el fondo
    
    # Configurar colores de fondo y primer plano para toda la aplicación
    root.configure(background=bg_color)
    
    # Configuración específica para ttk widgets
    style.configure('.', background=bg_color)
    style.configure("TFrame", background=bg_color)
    style.configure("TLabel", background=bg_color)
    style.configure("TLabelframe", background=bg_color)
    style.configure("TLabelframe.Label", background=bg_color)
    
    # Evitar que los widgets ttk hereden el color de fondo del tema
    style.map('TButton', background=[('active', bg_color)])
    style.map('TCheckbutton', background=[('active', bg_color)])
    
    # Inicializar la aplicación
    app = EtiquetaGeneratorGUI(root)
    
    # Centrar la ventana en la pantalla
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Iniciar el bucle principal
    root.mainloop()


if __name__ == "__main__":
    main()
