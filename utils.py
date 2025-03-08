import os
import subprocess

def commandParse(commandString):
    # Usally for running nerfstudio commands
    commandList = commandString.split()
    #print(commandList)
    subprocess.call(commandList,shell=True)
    #subprocess.call(["ls", "-l"])

def commandRaw(commandString):
    # Warning, don't use this unless necessary
    os.system(commandString)

def makeFolder(folderDir):
    if not os.path.isdir(folderDir):
        os.mkdir(folderDir)
    else:
        print(f"### Folder {folderDir} already exists")
    