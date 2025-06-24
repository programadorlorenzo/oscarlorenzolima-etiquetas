#!/usr/bin/env python3
"""
Script que utiliza otra técnica para crear interfaces en macOS.
Este script importa Python para macOS (PyObjC) si está disponible
y usa una aproximación alternativa para crear interfaces en macOS.
"""
import os
import sys
import platform
import subprocess

# Verificar que estamos en macOS
if platform.system() != "Darwin":
    print("Este script solo funciona en macOS.")
    sys.exit(1)

print("Verificando paquetes necesarios para macOS...")

# Intentar instalar PyObjC si no está presente
try:
    import objc
    import AppKit
    import Cocoa
    print("PyObjC está instalado. Continuando...")
except ImportError:
    print("PyObjC no está instalado. Intentando instalarlo...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyobjc"])
        print("PyObjC instalado correctamente.")
        # Intentar importar de nuevo
        try:
            import objc
            import AppKit
            import Cocoa
            print("PyObjC importado correctamente.")
        except ImportError:
            print("No se pudo importar PyObjC después de instalarlo. Continuando con alternativa...")
    except:
        print("No se pudo instalar PyObjC. Continuando con alternativa...")

# Establecer variables de entorno para macOS
os.environ['NSRequiresAquaSystemAppearance'] = 'YES'
os.environ['TK_SILENCE_DEPRECATION'] = '1'
os.environ['PYTHONCOERCECLOCALE'] = '0'
os.environ['LANG'] = 'en_US.UTF-8'

# Directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Importar el generador de etiquetas
sys.path.append(current_dir)
from etiquetas import EtiquetaGenerator

# Función para verificar si podemos usar interfaces nativas de macOS
def can_use_native_macos_ui():
    try:
        import objc
        import AppKit
        return True
    except ImportError:
        return False

# Definir una clase para la aplicación nativa de macOS si es posible
if can_use_native_macos_ui():
    import tkinter as tk
    from tkinter import filedialog, messagebox
    import AppKit
    
    class CocoaBasedApp:
        def __init__(self):
            # Configurar para usar tema claro
            AppKit.NSApp.appearance = AppKit.NSAppearance.appearanceNamed_(
                AppKit.NSAppearanceNameAqua
            )
            
            # Crear ventana Tkinter
            self.root = tk.Tk()
            self.root.withdraw()  # Ocultar ventana principal
            
            # Preguntar por archivo Excel
            file_path = filedialog.askopenfilename(
                title="Seleccionar archivo Excel",
                filetypes=[("Archivos Excel", "*.xlsx *.xls")]
            )
            
            if not file_path:
                messagebox.showerror("Error", "No se seleccionó ningún archivo")
                return
            
            # Preguntar si usar stock
            use_stock = messagebox.askyesno(
                "Configuración", 
                "¿Desea generar una etiqueta por cada unidad en stock?\n\n"
                "- Sí: Se usará la columna 'Stock' del Excel\n"
                "- No: Podrá especificar cantidades manualmente"
            )
            
            # Generar etiquetas
            generator = EtiquetaGenerator()
            
            try:
                # Generar vista previa
                preview = messagebox.askyesno(
                    "Vista previa", 
                    "¿Desea generar una vista previa antes de crear todas las etiquetas?"
                )
                
                if preview:
                    pdf_path = generator.generate_labels(file_path, use_stock=use_stock, is_preview=True)
                    
                    # Abrir PDF
                    if messagebox.askyesno("Vista previa generada", "¿Abrir la vista previa?"):
                        subprocess.run(["open", pdf_path])
                
                # Generar etiquetas finales
                if messagebox.askyesno("Generar etiquetas", "¿Generar todas las etiquetas ahora?"):
                    pdf_path = generator.generate_labels(file_path, use_stock=use_stock, is_preview=False)
                    messagebox.showinfo("Éxito", f"Etiquetas generadas en:\n{pdf_path}")
                    
                    # Abrir PDF
                    if messagebox.askyesno("Etiquetas generadas", "¿Abrir el archivo PDF?"):
                        subprocess.run(["open", pdf_path])
            
            except Exception as e:
                messagebox.showerror("Error", f"Error al generar etiquetas: {str(e)}")
    
    # Ejecutar aplicación nativa
    app = CocoaBasedApp()

else:
    # Si no podemos usar interfaces nativas, usar la versión normal
    print("No se puede usar la interfaz nativa de macOS. Ejecutando versión alternativa...")
    macos_fix_path = os.path.join(current_dir, "macos_fix.py")
    subprocess.run([sys.executable, macos_fix_path])
