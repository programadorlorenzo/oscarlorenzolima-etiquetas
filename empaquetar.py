#!/usr/bin/env python3
"""
Script para empaquetar la aplicación de etiquetas usando PyInstaller.
Este script creará un ejecutable que incluirá todos los recursos necesarios.
"""
import os
import sys
import PyInstaller.__main__
import shutil
from datetime import datetime

# Obtener el directorio raíz del proyecto
root_dir = os.path.dirname(os.path.abspath(__file__))

# Definir las carpetas de recursos que necesitamos incluir
assets_dir = os.path.join(root_dir, 'assets')
data_dir = os.path.join(root_dir, 'data')
output_dir = os.path.join(root_dir, 'output')

# Crear carpeta dist si no existe
dist_folder = os.path.join(root_dir, 'dist')
if not os.path.exists(dist_folder):
    os.makedirs(dist_folder)

# Configurar nombre del ejecutable con fecha
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
app_name = f"Generador_Etiquetas_{timestamp}"

# Parámetros para PyInstaller
pyinstaller_args = [
    '--name=%s' % app_name,
    '--onedir',  # Crea una carpeta con el ejecutable y las dependencias
    '--windowed',  # Sin consola en Windows
    '--add-data=%s:assets' % os.path.join(assets_dir, '*'),  # Incluir carpeta de assets
    '--add-data=%s:data' % os.path.join(data_dir, '*'),  # Incluir carpeta de datos
    '--hidden-import=PIL._tkinter_finder',  # Importación oculta necesaria para PIL
    '--icon=%s' % os.path.join(assets_dir, 'logo.png'),  # Icono de la aplicación
    os.path.join(root_dir, 'gui_pyqt5.py'),  # Script principal
]

# Ejecutar PyInstaller
print("Empaquetando aplicación...")
PyInstaller.__main__.run(pyinstaller_args)

# Crear carpeta output en el paquete distribuible si no existe
dist_output_dir = os.path.join(dist_folder, app_name, 'output')
if not os.path.exists(dist_output_dir):
    os.makedirs(dist_output_dir)

print(f"Aplicación empaquetada exitosamente en: {os.path.join(dist_folder, app_name)}")
print(f"Ejecuta la aplicación con: {os.path.join(dist_folder, app_name, app_name)}")
