#!/usr/bin/env python3
"""
Script ultra simple para macOS que solo ejecuta el programa sin importar nada adicional.
Esta es una versión mínima que usa Python para evitar problemas de importación o configuración.
"""
import os
import sys
import platform
import subprocess

# Obtener la ruta al ejecutable de Python que está siendo usado actualmente
python_executable = sys.executable

# Obtener el directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Definir las variables de entorno necesarias
env_vars = {
    'NSRequiresAquaSystemAppearance': 'YES',
    'TK_SILENCE_DEPRECATION': '1',
    'PYTHONCOERCECLOCALE': '0',
    'LANG': 'en_US.UTF-8',
    'SYSTEM_VERSION_COMPAT': '1'
}

# Copiar las variables de entorno actuales
env = os.environ.copy()

# Añadir nuestras variables de entorno
for key, value in env_vars.items():
    env[key] = value

# Crear un script temporal extremadamente simple
temp_script_content = """
import tkinter as tk

# Crear una ventana básica
root = tk.Tk()
root.title("Test de Tkinter en macOS")
root.geometry("300x200")

# Forzar colores claros
root.configure(bg='white')

# Etiqueta con mensaje
label = tk.Label(
    root, 
    text="Si puedes ver este texto, Tkinter funciona correctamente.", 
    bg='white', 
    fg='black',
    wraplength=280
)
label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Botón para cerrar
button = tk.Button(
    root, 
    text="Cerrar", 
    command=root.destroy,
    bg='lightgray',
    fg='black'
)
button.pack(pady=20)

# Iniciar el bucle principal
root.mainloop()
"""

temp_script_path = os.path.join(current_dir, "_test_tk.py")

# Escribir el script temporal
with open(temp_script_path, "w") as f:
    f.write(temp_script_content)

try:
    # Ejecutar el script con las variables de entorno configuradas
    print("Ejecutando prueba básica de Tkinter...")
    subprocess.run([python_executable, temp_script_path], env=env)
    
    # Si llegamos aquí, el script se ejecutó sin errores fatales
    print("\n✅ La prueba básica de Tkinter funcionó correctamente.")
    print("Si pudo ver la ventana con texto negro sobre fondo blanco, la configuración básica funciona.")
    print("\nAhora puede intentar ejecutar la aplicación principal con:")
    print(f"  {python_executable} {os.path.join(current_dir, 'run_macos.py')}")
    
except Exception as e:
    print(f"\n❌ Error al ejecutar la prueba: {e}")
    print("Esto indica problemas fundamentales con la configuración de Tkinter.")
    
finally:
    # Eliminar el script temporal
    try:
        os.remove(temp_script_path)
    except:
        pass
