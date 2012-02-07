# -*- mode: python -*-
a = Analysis(['trayjenkins.py'],
             pathex=['submodules/pyjenkins'],
             hiddenimports=['encodings'],
             hookspath=None)
a.datas += Tree('media', prefix='media')
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'trayjenkins.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False )
