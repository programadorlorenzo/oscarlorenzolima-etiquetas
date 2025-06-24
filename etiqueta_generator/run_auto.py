#!/usr/bin/env python3
"""
Script automatizado para ejecutar la aplicación con varios métodos en caso de problemas.
Este script intentará ejecutar la aplicación con diferentes configuraciones hasta encontrar
una que funcione correctamente.
"""
import os
import platform
import subprocess
import sys
import time

# Colores para console output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️ {text}{Colors.ENDC}")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

# Detección del sistema operativo
os_name = platform.system()
print_header(f"Generador de Etiquetas - Ejecutando en {os_name}")
print_info(f"Python {platform.python_version()} - {sys.executable}")

# Configuraciones de entorno
env = os.environ.copy()
env['TK_SILENCE_DEPRECATION'] = '1'
env['PYTHONUNBUFFERED'] = '1'

if os_name == "Darwin":  # macOS
    print_info("Detectado macOS, configurando variables de entorno específicas...")
    env['NSRequiresAquaSystemAppearance'] = 'YES'
    env['PYTHONCOERCECLOCALE'] = '0'
    env['LANG'] = 'en_US.UTF-8'

# Directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Definir los métodos de ejecución
execution_methods = []

if os_name == "Darwin":  # macOS
    execution_methods = [
        {
            "name": "Script específico para macOS",
            "command": ["python3", "macos_app.py"],
            "env": env
        },
        {
            "name": "Script de emergencia con configuración básica",
            "command": ["python3", "emergency_app.py"],
            "env": env
        },
        {
            "name": "Script alternativo con configuración para macOS Dark Mode",
            "command": ["python3", "run_app.py"],
            "env": env
        },
        {
            "name": "Script principal (última opción)",
            "command": ["python3", "main.py"],
            "env": env
        }
    ]
else:  # Windows o Linux
    execution_methods = [
        {
            "name": "Script de emergencia (interfaz mínima)",
            "command": ["python", "emergency_app.py"],
            "env": env
        },
        {
            "name": "Script alternativo",
            "command": ["python", "run_app.py"],
            "env": env
        },
        {
            "name": "Script principal",
            "command": ["python", "main.py"],
            "env": env
        }
    ]

# Intentar ejecutar la aplicación con cada método
for i, method in enumerate(execution_methods):
    print_header(f"\nMétodo {i+1}: {method['name']}")
    print_info(f"Ejecutando: {' '.join(method['command'])}")
    
    try:
        # Verificar que el archivo existe
        script_path = os.path.join(current_dir, method["command"][1])
        if not os.path.exists(script_path):
            print_warning(f"El archivo {script_path} no existe. Saltando este método.")
            continue
        
        # Ejecutar el comando
        process = subprocess.Popen(
            method["command"],
            env=method["env"],
            cwd=current_dir
        )
        
        # Esperar a que el usuario cierre la aplicación o presione Ctrl+C
        print_info("La aplicación está en ejecución. Presione Ctrl+C para probar el siguiente método.")
        process.wait()
        
        # Si el proceso terminó normalmente, preguntar si todo funcionó bien
        if process.returncode == 0:
            print_success("La aplicación se cerró correctamente.")
            response = input("¿La interfaz se visualizó correctamente? (s/n): ").lower()
            if response == 's' or response == 'si':
                print_success(f"¡Éxito! El método '{method['name']}' funciona correctamente.")
                print_info(f"Para futuras ejecuciones, use directamente: {' '.join(method['command'])}")
                sys.exit(0)
            else:
                print_warning("Probando con el siguiente método...")
        else:
            print_error(f"La aplicación terminó con código de error {process.returncode}.")
            print_warning("Probando con el siguiente método...")
    
    except KeyboardInterrupt:
        print_warning("\nEjecución interrumpida por el usuario.")
        try:
            process.terminate()
        except:
            pass
        print_info("Probando con el siguiente método...")
    except Exception as e:
        print_error(f"Error al ejecutar el método: {str(e)}")
        print_warning("Probando con el siguiente método...")

print_error("Se han probado todos los métodos disponibles sin éxito.")
print_warning("Posibles soluciones:")
print_info("1. Asegúrese de tener todas las dependencias instaladas: pip install -r requirements.txt")
print_info("2. Actualice Python y Tkinter a la última versión disponible.")
print_info("3. Si está en macOS, pruebe temporalmente cambiar a modo claro en Preferencias del Sistema.")
print_info("4. Contacte al desarrollador para obtener asistencia adicional.")
