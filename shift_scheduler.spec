# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/run_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('config/config.json', 'config'), ('venv/lib/python3.12/site-packages/pulp/', 'pulp/')],
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
    [],
    exclude_binaries=True,
    name='shift_scheduler',
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
    icon=['icon/feather_pen.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='shift_scheduler',
)
app = BUNDLE(
    coll,
    name='shift_scheduler.app',
    icon='icon/feather_pen.ico',
    bundle_identifier=None,
)
