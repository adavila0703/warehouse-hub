from shutil import copy, copytree, rmtree
import pathlib
import os
import time


def update():
    """Update is a script to auto update all the files that the user is using"""
    print('Warehouse Hub is updating, do not close this window...')

    time.sleep(3)

    print('Applying patch...')

    time.sleep(1)

    copy('C:/warehousehub/warehousehub.exe', pathlib.Path().absolute())
    rmtree(f'{pathlib.Path().absolute()}/templates')
    copytree('C:/warehousehub/templates', f'{pathlib.Path().absolute()}/templates')

    print('Patch Completed!')
    print('Warehouse Hub is restarting, please wait...')

    os.system(f'cmd /c "{pathlib.Path().absolute()}/warehousehub.exe"')


if __name__ == '__main__':
    update()
