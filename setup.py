from setuptools import setup

APP = ['ChemCalc.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['ttkbootstrap'],
    'iconfile': 'icons/chemcalc.ico',
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)


#copy and paste this in terminal to create the .app file
#python setup.py py2app

#copy and paste this in terminal to create the .exe file
#pyinstaller --noconfirm --onefile --windowed --icon=icons/chemcalc.ico ChemCalc.py

# MacOS icon conversion command
#sips -s format icns icons/chemcalc_icon.png --out icons/chemcalc.icns
