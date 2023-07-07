import PySimpleGUI as sg
import subprocess as sp
from xml.dom.minidom import parse
import win32com.client as wc

sg.theme("Dark")

srcDir = "D:\\IdeaProjects\\BetterRecipesV2"
destDir = ""
pomDir = srcDir + "\\pom.xml"

pom = parse(pomDir)
pluginName = pom.getElementsByTagName("artifactId")[0].childNodes[0].data
version = pom.getElementsByTagName("version")[0].childNodes[0].data

layout = [  [sg.Text("Source Directory: " + srcDir)],
            [sg.Text("Destination Directory: " + destDir)],
            [sg.Checkbox("Delete Config Folder", key="delete")],
            [sg.Button("Start"), sg.Button("Stop"), sg.Button("Exit")] ]

window = sg.Window("Auto Move", layout, size=(500, 150))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "Start":
        sp.run(["mvn", "package", "-f", pomDir], shell=True)
        sp.run(["copy", "/y", f"{srcDir}\\target\\{pluginName} {version}.jar", f"{destDir}\\plugins"], shell=True)
        
        if values["delete"] == True:
            sp.run(["rmdir", "/s", "/q", f"{destDir}\\plugins\\{pluginName}"], shell=True)

        sp.run(f"start cmd /k \"title SERVER & cd Scripts & deactivate.bat & cd \"{destDir}\" & start.bat\"", shell=True)
    elif event == "Stop":
        shell = wc.Dispatch("WScript.Shell")
        shell.AppActivate("SERVER  - start.bat")
        shell.SendKeys("stop{ENTER}")
    elif event == "Exit":
        shell = wc.Dispatch("WScript.Shell")
        shell.AppActivate("SERVER")
        shell.SendKeys("exit{ENTER}")

window.close()
