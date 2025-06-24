"""
Punto de entrada principal para el generador de etiquetas.
"""
import os
import platform

# Silenciar advertencia de depreciación de Tk
os.environ['TK_SILENCE_DEPRECATION'] = '1'

from gui import main

if __name__ == "__main__":
    main()
