#!/usr/bin/env python3
"""
Script de lanzamiento que resuelve problemas específicos de macOS Dark Mode.
Este script detecta el sistema operativo y lanza el script adecuado,
con un enfoque especial en los problemas de modo oscuro en macOS.

Este es el script principal que debes usar si tienes problemas con
la interfaz gráfica, especialmente en macOS con modo oscuro.
"""
import os
import sys
import platform
import subprocess

def print_header():
    """Imprime el encabezado del script."""
    print("=" * 80)
    print(" LANZADOR UNIVERSAL DEL GENERADOR DE ETIQUETAS ".center(80, "="))
    print("=" * 80)
    print(f"Sistema detectado: {platform.system()} {platform.release()}")
    print(f"Python: {platform.python_version()}")
    print("-" * 80)

def check_macos_dark_mode():
    """Verifica si macOS está en modo oscuro."""
    if platform.system() != "Darwin":
        return False
    
    return os.system('defaults read -g AppleInterfaceStyle 2>/dev/null') == 0

def run_app():
    """Ejecuta la aplicación según el sistema operativo."""
    # Obtener directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Obtener ruta del intérprete de Python
    python_exe = sys.executable
    
    # Configurar variables de entorno comunes
    env = os.environ.copy()
    env['TK_SILENCE_DEPRECATION'] = '1'
    
    # Determinar qué script ejecutar según el sistema
    if platform.system() == "Darwin":  # macOS
        is_dark_mode = check_macos_dark_mode()
        
        if is_dark_mode:
            print("Detectado macOS en modo oscuro")
            print("Usando configuración especial para compatibilidad con modo oscuro")
            
            # Configurar variables adicionales para macOS
            env['NSRequiresAquaSystemAppearance'] = 'YES'
            env['PYTHONCOERCECLOCALE'] = '0'
            env['LANG'] = 'en_US.UTF-8'
            env['SYSTEM_VERSION_COMPAT'] = '1'
            
            # Intentar con la solución más avanzada primero
            script_path = os.path.join(current_dir, "macos_fix.py")
        else:
            print("Detectado macOS en modo claro")
            print("Usando configuración estándar para macOS")
            
            # En modo claro, usar run_app.py que debería funcionar bien
            script_path = os.path.join(current_dir, "run_app.py")
    
    elif platform.system() == "Windows":  # Windows
        print("Detectado Windows")
        print("Usando configuración estándar para Windows")
        script_path = os.path.join(current_dir, "run_app.py")
    
    else:  # Linux u otro
        print("Detectado Linux u otro sistema")
        print("Usando configuración estándar")
        script_path = os.path.join(current_dir, "run_app.py")
    
    # Ejecutar el script seleccionado
    print(f"Ejecutando: {script_path}")
    print("-" * 80)
    
    try:
        subprocess.run([python_exe, script_path], env=env)
        print("\nAplicación cerrada correctamente.")
    except Exception as e:
        print(f"\nError al ejecutar la aplicación: {e}")
        print("\nIntentando con método alternativo...")
        
        # Si falla, intentar con emergency_app.py
        try:
            emergency_script = os.path.join(current_dir, "emergency_app.py")
            print(f"Ejecutando script de emergencia: {emergency_script}")
            subprocess.run([python_exe, emergency_script], env=env)
        except Exception as e2:
            print(f"\nError en el método alternativo: {e2}")
            print("\nPor favor, consulte la sección de solución de problemas en el README.")

if __name__ == "__main__":
    print_header()
    run_app()
