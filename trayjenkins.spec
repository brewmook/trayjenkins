# -*- mode: python -*-
a = Analysis(['trayjenkins.py'],
             pathex=['submodules/pyjenkins'],
             hiddenimports=['encodings'],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\trayjenkins', 'trayjenkins.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               Tree('media', prefix='media'),
               strip=None,
               upx=True,
               name=os.path.join('dist', 'trayjenkins'))
