#!/usr/bin/env python3
"""
Script alternativo para macOS que evita los problemas de visualización.
Este script se basa en la solución de la comunidad para problemas
específicos con Tkinter en macOS.
"""
import os
import sys
import platform

# Verificar que estamos en macOS
if platform.system() != "Darwin":
    print("Este script está optimizado para macOS. En otros sistemas use run_app.py o emergency_app.py")
    sys.exit(1)

# Silenciar advertencia de depreciación de Tk
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# Forzar modo claro para la aplicación
os.environ['NSRequiresAquaSystemAppearance'] = 'YES'

# Configuraciones específicas para macOS
os.environ['PYTHONCOERCECLOCALE'] = '0'
os.environ['LANG'] = 'en_US.UTF-8'

# Agregar el directorio actual al path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Importaciones
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import subprocess
from etiquetas import EtiquetaGenerator

class MacOSApp:
    def __init__(self, root):
        # Configuración básica de la ventana
        self.root = root
        self.root.title("Generador de Etiquetas para macOS")
        self.root.geometry("600x400")
        
        # Obtener el color de fondo correcto para macOS
        self.bg_color = self.root.cget("background")
        
        # Generador de etiquetas
        self.etiqueta_generator = EtiquetaGenerator()
        
        # Variables
        self.excel_path = tk.StringVar()
        self.use_stock = tk.IntVar(value=1)  # IntVar es más confiable en macOS
        
        # Crear la interfaz
        self.setup_ui()
    
    def setup_ui(self):
        """
        Configura la interfaz de usuario con widgets nativos de macOS
        para evitar problemas de visualización.
        """
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="Generador de Etiquetas para Ropa",
            font=("Helvetica", 18, "bold")
        )
        title_label.pack()
        
        # Instrucciones
        instructions = tk.Label(
            header_frame,
            text="Seleccione un archivo Excel y configure las opciones",
            font=("Helvetica", 12)
        )
        instructions.pack(pady=(5, 0))
        
        # Frame para selección de archivo
        file_frame = tk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        file_label = tk.Label(file_frame, text="Archivo Excel:", width=12, anchor='e')
        file_label.pack(side=tk.LEFT)
        
        excel_entry = tk.Entry(file_frame, textvariable=self.excel_path, width=40)
        excel_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        browse_button = tk.Button(file_frame, text="Examinar...", command=self.browse_excel)
        browse_button.pack(side=tk.RIGHT)
        
        # Frame para opciones
        options_frame = tk.LabelFrame(main_frame, text="Opciones", padx=10, pady=10)
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        stock_check = tk.Checkbutton(
            options_frame,
            text="Usar el stock del Excel para generar cantidad de etiquetas",
            variable=self.use_stock
        )
        stock_check.pack(anchor=tk.W)
        
        help_text = tk.Label(
            options_frame,
            text="Si activa esta opción, se generará una etiqueta por cada unidad en stock.\nTodas las unidades del mismo producto tendrán el mismo código de barras.",
            justify=tk.LEFT,
            font=("Helvetica", 10),
            fg="gray50"
        )
        help_text.pack(anchor=tk.W, pady=(5, 0))
        
        # Frame para botones
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=15)
        
        preview_button = tk.Button(
            button_frame,
            text="Previsualizar",
            width=15,
            command=self.preview_labels
        )
        preview_button.pack(side=tk.LEFT, padx=(0, 10))
        
        generate_button = tk.Button(
            button_frame,
            text="Generar Etiquetas",
            width=15,
            command=self.generate_labels
        )
        generate_button.pack(side=tk.LEFT)
        
        # Barra de estado
        self.status_var = tk.StringVar(value="Listo para comenzar. Seleccione un archivo Excel.")
        status_bar = tk.Label(
            main_frame,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padx=5,
            pady=5
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def browse_excel(self):
        """Abre un diálogo para seleccionar un archivo Excel."""
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
        
        self.status_var.set("Generando previsualización...")
        threading.Thread(target=self._do_preview).start()
    
    def _do_preview(self):
        """Ejecuta la previsualización en un hilo separado."""
        try:
            # Cargar el Excel
            success = self.etiqueta_generator.load_excel(self.excel_path.get())
            if success:
                # Generar previsualización
                pdf_path = self.etiqueta_generator.generate_labels(preview=True)
                
                # Actualizar interfaz en hilo principal
                if pdf_path:
                    self.root.after(0, lambda: self.status_var.set("Previsualización generada correctamente."))
                    self.root.after(0, lambda: self._ask_open_pdf(pdf_path))
                else:
                    self.root.after(0, lambda: self.status_var.set("Error al generar la previsualización."))
                    self.root.after(0, lambda: messagebox.showerror("Error", "No se pudo generar la previsualización."))
            else:
                self.root.after(0, lambda: self.status_var.set("Error al cargar el archivo Excel."))
                self.root.after(0, lambda: messagebox.showerror("Error", "El archivo Excel no tiene las columnas requeridas."))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error al procesar: {str(e)}"))
    
    def generate_labels(self):
        """Genera todas las etiquetas."""
        if not self.excel_path.get():
            messagebox.showwarning("Advertencia", "Debe seleccionar un archivo Excel primero.")
            return
        
        self.status_var.set("Generando etiquetas...")
        threading.Thread(target=self._do_generate).start()
    
    def _do_generate(self):
        """Ejecuta la generación de etiquetas en un hilo separado."""
        try:
            # Cargar el Excel
            success = self.etiqueta_generator.load_excel(self.excel_path.get())
            if success:
                # Generar etiquetas usando la opción seleccionada
                use_stock = bool(self.use_stock.get())
                pdf_path = self.etiqueta_generator.generate_labels(use_stock=use_stock)
                
                # Actualizar interfaz en hilo principal
                if pdf_path:
                    self.root.after(0, lambda: self.status_var.set("Etiquetas generadas correctamente."))
                    self.root.after(0, lambda: self._ask_open_pdf(pdf_path))
                else:
                    self.root.after(0, lambda: self.status_var.set("Error al generar las etiquetas."))
                    self.root.after(0, lambda: messagebox.showerror("Error", "No se pudo generar el PDF de etiquetas."))
            else:
                self.root.after(0, lambda: self.status_var.set("Error al cargar el archivo Excel."))
                self.root.after(0, lambda: messagebox.showerror("Error", "El archivo Excel no tiene las columnas requeridas."))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error al procesar: {str(e)}"))
    
    def _ask_open_pdf(self, pdf_path):
        """Pregunta si desea abrir el PDF generado."""
        if messagebox.askyesno("PDF Generado", f"¿Desea abrir el PDF generado?\n{pdf_path}"):
            self._open_file(pdf_path)
    
    def _open_file(self, file_path):
        """Abre un archivo con la aplicación predeterminada del sistema."""
        try:
            subprocess.call(('open', file_path))  # Comando específico para macOS
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {str(e)}")

def main():
    """Función principal para iniciar la aplicación."""
    # Crear y configurar la ventana raíz
    root = tk.Tk()
    
    # Verificar versión de Python y Tk antes de continuar
    print(f"Python versión: {platform.python_version()}")
    print(f"Tkinter versión: {tk.TkVersion}")
    
    # Iniciar la aplicación
    app = MacOSApp(root)
    
    # Centrar la ventana en la pantalla
    root.eval('tk::PlaceWindow . center')
    
    # Iniciar bucle principal de eventos
    root.mainloop()

if __name__ == "__main__":
    main()
