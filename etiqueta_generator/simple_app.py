#!/usr/bin/env python3
"""
Script ultra simple para resolver el problema específico del filedialog.
Esta versión no hace nada especial, solo se asegura de importar correctamente
los módulos necesarios para Tkinter.
"""
import os
import sys
import platform
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

# Configuraciones básicas para macOS
os.environ['TK_SILENCE_DEPRECATION'] = '1'
os.environ['NSRequiresAquaSystemAppearance'] = 'YES'

# Directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Importar el generador de etiquetas
from etiquetas import EtiquetaGenerator

class SimpleApp:
    def __init__(self, root):
        # Configuración básica
        self.root = root
        self.root.title("Generador de Etiquetas - Versión Simple")
        self.root.geometry("600x400")
        
        # Usar colores muy básicos
        self.root.configure(bg='white')
        
        # Generador de etiquetas
        self.etiqueta_generator = EtiquetaGenerator()
        
        # Variables
        self.excel_path = tk.StringVar()
        self.use_stock = tk.BooleanVar(value=True)
        
        # Crear interfaz
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title = tk.Label(
            main_frame, 
            text="Generador de Etiquetas",
            font=("Arial", 16, "bold"),
            bg='white',
            fg='black'
        )
        title.pack(pady=10)
        
        # Frame para archivo
        file_frame = tk.LabelFrame(
            main_frame,
            text="Seleccionar Excel",
            bg='white',
            fg='black'
        )
        file_frame.pack(fill=tk.X, pady=10, padx=5)
        
        # Entrada y botón
        file_entry = tk.Entry(
            file_frame,
            textvariable=self.excel_path,
            width=50,
            bg='white',
            fg='black'
        )
        file_entry.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(
            file_frame,
            text="Examinar",
            command=self.browse_file,
            bg='lightgray',
            fg='black'
        )
        browse_btn.pack(side=tk.RIGHT, padx=5, pady=10)
        
        # Opción de stock
        stock_check = tk.Checkbutton(
            main_frame,
            text="Usar valores de stock del Excel",
            variable=self.use_stock,
            bg='white',
            fg='black',
            selectcolor='white'
        )
        stock_check.pack(anchor=tk.W, padx=5, pady=5)
        
        # Botones
        preview_btn = tk.Button(
            main_frame,
            text="Vista Previa",
            command=self.generate_preview,
            bg='lightgray',
            fg='black'
        )
        preview_btn.pack(fill=tk.X, pady=5, padx=5)
        
        generate_btn = tk.Button(
            main_frame,
            text="Generar Etiquetas",
            command=self.generate_labels,
            bg='blue',
            fg='white'
        )
        generate_btn.pack(fill=tk.X, pady=5, padx=5)
    
    def browse_file(self):
        file_types = [("Archivos Excel", "*.xlsx *.xls")]
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=file_types
        )
        
        if file_path:
            self.excel_path.set(file_path)
    
    def generate_preview(self):
        if not self.excel_path.get():
            messagebox.showerror("Error", "Por favor seleccione un archivo Excel primero")
            return
        
        try:
            # Cargar el Excel
            if not self.etiqueta_generator.load_excel(self.excel_path.get()):
                messagebox.showerror("Error", "El archivo Excel no tiene el formato correcto")
                return
            
            # Generar vista previa
            pdf_path = self.etiqueta_generator.generate_labels(
                preview=True,
                use_stock=self.use_stock.get()
            )
            
            if pdf_path:
                if messagebox.askyesno("Éxito", "Vista previa generada. ¿Desea abrirla?"):
                    self.open_pdf(pdf_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar vista previa: {str(e)}")
    
    def generate_labels(self):
        if not self.excel_path.get():
            messagebox.showerror("Error", "Por favor seleccione un archivo Excel primero")
            return
        
        try:
            # Cargar el Excel
            if not self.etiqueta_generator.load_excel(self.excel_path.get()):
                messagebox.showerror("Error", "El archivo Excel no tiene el formato correcto")
                return
            
            # Generar etiquetas completas
            pdf_path = self.etiqueta_generator.generate_labels(
                preview=False,
                use_stock=self.use_stock.get()
            )
            
            if pdf_path:
                messagebox.showinfo("Éxito", f"Etiquetas generadas en: {pdf_path}")
                if messagebox.askyesno("Éxito", "¿Desea abrir el archivo PDF?"):
                    self.open_pdf(pdf_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar etiquetas: {str(e)}")
    
    def open_pdf(self, pdf_path):
        try:
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["open", pdf_path])
            elif platform.system() == "Windows":
                os.startfile(pdf_path)
            else:  # Linux
                subprocess.run(["xdg-open", pdf_path])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el PDF: {str(e)}")

def main():
    # Crear ventana principal
    root = tk.Tk()
    
    # Para macOS, forzar estilo claro
    if platform.system() == "Darwin":
        # Intentar configuraciones adicionales para macOS
        try:
            root.tk.call('::tk::unsupported::MacWindowStyle', 'style', root._w, 'document', 'none')
        except:
            pass
    
    # Iniciar la aplicación
    app = SimpleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
