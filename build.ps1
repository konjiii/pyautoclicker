echo "creating virtual environment..."
# download python installer
curl https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe > python-3.13.2-amd64.exe
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
pyinstaller .\main.py --noconfirm --onefile --windowed --icon .\textures\icon.ico

echo "cleaning up..."
mv .\dist\main.exe .
rm -r dist
rm -r build
rm -r main.spec
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
rm -r python
rm -r python-3.13.2-amd64.exe