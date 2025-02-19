echo "creating virtual environment..."
# download python installer
Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe -OutFile python-3.13.2-amd64.exe
# install python 3.13.2 into .\python
.\python-3.13.2-amd64.exe TargetDir=$PSScriptRoot\python AssociateFiles=0 Shortcuts=0 Include_doc=0 Include_launcher=0 /quiet
# wait for the python installer to finish
while($true) {
    Start-Sleep 1
    if(get-process | ?{$_.path -eq "$($PSScriptRoot)\python-3.13.2-amd64.exe"}){
        continue
    } else {
        break
    }
}

echo "installing required packages..."
.\python\Scripts\pip.exe install -r .\requirements.txt --no-warn-script-location

echo "building application..."
.\python\Scripts\pyinstaller.exe .\main.py --noconfirm --onefile --windowed --icon .\textures\icon.ico

echo "cleaning up..."
mv .\dist\main.exe .\autoclicker.exe
rm -r -Force dist
rm -r -Force build
rm -r -Force main.spec
.\python-3.13.2-amd64.exe /uninstall /quiet
# wait for the python uninstaller to finish
while($true) {
    Start-Sleep 1
    if(get-process | ?{$_.path -eq "$($PSScriptRoot)\python-3.13.2-amd64.exe"}){
        continue
    } else {
        break
    }
}
rm -r -Force python
rm -r -Force python-3.13.2-amd64.exe
echo "build finished. resulting binary is autoclicker.exe"
