import os
import shutil
import tkinter as tk
from tkinter import filedialog, colorchooser

COLOR_TYPES = ['Primary', 'Secondary', 'Success', 'Info', 'Warning', 'Danger', 'Light', 'Dark']
IMAGE_FILETYPES = '*.png *.jpg *.jpeg *.svg *.webp'

def promptFile(filetypes: list[tuple] = [('All files', '*')]) -> str:
    path = filedialog.askopenfilename(filetypes=filetypes)
    return path

def promptColor(title: str = 'Choose Color') -> str:
    color_rgb, color_hex = colorchooser.askcolor(title=title)
    return color_hex

def createBlazoriseApp(appName: str, css: str = 'Bootstrap5', host: str = 'Server', framework: str = 'net8.0'):
    cmd = f'dotnet new blazorise -n {appName} -p {css} -bh {host} -f {framework}'
    os.system(cmd)

def configureApp(path: str):
    removeFile(f'{path}/Components/TodoApp')
    removeFile(f'{path}/Pages/SimpleFormPage.razor')
    removeFile(f'{path}/Pages/TodoAppPage.razor')
    removeFile(f'{path}/wwwroot/brand-logo.png')
    os.replace(f'{path}/Pages/Dashboard.razor', f'{path}/Pages/Home.razor')

def copyFile(file: str, to: str) -> bool:
    shutil.copy(file, to)

def removeFile(path):
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)

if __name__ == '__main__':
    appName = 'test'
    createBlazoriseApp(appName)
    logo = promptFile([('Image files', IMAGE_FILETYPES)])

    colors = dict.fromkeys(COLOR_TYPES, '#ffffff')
    #for color_type in COLOR_TYPES:
    #    colors[color_type] = promptColor(color_type)

    copyFile(logo, f'./{appName}/{appName}/wwwroot')
    configureApp(f'./{appName}/{appName}')


