; Script para crear un instalador para Windows usando NSIS
; Guarda este archivo como installer.nsi y compílalo con NSIS después de generar el ejecutable con PyInstaller

!include "MUI2.nsh"
!include "FileFunc.nsh"

; Definir nombre de la aplicación y compañía
!define APPNAME "Generador de Etiquetas"
!define COMPANYNAME "JOLG"
!define DESCRIPTION "Aplicación para generar etiquetas de productos con código de barras"

; Obtener la fecha actual para el nombre del instalador
!define /date NOW "%Y%m%d_%H%M%S"

; Obtener carpeta de la aplicación (debe ajustarse al nombre generado por PyInstaller)
; Por defecto usamos un nombre estático, pero deberías cambiarlo al nombre exacto generado por PyInstaller
!define APPFOLDER "Generador_Etiquetas_${NOW}"

; Nombres de archivos
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPLINK "http://www.example.com"
!define UPDATELINK "http://www.example.com"
!define ABOUTLINK "http://www.example.com"

; Configuración general
Name "${APPNAME}"
OutFile "Instalador_${APPNAME}_${NOW}.exe"
InstallDir "$PROGRAMFILES\${COMPANYNAME}\${APPNAME}"
InstallDirRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "UninstallString"
RequestExecutionLevel admin

; Interfaz de usuario
!define MUI_ABORTWARNING
!define MUI_ICON "assets\logo.ico"
!define MUI_UNICON "assets\logo.ico"

; Páginas del instalador
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Páginas de desinstalación
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Idiomas
!insertmacro MUI_LANGUAGE "Spanish"

; Sección de instalación
Section "Instalar"
    SetOutPath "$INSTDIR"
    
    ; Copiar todos los archivos de la carpeta dist de PyInstaller
    File /r "dist\${APPFOLDER}\*.*"
    
    ; Crear carpeta output si no existe
    CreateDirectory "$INSTDIR\output"
    
    ; Crear acceso directo en el menú de inicio
    CreateDirectory "$SMPROGRAMS\${COMPANYNAME}"
    CreateShortCut "$SMPROGRAMS\${COMPANYNAME}\${APPNAME}.lnk" "$INSTDIR\${APPFOLDER}.exe" "" "$INSTDIR\${APPFOLDER}.exe" 0
    
    ; Crear acceso directo en el escritorio
    CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${APPFOLDER}.exe" "" "$INSTDIR\${APPFOLDER}.exe" 0
    
    ; Registrar información de desinstalación
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "InstallLocation" "$\"$INSTDIR$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "DisplayIcon" "$\"$INSTDIR\${APPFOLDER}.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "Publisher" "${COMPANYNAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "HelpLink" "${HELPLINK}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "URLUpdateInfo" "${UPDATELINK}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "URLInfoAbout" "${ABOUTLINK}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "VersionMinor" ${VERSIONMINOR}
    
    ; Calculamos el tamaño de la instalación
    ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
    IntFmt $0 "0x%08X" $0
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "EstimatedSize" "$0"
    
    ; Crear archivo de desinstalación
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

; Sección de desinstalación
Section "Uninstall"
    ; Eliminar archivos y carpetas de programa
    RMDir /r "$INSTDIR\*.*"
    RMDir "$INSTDIR"
    
    ; Eliminar accesos directos
    Delete "$SMPROGRAMS\${COMPANYNAME}\${APPNAME}.lnk"
    RMDir "$SMPROGRAMS\${COMPANYNAME}"
    Delete "$DESKTOP\${APPNAME}.lnk"
    
    ; Eliminar claves de registro
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}"
SectionEnd
