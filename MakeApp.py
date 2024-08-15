import os
import shutil
import tkinter as tk
from tkinter import filedialog, colorchooser

COLOR_TYPES = ['Primary', 'Secondary', 'Success', 'Info', 'Warning', 'Danger', 'Light', 'Dark']
IMAGE_FILETYPES = '*.png *.jpg *.jpeg *.svg *.webp'

def promptAppName() -> str:
    appName = input('Enter project name: ')
    appName = appName.replace(' ', '-')
    return appName

def promptFile(filetypes: list[tuple] = [('All files', '*')]) -> str:
    path = filedialog.askopenfilename(filetypes=filetypes)
    return path

def promptColor(title: str = 'Choose Color') -> str:
    _, color_hex = colorchooser.askcolor(title=title)
    return color_hex

def createBlazoriseApp(appName: str, css: str = 'Bootstrap5', host: str = 'Server', framework: str = 'net8.0'):
    cmd = f'dotnet new blazorise -n {appName} -p {css} -bh {host} -f {framework}'
    os.system(cmd)

def configureApp(path: str, appName: str, colors: dict, logoPath: str, auth: bool = False):
    removeNode(f'{path}/Components/TodoApp')
    removeNode(f'{path}/Components/Layout/ThemeColorSelector.razor')
    removeNode(f'{path}/Components/Layout/ThemeColorSelector.razor.css')
    removeNode(f'{path}/Layouts/MainLayout.razor.cs')
    removeNode(f'{path}/Pages/Dashboard.razor')
    removeNode(f'{path}/Pages/SimpleFormPage.razor')
    removeNode(f'{path}/Pages/TodoAppPage.razor')
    removeNode(f'{path}/wwwroot/brand-logo.png')
    
    copyFile(logoPath, f'{path}/wwwroot')
    copyFile('./BaseFiles/SideMenu.razor', f'{path}/Components/Layout/SideMenu.razor')
    copyFile('./BaseFiles/TopMenu.razor', f'{path}/Components/Layout/TopMenu.razor')
    copyFile('./BaseFiles/MainLayout.razor', f'{path}/Layouts/MainLayout.razor')
    copyFile('./BaseFiles/Home.razor', f'{path}/Pages/Home.razor')
    copyFile('./BaseFiles/_Layout.cshtml', f'{path}/Pages/_Layout.cshtml')
    copyFile('./BaseFiles/App.razor', f'{path}/App.razor')
    
    replacements = [
        ('APP_NAME', appName),
        ('APP_LOGO', os.path.basename(logoPath)),
        ('PRIMARY_COLOR', f"\"{colors['Primary']}\""),
        ('SECONDARY_COLOR', f"\"{colors['Secondary']}\""),
        ('SUCCESS_COLOR', f"\"{colors['Success']}\""),
        ('INFO_COLOR', f"\"{colors['Info']}\""),
        ('WARNING_COLOR', f"\"{colors['Warning']}\""),
        ('DANGER_COLOR', f"\"{colors['Danger']}\""),
        ('LIGHT_COLOR', f"\"{colors['Light']}\""),
        ('DARK_COLOR', f"\"{colors['Dark']}\"")
    ]
    updateFile(f'{path}/Components/Layout/SideMenu.razor', replacements)
    updateFile(f'{path}/Components/Layout/TopMenu.razor', replacements)
    updateFile(f'{path}/Layouts/MainLayout.razor', replacements)
    updateFile(f'{path}/App.razor', replacements)
    updateFile(f'{path}/Pages/_Layout.cshtml', replacements)
    
    if auth:
        pass
    

def copyFile(file: str, to: str) -> bool:
    shutil.copy(file, to)

def removeNode(path):
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)
        
def updateFile(path: str, replacements: list[tuple] = []):
    with open(path, 'r') as infile:
        file_content = infile.read()
        
    new_content = file_content
    for replacement in replacements:
        find,replace = replacement
        new_content = new_content.replace(find, replace)
        
    with open(path, 'w') as outfile:
        outfile.write(new_content)

if __name__ == '__main__':
    appName = promptAppName()
    
    logoPath = promptFile([('Image files', IMAGE_FILETYPES)])

    colors = dict.fromkeys(COLOR_TYPES, '#ffffff')
    for color_type in COLOR_TYPES:
        colors[color_type] = promptColor(color_type)

    createBlazoriseApp(appName)
    configureApp(f'./{appName}/{appName}', appName, colors, logoPath)


