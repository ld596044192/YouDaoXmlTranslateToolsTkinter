# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['YouDao_XML_Translate\\xml_translate_tool\\youdao_gui.py'],
    pathex=[r'.\\YouDao_XML_Translate\\xml_translate_tool\\youdao_translate.py,.\\YouDao_XML_Translate\\xml_translate_tool\\content.py, \
    .\\YouDao_XML_Translate\\xml_translate_tool\\youdao_demo.py,.\\YouDao_XML_Translate\\xml_translate_tool\\my_thread.py, \
    .\\YouDao_XML_Translate\\xml_translate_tool\\xml_merge_demo\\xml_merge.py,.\\YouDao_XML_Translate\\xml_translate_tool\\xml_merge_demo\\xml_compare.py, \
    .\\YouDao_XML_Translate\\xml_translate_tool\\extra_functions\\single_xml_translate.py,.\YouDao_XML_Translate\xml_translate_tool\extra_functions\module_illustrate.py, \
    .\YouDao_XML_Translate\xml_translate_tool\extra_functions\zhoufei_tools.py,.\YouDao_XML_Translate\xml_translate_tool\extra_functions\template_function.py'],
    binaries=[],
    datas=[(r'.\YouDao_XML_Translate\xml_translate_tool\version',r'.\YouDao_XML_Translate\xml_translate_tool\version'),(r'.\YouDao_XML_Translate\xml_translate_tool\icon',r'.\YouDao_XML_Translate\xml_translate_tool\icon'),(r'.\YouDao_XML_Translate\xml_translate_tool\xml_merge_demo',r'.\YouDao_XML_Translate\xml_translate_tool\xml_merge_demo'),(r'.\YouDao_XML_Translate\xml_translate_tool\extra_functions',r'.\YouDao_XML_Translate\xml_translate_tool\extra_functions'),('YouDao_XML_Translate','YouDao_XML_Translate')],
    hiddenimports=[],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='xml批量翻译工具',
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
    icon=['YouDao_XML_Translate\\xml_translate_tool\\icon\\my-da.ico'],
)
