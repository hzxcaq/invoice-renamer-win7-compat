# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\invoice_renamer\\main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['invoice_renamer.gui', 'invoice_renamer.gui.main_window', 'invoice_renamer.gui.file_selector', 'invoice_renamer.gui.excel_viewer', 'invoice_renamer.gui.format_builder', 'invoice_renamer.gui.preview_table', 'invoice_renamer.core', 'invoice_renamer.core.excel_reader', 'invoice_renamer.core.file_matcher', 'invoice_renamer.core.renamer'],
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
    name='发票批量重命名工具_v2',
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
    icon='NONE',
)
