@echo off
REM Script para empaquetar la aplicación de etiquetas en Windows

echo Iniciando proceso de empaquetado de la aplicación Generador de Etiquetas
echo.

REM Verificar si estamos en un entorno virtual
python -c "import sys; print('virtual' if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 'system')" > temp.txt
set /p ENV_TYPE=<temp.txt
del temp.txt

if "%ENV_TYPE%"=="system" (
    echo Creando entorno virtual...
    python -m venv .venv
    call .venv\Scripts\activate
    echo Entorno virtual activado.
) else (
    echo Usando entorno virtual existente.
)

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

REM Verificar si PyInstaller se instaló correctamente
python -c "import PyInstaller" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller no se instaló correctamente, intentando instalar directamente...
    pip install PyInstaller==5.13.0
)

REM Crear directorios necesarios si no existen
if not exist assets mkdir assets
if not exist data mkdir data
if not exist output mkdir output

REM Empaquetar la aplicación
echo Empaquetando la aplicación...

REM Obtener timestamp para el nombre del ejecutable
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set "timestamp=%datetime:~0,8%_%datetime:~8,6%"
set "APP_NAME=Generador_Etiquetas_%timestamp%"

REM Ejecutar PyInstaller directamente
pyinstaller --name="%APP_NAME%" ^
            --onedir ^
            --windowed ^
            --add-data="assets\*;assets" ^
            --add-data="data\*;data" ^
            --hidden-import=PIL._tkinter_finder ^
            --icon=assets\logo.png ^
            gui_pyqt5.py

REM Crear carpeta output en el paquete distribuible
if not exist "dist\%APP_NAME%\output" mkdir "dist\%APP_NAME%\output"

echo.
echo Aplicación empaquetada exitosamente en: %CD%\dist\%APP_NAME%
echo Ejecuta la aplicación con: dist\%APP_NAME%\%APP_NAME%.exe
echo.

pause
