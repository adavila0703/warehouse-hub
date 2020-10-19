from shutil import copytree, rmtree
import os
import time


def patch():
    """Patch.py is meant to move all new files to the installer location"""
    print('Pushing Patch')
    os.system(f'start cmd /c "pyinstaller app.py -F -n warehousehub --distpath C:/Documents/warehousehub"')
    time.sleep(1)
    rmtree(f'C:/Documents/warehousehub/templates')
    print('Updating Templates')
    time.sleep(1)
    copytree('C:/warehousehub/templates',
             f'C:/Documents/warehousehub/templates')
    print('Done')


if __name__ == '__main__':
    patch()
