#!/usr/bin/env python3
"""
Abre el archivo PDF generado.
"""
import os
import platform
import sys

def main():
    """Función principal."""
    pdf_file = "etiqueta_jean.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"Error: El archivo {pdf_file} no existe.")
        return
    
    try:
        if platform.system() == 'Darwin':  # macOS
            os.system(f'open "{pdf_file}"')
        elif platform.system() == 'Windows':  # Windows
            os.system(f'start "" "{pdf_file}"')
        else:  # Linux
            os.system(f'xdg-open "{pdf_file}"')
            
        print(f"Abriendo {pdf_file}...")
    except Exception as e:
        print(f"No se pudo abrir el archivo: {e}")

if __name__ == "__main__":
    main()
