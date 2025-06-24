#!/usr/bin/env python3
"""
Script para instalar todas las dependencias necesarias para el generador de etiquetas.
Este script verificará e instalará las dependencias faltantes.
"""
import sys
import subprocess
import platform

def check_and_install(package, verbose=True):
    """Verifica si un paquete está instalado, y si no, lo instala."""
    if verbose:
        print(f"Verificando {package}...", end=" ", flush=True)
    
    try:
        __import__(package.split("==")[0])
        if verbose:
            print("✓ Instalado")
        return True
    except ImportError:
        if verbose:
            print(f"✗ No instalado. Instalando {package}...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            if verbose:
                print(f"✓ {package} instalado correctamente")
            return True
        except Exception as e:
            if verbose:
                print(f"✗ Error al instalar {package}: {e}")
            return False

def main():
    """Función principal para instalar dependencias."""
    print("=" * 80)
    print(" Instalador de Dependencias del Generador de Etiquetas ".center(80, "="))
    print("=" * 80)
    print(f"Sistema detectado: {platform.system()} {platform.release()}")
    print(f"Python: {platform.python_version()}")
    print("-" * 80)
    
    # Lista de dependencias requeridas
    dependencies = [
        "pandas",
        "openpyxl",  # Para leer archivos Excel
        "reportlab",  # Para generar PDFs
        "pillow",     # Para manipular imágenes
        "python-barcode",  # Para generar códigos de barras
    ]
    
    # Dependencias específicas para macOS
    if platform.system() == "Darwin":
        dependencies.append("pyobjc")
    
    # Instalar dependencias
    print("Instalando dependencias requeridas:")
    success = True
    for dep in dependencies:
        if not check_and_install(dep):
            success = False
    
    if success:
        print("\n✅ Todas las dependencias fueron instaladas correctamente.")
        print("\nAhora puedes ejecutar la aplicación con:")
        print("  python etiqueta_generator/launch.py")
    else:
        print("\n❌ Hubo errores al instalar algunas dependencias.")
        print("Intenta instalarlas manualmente con:")
        print("  pip install pandas openpyxl reportlab pillow python-barcode")
        if platform.system() == "Darwin":
            print("  pip install pyobjc")

if __name__ == "__main__":
    main()
