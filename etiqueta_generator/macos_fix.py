#!/usr/bin/env python3
"""
Script de corrección específico para macOS con soluciones avanzadas para problemas de tema oscuro.
Este script aplica múltiples técnicas para garantizar que la interfaz Tkinter se muestre correctamente.
"""
import os
import sys
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog

# Verificar que estamos en macOS
if platform.system() != "Darwin":
    print("Este script es específico para macOS. En otros sistemas use run_app.py")
    sys.exit(1)

# Configuraciones críticas para macOS
os.environ['TK_SILENCE_DEPRECATION'] = '1'
os.environ['NSRequiresAquaSystemAppearance'] = 'YES'  # Forzar modo claro para la app
os.environ['PYTHONCOERCECLOCALE'] = '0'
os.environ['LANG'] = 'en_US.UTF-8'
os.environ['SYSTEM_VERSION_COMPAT'] = '1'

# Verificar si estamos en modo oscuro
is_dark_mode = os.system('defaults read -g AppleInterfaceStyle 2>/dev/null') == 0
if is_dark_mode:
    print("Detectado modo oscuro en macOS. Aplicando correcciones...")

# Directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Importar después de configurar variables de entorno
from etiquetas import EtiquetaGenerator

class FixedMacOSApp:
    def __init__(self, root):
        # Configuración básica de la ventana
        self.root = root
        self.root.title("Generador de Etiquetas (macOS)")
        self.root.geometry("600x450")
        
        # Forzar colores claros de forma explícita
        self.bg_color = '#ffffff'  # Blanco puro
        self.fg_color = '#000000'  # Negro puro
        self.accent_color = '#0078d7'  # Azul claro
        self.button_bg = '#e1e1e1'  # Gris claro
        
        # Aplicar colores a la ventana raíz
        self.root.configure(bg=self.bg_color)
        
        # Generador de etiquetas
        self.etiqueta_generator = EtiquetaGenerator()
        
        # Variables
        self.excel_path = tk.StringVar()
        self.use_stock = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="Esperando selección de archivo Excel...")
        self.preview_pdf_path = None
        self.final_pdf_path = None
        
        # Crear la interfaz
        self.create_widgets()
    
    def create_widgets(self):
        """Crear los widgets de la interfaz con configuración de color explícita."""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="Generador de Etiquetas para Ropa",
            font=("Helvetica", 16, "bold"),
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
        
        # Contenedor para archivo
        file_container = tk.Frame(file_frame, bg=self.bg_color)
        file_container.pack(fill=tk.X)
        
        # Campo para ruta del archivo
        excel_entry = tk.Entry(
            file_container,
            textvariable=self.excel_path,
            width=50,
            bg='white',
            fg='black'
        )
        excel_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        # Botón para seleccionar archivo
        browse_button = tk.Button(
            file_container,
            text="Examinar",
            command=self.browse_excel,
            bg=self.button_bg,
            fg=self.fg_color,
            relief=tk.RAISED,
            bd=2
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
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Checkbox para usar stock
        stock_check = tk.Checkbutton(
            options_frame,
            text="Usar valores de stock del Excel (columna 'Stock')",
            variable=self.use_stock,
            bg=self.bg_color,
            fg=self.fg_color,
            activebackground=self.bg_color,
            selectcolor=self.bg_color
        )
        stock_check.pack(anchor=tk.W)
        
        # Botón para ver vista previa
        preview_button = tk.Button(
            main_frame,
            text="Generar Vista Previa",
            command=self.generate_preview,
            bg=self.button_bg,
            fg=self.fg_color,
            relief=tk.RAISED,
            bd=2
        )
        preview_button.pack(fill=tk.X, pady=(0, 10))
        
        # Botón para generar etiquetas
        generate_button = tk.Button(
            main_frame,
            text="Generar Etiquetas",
            command=self.generate_labels,
            bg=self.accent_color,
            fg='white',
            relief=tk.RAISED,
            bd=2
        )
        generate_button.pack(fill=tk.X, pady=(0, 10))
        
        # Barra de estado
        status_frame = tk.Frame(main_frame, bg=self.bg_color, relief=tk.SUNKEN, bd=1)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            bg=self.bg_color,
            fg=self.fg_color,
            anchor=tk.W
        )
        status_label.pack(fill=tk.X, padx=5, pady=2)
    
    def browse_excel(self):
        """Abre un diálogo para seleccionar un archivo Excel."""
        file_path = tk.filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx *.xls")]
        )
        
        if file_path:
            self.excel_path.set(file_path)
            self.status_var.set(f"Archivo seleccionado: {os.path.basename(file_path)}")
    
    def generate_preview(self):
        """Genera una vista previa de las etiquetas."""
        if not self.excel_path.get():
            tk.messagebox.showerror("Error", "Por favor, seleccione un archivo Excel primero.")
            return
        
        self.status_var.set("Generando vista previa...")
        self.root.update()
        
        try:
            # Generar vista previa (solo primera página)
            self.preview_pdf_path = self.etiqueta_generator.generate_labels(
                self.excel_path.get(),
                use_stock=self.use_stock.get(),
                is_preview=True
            )
            
            self.status_var.set("Vista previa generada correctamente.")
            
            # Abrir el archivo PDF
            self.open_pdf(self.preview_pdf_path)
            
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error al generar vista previa: {str(e)}")
            self.status_var.set("Error al generar vista previa.")
    
    def generate_labels(self):
        """Genera todas las etiquetas y guarda el PDF final."""
        if not self.excel_path.get():
            tk.messagebox.showerror("Error", "Por favor, seleccione un archivo Excel primero.")
            return
        
        self.status_var.set("Generando etiquetas...")
        self.root.update()
        
        try:
            # Generar etiquetas completas
            self.final_pdf_path = self.etiqueta_generator.generate_labels(
                self.excel_path.get(),
                use_stock=self.use_stock.get(),
                is_preview=False
            )
            
            self.status_var.set("Etiquetas generadas correctamente.")
            
            # Preguntar si quiere abrir el PDF
            if tk.messagebox.askyesno("Éxito", f"Etiquetas generadas en: {self.final_pdf_path}\n\n¿Desea abrir el archivo?"):
                self.open_pdf(self.final_pdf_path)
            
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error al generar etiquetas: {str(e)}")
            self.status_var.set("Error al generar etiquetas.")
    
    def open_pdf(self, pdf_path):
        """Abre un archivo PDF con el visor predeterminado del sistema."""
        if platform.system() == "Darwin":  # macOS
            subprocess.run(["open", pdf_path])
        elif platform.system() == "Windows":
            os.startfile(pdf_path)
        else:  # Linux
            subprocess.run(["xdg-open", pdf_path])

def main():
    """Función principal para iniciar la aplicación."""
    # Crear la ventana principal con colores claros forzados
    root = tk.Tk()
    
    # Ajustes críticos para macOS
    if platform.system() == "Darwin":
        root.tk.call('::tk::unsupported::MacWindowStyle', 'style', root._w, 'document', 'none')
        
        # Intentar forzar tema claro desde Tk
        try:
            root.tk.call('tk_setPalette', 'background', '#FFFFFF', 'foreground', '#000000')
        except:
            pass
    
    # Iniciar la aplicación
    app = FixedMacOSApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
