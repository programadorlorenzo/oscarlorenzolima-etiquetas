#!/usr/bin/env python3
"""
Ejecuta la interfaz gráfica del generador de etiquetas.
"""

import tkinter as tk
from gui_manager import EtiquetasApp
import os
import sys

def main():
    """Función principal."""
    # Asegurarse de que estamos en el directorio correcto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Crear ventana principal
    root = tk.Tk()
    
    # Inicializar la aplicación
    app = EtiquetasApp(root)
    
    # Ejecutar el bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()