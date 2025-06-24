#!/usr/bin/env python3
"""
Script para instalar las dependencias necesarias para el generador de etiquetas simple.
"""
import subprocess
import sys

def install_dependencies():
    """Instala las dependencias necesarias."""
    dependencies = [
        'python-barcode',
        'reportlab',
        'pillow'
    ]
    
    print("Instalando dependencias necesarias...")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + dependencies)
        print("\n¡Instalación completada con éxito!")
        print("Ahora puede ejecutar el generador de etiquetas simple usando:")
        print("python simple_label_generator.py")
    except Exception as e:
        print(f"\nError al instalar dependencias: {e}")
        print("\nIntente instalarlas manualmente con:")
        print("pip install python-barcode reportlab pillow")

if __name__ == "__main__":
    install_dependencies()
