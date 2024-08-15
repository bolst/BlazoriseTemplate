import os



def createBlazoriseApp(appName: str, css: str = 'Bootstrap5', host: str = 'Server', framework: str = 'net8.0'):
    cmd = f'dotnet new blazorise -n {appName} -p {css} -bh {host} -f {framework}'
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':
    createBlazoriseApp('test')
