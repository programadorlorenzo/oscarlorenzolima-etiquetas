# Generador de Etiquetas

Aplicación para generar etiquetas de productos con código de barras en formato PDF y gestionar datos en Excel.

## Características

- Interfaz gráfica intuitiva (GUI) utilizando PyQt5
- Formulario para agregar/editar productos individualmente
- Importación de productos desde archivos Excel
- Generación de códigos de barras únicos basados en SKU
- Exportación de etiquetas en formato PDF (3x4 cm, 3 columnas por página)
- Exportación de datos de productos a Excel
- Réplica automática de etiquetas según stock
- Compatibilidad con modo oscuro en macOS

## Estructura del Proyecto

```
etiquetas/
├── assets/               # Recursos como logos e imágenes
├── data/                 # Archivos Excel de productos
├── output/               # PDFs y Excels generados
├── gui_pyqt5.py          # Interfaz gráfica principal (PyQt5)
├── excel_manager.py      # Manejo de Excel y generación de códigos de barras
├── generador_etiqueta.py # Generación de PDF de etiquetas
├── etiqueta_pdf.py       # Clase Etiqueta para generar etiquetas individuales
├── empaquetar_mac.sh     # Script para empaquetar en macOS (ejecutable)
├── crear_app_mac.sh      # Script para crear .app en macOS
└── requirements.txt      # Dependencias del proyecto
```

## Requisitos

- Python 3.7+
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio o descargar los archivos
2. Crear un entorno virtual (recomendado):
   ```
   python3 -m venv .venv
   source .venv/bin/activate  # En macOS/Linux
   ```
3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

## Ejecución

Para ejecutar la aplicación:

```
python gui_pyqt5.py
```

## Empaquetado

### Para macOS

#### Opción 1: Crear ejecutable con PyInstaller

```
./empaquetar_mac.sh
```

El ejecutable se creará en la carpeta `dist/Generador_Etiquetas_YYYYMMDD_HHMMSS/`.

#### Opción 2: Crear aplicación .app

```
./crear_app_mac.sh
```

La aplicación .app se creará en `dist/GeneradorEtiquetas.app`.

### Para Windows

Para empaquetar en Windows, necesitarás PyInstaller y ejecutar:

```
pyinstaller --name="Generador_Etiquetas" --onedir --windowed --add-data="assets/*;assets" --add-data="data/*;data" --hidden-import=PIL._tkinter_finder --icon=assets/logo.png gui_pyqt5.py
```

## Licencia

Propiedad de JOLG - Todos los derechos reservados
