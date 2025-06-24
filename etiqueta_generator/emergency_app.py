#!/usr/bin/env python3
"""
Script de emergencia para ejecutar el generador de etiquetas con Tkinter básico.
Este script usa widgets Tk nativos (no ttk) con tema explícitamente claro
para evitar problemas con macOS Dark Mode.
"""
import os
import sys
import platform

# Silenciar advertencia de depreciación de Tk
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# Forzar modo claro para la aplicación
os.environ['NSRequiresAquaSystemAppearance'] = 'Yes'

# Agregar el directorio actual al path para importar módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Importar la aplicación después de configurar las variables de entorno
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import subprocess
from etiquetas import EtiquetaGenerator

class EmergencyApp:
    def __init__(self, root):
        # Configuración básica de la ventana
        self.root = root
        self.root.title("Generador de Etiquetas (Modo de Emergencia)")
        self.root.geometry("600x400")
        
        # Usar colores muy básicos que funcionan en todos los sistemas
        self.root.configure(bg='white')
        
        # Generador de etiquetas
        self.etiqueta_generator = EtiquetaGenerator()
        
        # Variables
        self.excel_path = tk.StringVar()
        self.use_stock = tk.BooleanVar(value=True)
        
        # Crear la interfaz
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="Generador de Etiquetas - Modo Básico",
            font=("Arial", 16, "bold"),
            bg='white',
            fg='black'
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para selección de archivo
        file_frame = tk.Frame(main_frame, bg='white')
        file_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(file_frame, text="Archivo Excel:", bg='white', fg='black').pack(side=tk.LEFT)
        
        excel_entry = tk.Entry(
            file_frame, 
            textvariable=self.excel_path, 
            width=40,
            bg='white',
            fg='black'
        )
        excel_entry.pack(side=tk.LEFT, padx=10)
        
        browse_button = tk.Button(
            file_frame, 
            text="Buscar", 
            command=self.browse_excel,
            bg='#e0e0e0',
            fg='black',
            relief=tk.RAISED,
            borderwidth=2
        )
        browse_button.pack(side=tk.LEFT)
        
        # Opción de usar stock
        stock_check = tk.Checkbutton(
            main_frame, 
            text="Usar el stock del Excel para generar cantidad de etiquetas",
            variable=self.use_stock,
            bg='white',
            fg='black',
            selectcolor='white'
        )
        stock_check.pack(anchor=tk.W, pady=10)
        
        # Frame para botones
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(pady=20)
        
        preview_button = tk.Button(
            button_frame, 
            text="Previsualizar Etiqueta", 
            command=self.preview_labels,
            bg='#e0e0e0',
            fg='black',
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            pady=5
        )
        preview_button.pack(side=tk.LEFT, padx=(0, 10))
        
        generate_button = tk.Button(
            button_frame, 
            text="Generar Etiquetas", 
            command=self.generate_labels,
            bg='#e0e0e0',
            fg='black',
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            pady=5
        )
        generate_button.pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar(value="Esperando selección de archivo...")
        status_label = tk.Label(
            main_frame, 
            textvariable=self.status_var, 
            bg='white',
            fg='black',
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_label.pack(fill=tk.X, side=tk.BOTTOM, pady=(20, 0))
    
    def browse_excel(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar Archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx *.xls")]
        )
        
        if file_path:
            self.excel_path.set(file_path)
            self.status_var.set("Archivo seleccionado. Listo para generar etiquetas.")
    
    def preview_labels(self):
        if not self.excel_path.get():
            messagebox.showwarning("Advertencia", "Debe seleccionar un archivo Excel primero.")
            return
        
        self.status_var.set("Generando previsualización...")
        threading.Thread(target=self._do_preview).start()
    
    def _do_preview(self):
        try:
            success = self.etiqueta_generator.load_excel(self.excel_path.get())
            if success:
                pdf_path = self.etiqueta_generator.generate_labels(preview=True)
                if pdf_path:
                    self.root.after(0, lambda: self.status_var.set("Previsualización generada."))
                    self.root.after(0, lambda: self._ask_open_pdf(pdf_path))
                else:
                    self.root.after(0, lambda: self.status_var.set("Error al generar la previsualización."))
            else:
                self.root.after(0, lambda: self.status_var.set("Error al cargar el archivo Excel."))
                self.root.after(0, lambda: messagebox.showerror("Error", "El archivo Excel no tiene las columnas requeridas."))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {e}"))
    
    def generate_labels(self):
        if not self.excel_path.get():
            messagebox.showwarning("Advertencia", "Debe seleccionar un archivo Excel primero.")
            return
        
        self.status_var.set("Generando etiquetas...")
        threading.Thread(target=self._do_generate).start()
    
    def _do_generate(self):
        try:
            success = self.etiqueta_generator.load_excel(self.excel_path.get())
            if success:
                use_stock = self.use_stock.get()
                pdf_path = self.etiqueta_generator.generate_labels(use_stock=use_stock)
                if pdf_path:
                    self.root.after(0, lambda: self.status_var.set("Etiquetas generadas correctamente."))
                    self.root.after(0, lambda: self._ask_open_pdf(pdf_path))
                else:
                    self.root.after(0, lambda: self.status_var.set("Error al generar las etiquetas."))
            else:
                self.root.after(0, lambda: self.status_var.set("Error al cargar el archivo Excel."))
                self.root.after(0, lambda: messagebox.showerror("Error", "El archivo Excel no tiene las columnas requeridas."))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {e}"))
    
    def _ask_open_pdf(self, pdf_path):
        if messagebox.askyesno("PDF Generado", f"¿Desea abrir el PDF generado?\n{pdf_path}"):
            self._open_file(pdf_path)
    
    def _open_file(self, file_path):
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', file_path))
            elif platform.system() == 'Windows':  # Windows
                os.startfile(file_path)
            else:  # Linux
                subprocess.call(('xdg-open', file_path))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

def main():
    # Crear y configurar la ventana
    root = tk.Tk()
    app = EmergencyApp(root)
    
    # Centrar la ventana
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Iniciar bucle de eventos
    root.mainloop()

if __name__ == "__main__":
    main()
