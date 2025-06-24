#!/usr/bin/env python3
"""
Script alternativo para ejecutar el generador de etiquetas con un enfoque básico.
Este script utiliza Tkinter directamente con configuración mínima para evitar
problemas de visualización, especialmente en macOS con Dark Mode.
"""
import os
import sys
import platform

# Silenciar advertencia de depreciación de Tk
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# Forzar modo claro para la aplicación
os.environ['SYSTEM_VERSION_COMPAT'] = '1'
os.environ['NSRequiresAquaSystemAppearance'] = 'Yes'

# Configuraciones adicionales para macOS
if platform.system() == "Darwin":
    # Comprobar si estamos en Dark Mode
    is_dark_mode = os.system('defaults read -g AppleInterfaceStyle 2>/dev/null') == 0
    if is_dark_mode:
        print("Detectado modo oscuro en macOS. Forzando modo claro para la aplicación...")
    
    # Forzar modo ligero para esta aplicación específica
    os.environ['PYTHONCOERCECLOCALE'] = '0'
    
    # Desactivar características que pueden causar problemas
    os.environ['PYOBJC_DISABLE_AUTO_THEME'] = '1'

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Crear la aplicación desde cero sin usar gui.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from etiquetas import EtiquetaGenerator
import threading

class SimpleEtiquetaApp:
    """Versión simplificada de la aplicación para evitar problemas de visualización."""
    
    def __init__(self, root):
        """Inicializar la aplicación con configuración mínima."""
        self.root = root
        self.root.title("Generador de Etiquetas")
        self.root.geometry("600x450")
        
        # Forzar colores en modo claro
        self.bg_color = 'white'
        self.fg_color = 'black'
        self.button_bg = 'lightgray'
        
        # Configurar la ventana con colores fijos
        self.root.configure(bg=self.bg_color)
        
        # Generador de etiquetas
        self.etiqueta_generator = EtiquetaGenerator()
        
        # Variables
        self.excel_path = tk.StringVar()
        self.use_stock = tk.BooleanVar(value=True)
        
        # Crear la interfaz
        self.create_widgets()
    
    def create_widgets(self):
        """Crear los widgets de la interfaz con configuración mínima."""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="Generador de Etiquetas para Ropa",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para selección de archivo
        file_frame = tk.LabelFrame(
            main_frame,
            text="Selección de Archivo Excel",
            bg=self.bg_color,
            fg=self.fg_color,
            padx=10,
            pady=10
        )
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campo para ruta del archivo
        excel_entry = tk.Entry(
            file_frame,
            textvariable=self.excel_path,
            width=50,
            bg='white',
            fg='black'
        )
        excel_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        # Botón para buscar archivo
        browse_button = tk.Button(
            file_frame,
            text="Buscar",
            command=self.browse_excel,
            bg=self.button_bg
        )
        browse_button.pack(side=tk.RIGHT)
        
        # Frame para opciones
        options_frame = tk.LabelFrame(
            main_frame,
            text="Opciones de Generación",
            bg=self.bg_color,
            fg=self.fg_color,
            padx=10,
            pady=10
        )
        options_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Checkbox para usar el stock
        stock_check = tk.Checkbutton(
            options_frame,
            text="Usar el stock del Excel para generar etiquetas",
            variable=self.use_stock,
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor='white'
        )
        stock_check.pack(anchor=tk.W, pady=(5, 0))
        
        # Mensaje informativo
        info_label = tk.Label(
            options_frame,
            text="Seleccione un archivo Excel y luego genere las etiquetas.",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color
        )
        info_label.pack(pady=20)
        
        # Frame para botones de acción
        buttons_frame = tk.Frame(main_frame, bg=self.bg_color)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botón para previsualizar
        preview_button = tk.Button(
            buttons_frame,
            text="Previsualizar Etiqueta",
            command=self.preview_labels,
            bg=self.button_bg
        )
        preview_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón para generar todas las etiquetas
        generate_button = tk.Button(
            buttons_frame,
            text="Generar Etiquetas",
            command=self.generate_labels,
            bg=self.button_bg
        )
        generate_button.pack(side=tk.LEFT)
        
        # Etiqueta de estado
        self.status_var = tk.StringVar(value="Esperando selección de archivo Excel...")
        status_label = tk.Label(
            main_frame,
            textvariable=self.status_var,
            bg=self.bg_color,
            fg=self.fg_color,
            anchor=tk.W
        )
        status_label.pack(fill=tk.X, pady=(10, 0))
    
    def browse_excel(self):
        """Abrir diálogo para seleccionar un archivo Excel."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar Archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx *.xls")]
        )
        
        if file_path:
            self.excel_path.set(file_path)
            self.status_var.set("Archivo seleccionado. Listo para generar etiquetas.")
    
    def preview_labels(self):
        """Genera una previsualización de las etiquetas."""
        if not self.excel_path.get():
            messagebox.showwarning("Advertencia", "Debe seleccionar un archivo Excel primero.")
            return
        
        self.status_var.set("Cargando archivo Excel...")
        threading.Thread(target=self._do_preview).start()
    
    def _do_preview(self):
        """Ejecuta la previsualización en un hilo separado."""
        try:
            # Cargar el Excel
            success = self.etiqueta_generator.load_excel(self.excel_path.get())
            if not success:
                self.root.after(0, lambda: self.status_var.set("Error al cargar el archivo Excel."))
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", 
                    "No se pudo cargar el archivo Excel o no contiene las columnas requeridas."
                ))
                return
            
            # Generar previsualización
            pdf_path = self.etiqueta_generator.generate_labels(preview=True)
            
            # Actualizar interfaz en hilo principal
            if pdf_path:
                self.root.after(0, lambda: self.status_var.set("Previsualización generada correctamente."))
                self.root.after(0, lambda: self._ask_open_pdf(pdf_path))
            else:
                self.root.after(0, lambda: self.status_var.set("Error al generar la previsualización."))
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", 
                    "No se pudo generar la previsualización."
                ))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
    
    def generate_labels(self):
        """Genera todas las etiquetas."""
        if not self.excel_path.get():
            messagebox.showwarning("Advertencia", "Debe seleccionar un archivo Excel primero.")
            return
        
        self.status_var.set("Cargando archivo Excel...")
        threading.Thread(target=self._do_generate).start()
    
    def _do_generate(self):
        """Ejecuta la generación en un hilo separado."""
        try:
            # Cargar el Excel
            success = self.etiqueta_generator.load_excel(self.excel_path.get())
            if not success:
                self.root.after(0, lambda: self.status_var.set("Error al cargar el archivo Excel."))
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", 
                    "No se pudo cargar el archivo Excel o no contiene las columnas requeridas."
                ))
                return
            
            # Generar etiquetas
            use_stock = self.use_stock.get()
            pdf_path = self.etiqueta_generator.generate_labels(use_stock=use_stock)
            
            # Actualizar interfaz en hilo principal
            if pdf_path:
                self.root.after(0, lambda: self.status_var.set("Etiquetas generadas correctamente."))
                self.root.after(0, lambda: self._ask_open_pdf(pdf_path))
            else:
                self.root.after(0, lambda: self.status_var.set("Error al generar las etiquetas."))
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", 
                    "No se pudo generar el PDF de etiquetas."
                ))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
    
    def _ask_open_pdf(self, pdf_path):
        """Pregunta si desea abrir el PDF generado."""
        if messagebox.askyesno(
            "PDF Generado",
            f"El PDF se ha generado correctamente en:\n{pdf_path}\n\n¿Desea abrirlo ahora?"
        ):
            self._open_file(pdf_path)
    
    def _open_file(self, file_path):
        """Abre un archivo con la aplicación predeterminada del sistema."""
        try:
            import subprocess
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

def main():
    """Función principal para iniciar la aplicación."""
    root = tk.Tk()
    app = SimpleEtiquetaApp(root)
    
    # Centrar la ventana en la pantalla
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Iniciar bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()
