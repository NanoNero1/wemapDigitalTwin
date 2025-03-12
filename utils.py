import os
import subprocess
import json
import copy

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

def imageRangeTransform(imageRange):
    rangeList = imageRange.split(',')

    minImg = int(rangeList[0])
    maxImg = int(rangeList[1])

    # Open and read the JSON file
    with open('./digitalTwin/transforms.json', 'r') as file:
        data = json.load(file)

    allFrames = copy.deepcopy(data['frames'])
    clipFrames = []

    for f in allFrames:
        frameIdx = int(f['file_path'][-9:-4])
        #print(frameIdx)

        if (minImg <= frameIdx) and (frameIdx < maxImg):
            clipFrames.append(f)
        #error
        #if 

    #clipFrames = [f for f in clipFrames if f]
    data['frames'] = clipFrames

    # Serializing json
    json_object = json.dumps(data, indent=4)

    # Writing to sample.json
    with open(f"./digitalTwin/transforms.json", "w") as outfile:
        outfile.write(json_object)



    
    
    
    