#!/usr/bin/env python3
"""
Script extremadamente simple y robusto para ejecutar la aplicación en macOS.
Este script usa la técnica más básica posible para ejecutar Tkinter en macOS.
"""
import os
import sys
import platform
import subprocess

# Verificar que estamos en macOS
if platform.system() != "Darwin":
    print("Este script es específico para macOS.")
    print("En otros sistemas use: python main.py")
    sys.exit(1)

# Directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Configurar variables de entorno críticas
print("Configurando entorno para macOS...")
os.environ['TK_SILENCE_DEPRECATION'] = '1'
os.environ['NSRequiresAquaSystemAppearance'] = 'YES'
os.environ['PYTHONCOERCECLOCALE'] = '0'
os.environ['LANG'] = 'en_US.UTF-8'
os.environ['SYSTEM_VERSION_COMPAT'] = '1'

# Ejecutar el script en un nuevo proceso para asegurar que las variables
# de entorno se apliquen correctamente
python_path = sys.executable
macos_fix_path = os.path.join(current_dir, "macos_fix.py")

print(f"Ejecutando script optimizado para macOS desde: {macos_fix_path}")
subprocess.run([python_path, macos_fix_path])
