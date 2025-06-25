#!/bin/bash
# Script para empaquetar la aplicación de etiquetas en macOS

# Definir colores para la salida
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Iniciando proceso de empaquetado de la aplicación Generador de Etiquetas${NC}"

# Verificar si estamos en un entorno virtual
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}Creando entorno virtual...${NC}"
    python3 -m venv .venv
    source .venv/bin/activate
    echo -e "${GREEN}Entorno virtual activado.${NC}"
else
    echo -e "${GREEN}Usando entorno virtual existente: $VIRTUAL_ENV${NC}"
fi

# Instalar dependencias
echo -e "${YELLOW}Instalando dependencias...${NC}"
pip install -r requirements.txt

# Verificar si PyInstaller se instaló correctamente
if ! python -c "import PyInstaller" &> /dev/null; then
    echo -e "${YELLOW}PyInstaller no se instaló correctamente, intentando instalar directamente...${NC}"
    pip install PyInstaller==5.13.0
fi

# Crear directorios necesarios si no existen
mkdir -p assets data output

# Empaquetar la aplicación
echo -e "${YELLOW}Empaquetando la aplicación...${NC}"

# Obtener timestamp para el nombre del ejecutable
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
APP_NAME="Generador_Etiquetas_${TIMESTAMP}"

# Ejecutar PyInstaller directamente
pyinstaller --name="${APP_NAME}" \
            --onedir \
            --windowed \
            --add-data="assets/*:assets" \
            --add-data="data/*:data" \
            --hidden-import=PIL._tkinter_finder \
            --icon=assets/logo.png \
            gui_pyqt5.py

# Crear carpeta output en el paquete distribuible
mkdir -p "dist/${APP_NAME}/output"

echo -e "${GREEN}Aplicación empaquetada exitosamente en: $(pwd)/dist/${APP_NAME}${NC}"
echo -e "${GREEN}Ejecuta la aplicación con: dist/${APP_NAME}/${APP_NAME}${NC}"
