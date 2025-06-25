#!/bin/bash
# Script para crear un archivo .app para macOS

# Definir colores para la salida
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Iniciando proceso de creación de aplicación .app para macOS${NC}"

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

# Verificar si py2app se instaló
if ! python -c "import py2app" &> /dev/null; then
    echo -e "${YELLOW}Instalando py2app...${NC}"
    pip install py2app
fi

# Crear setup.py para py2app
echo -e "${YELLOW}Creando setup.py para py2app...${NC}"
cat > setup.py << 'EOF'
"""
Script de configuración para crear una aplicación macOS (.app)
usando py2app.
"""
from setuptools import setup

APP = ['gui_pyqt5.py']
DATA_FILES = [
    ('assets', ['assets/logo.png']),
    ('data', ['data/productos.xlsx']),
    ('', ['requirements.txt']),
]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5', 'pandas', 'reportlab', 'PIL'],
    'iconfile': 'assets/logo.png',
    'plist': {
        'CFBundleName': 'GeneradorEtiquetas',
        'CFBundleDisplayName': 'Generador de Etiquetas',
        'CFBundleGetInfoString': 'Aplicación para generar etiquetas de productos',
        'CFBundleIdentifier': 'com.etiquetas.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': '© 2023',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
EOF

# Limpiar build previo si existe
echo -e "${YELLOW}Limpiando builds previos...${NC}"
rm -rf build dist

# Construir la aplicación
echo -e "${YELLOW}Construyendo la aplicación .app...${NC}"
python setup.py py2app

# Crear carpeta output en la aplicación
mkdir -p "dist/GeneradorEtiquetas.app/Contents/Resources/output"

echo -e "${GREEN}Aplicación .app creada exitosamente en: $(pwd)/dist/GeneradorEtiquetas.app${NC}"
echo -e "${GREEN}Puedes abrir la aplicación haciendo doble clic en el Finder o con el comando:${NC}"
echo -e "${GREEN}open dist/GeneradorEtiquetas.app${NC}"
