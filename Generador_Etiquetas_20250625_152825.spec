# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['gui_pyqt5.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/*', 'assets'), ('data/*', 'data')],
    hiddenimports=['PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Generador_Etiquetas_20250625_152825',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/logo.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Generador_Etiquetas_20250625_152825',
)
app = BUNDLE(
    coll,
    name='Generador_Etiquetas_20250625_152825.app',
    icon='assets/logo.png',
    bundle_identifier=None,
)
