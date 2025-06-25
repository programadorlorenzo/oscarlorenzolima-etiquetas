#!/usr/bin/env python3
"""
Script para convertir el logo.png en un archivo .ico para Windows
y un archivo .icns para macOS.
"""
import os
import sys
from PIL import Image

def png_to_ico(png_path, ico_path):
    """Convierte un archivo PNG a ICO para Windows."""
    try:
        img = Image.open(png_path)
        
        # Crear versiones de diferentes tamaños para el ícono
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(ico_path, sizes=sizes)
        print(f"Archivo ICO creado exitosamente: {ico_path}")
        return True
    except Exception as e:
        print(f"Error al crear el archivo ICO: {e}")
        return False

def png_to_icns_mac(png_path, icns_path):
    """
    Convierte un archivo PNG a ICNS para macOS.
    Requiere la herramienta iconutil de macOS.
    """
    try:
        # Crear directorio temporal para los iconsets
        iconset_dir = "logo.iconset"
        if not os.path.exists(iconset_dir):
            os.makedirs(iconset_dir)
        
        # Crear las versiones de diferentes tamaños
        sizes = [(16, 16), (32, 32), (64, 64), (128, 128), (256, 256), (512, 512), (1024, 1024)]
        img = Image.open(png_path)
        
        # Generar los archivos de ícono para cada tamaño
        for size in sizes:
            resized_img = img.resize(size, Image.Resampling.LANCZOS)
            resized_img.save(f"{iconset_dir}/icon_{size[0]}x{size[0]}.png")
            # Para las versiones @2x
            if size[0] <= 512:  # No necesitamos 2048x2048
                resized_img = img.resize((size[0]*2, size[0]*2), Image.Resampling.LANCZOS)
                resized_img.save(f"{iconset_dir}/icon_{size[0]}x{size[0]}@2x.png")
        
        # Usar iconutil para crear el archivo .icns
        os.system(f"iconutil -c icns {iconset_dir} -o {icns_path}")
        
        # Limpiar el directorio temporal
        for file in os.listdir(iconset_dir):
            os.remove(os.path.join(iconset_dir, file))
        os.rmdir(iconset_dir)
        
        print(f"Archivo ICNS creado exitosamente: {icns_path}")
        return True
    except Exception as e:
        print(f"Error al crear el archivo ICNS: {e}")
        return False

def main():
    """Función principal."""
    # Rutas de archivos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, "assets")
    png_path = os.path.join(assets_dir, "logo.png")
    
    # Verificar que el archivo PNG existe
    if not os.path.exists(png_path):
        print(f"Error: No se encontró el archivo {png_path}")
        sys.exit(1)
    
    # Crear ícono para Windows
    ico_path = os.path.join(assets_dir, "logo.ico")
    png_to_ico(png_path, ico_path)
    
    # Crear ícono para macOS
    icns_path = os.path.join(assets_dir, "logo.icns")
    if sys.platform == "darwin":  # Solo en macOS
        png_to_icns_mac(png_path, icns_path)
    else:
        print("La creación de archivos .icns solo es posible en macOS.")

if __name__ == "__main__":
    main()
