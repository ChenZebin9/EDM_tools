# -*- mode: python -*-

block_cipher = None


a = Analysis(['MainApp.py'],
             pathex=['D:\\Documents\\OneDrive\\Program\\Python\\EDM_tools'],
             binaries=[],
             datas=[('data\\config.db', 'data'), ('template\\arguments_explaination.txt', 'template'), ('template\\config', 'template'), ('template\\measurement_el_block', 'template'), ('template\\measurement_el_block_2', 'template'), ('template\\measurement_point', 'template')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='MainApp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='MainApp.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='MainApp')
