# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['tiny_gui.py'],
    pathex=[],
    binaries=[('C:\\Users\\malenia0\\AppData\\Local\\Programs\\Python\\Python313\\DLLs\\tcl86t.dll', '.'), ('C:\\Users\\malenia0\\AppData\\Local\\Programs\\Python\\Python313\\DLLs\\tk86t.dll', '.')],
    datas=[('C:\\Users\\malenia0\\AppData\\Local\\Programs\\Python\\Python313\\tcl\\tcl8.6', 'tcl\\tcl8.6'), ('C:\\Users\\malenia0\\AppData\\Local\\Programs\\Python\\Python313\\tcl\\tk8.6', 'tcl\\tk8.6'), ('_third_party\\graphviz', '_third_party\\graphviz')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='tiny_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
