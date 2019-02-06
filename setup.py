try:
    from setuptools import setup
except:
    from distutils.core import setup

config = {
    'description': 'Module create VBS MsgBox and return vbValue.',
    'author': 'Sergey Trishkin',
    'url': 'https://github.com/grdvsng/pyMsgBox',
    'download_url': 'https://drive.google.com/drive/folders/1mr5o5t4KpzyjqhxwxPhttP7x9NagP316?usp=sharing',
    'author_email': 'grdvsng@gmail.com',
    'version': '1.0',
    'install_requires': ['nose'],
    'packages': ['pyMsgBox'],
    'name': 'pyvoc',
    }

setup(**config)
