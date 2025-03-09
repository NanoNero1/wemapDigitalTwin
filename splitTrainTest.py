import json
import copy
import numpy as np
import random
import shutil
import os
from utils import commandParse
from utils import makeFolder

def splitData():

    print(os.getcwd())
    currPath = os.getcwd()
    #error
    # Making necessary folders

    if os.path.exists("./digitalTwin/test_folder"):
        print(" \n Already split into training/test data. To re-do the split please TODO \n")
        return

    makeFolder("./digitalTwin/test_folder")
    makeFolder("./digitalTwin/transform_jsons")
    makeFolder("./digitalTwin/train_folder")
    #if not os.path.isdir("./digitalTwin/test_folder"):
    #    os.mkdir("./digitalTwin/test_folder")
    #os.mkdir("./digitalTwin/transform_jsons")
    #commandParse("mkdir digitalTwin/test_folder")
    #commandParse("mkdir digitalTwin/transform_jsons")
    ##error


    # Open and read the JSON file
    with open('./digitalTwin/transforms.json', 'r') as file:
        data = json.load(file)

    # Sort the frames by order they are taken in
    sortFrames = sorted(data['frames'], key=lambda x: x["file_path"], reverse=False)


    posesPerImg = 12
    totalFrames = len(sortFrames)
    data['frames'] = sortFrames

    # Getting the json/dictionary objects
    testDict = copy.deepcopy(data)
    trainDict = copy.deepcopy(data)
    testDict['frames'] = []
    trainDict['frames'] = []

    for imgIdx in range(int(totalFrames / posesPerImg)):
        
        # Randomly sample a frame from one 360 image
        testIndex = random.randint(0,posesPerImg)
        
        # Test Frames
        testDict['frames'].append(sortFrames[imgIdx*posesPerImg + testIndex])
        
        # Training Frames
        tFrames = sortFrames[imgIdx*posesPerImg : imgIdx*posesPerImg + testIndex] + sortFrames[imgIdx*posesPerImg + testIndex + 1 : (1 + imgIdx)*posesPerImg  ]

        #print(len(tFrames))

        for frame in tFrames:
            
            #print(frame)
            #error
            trainDict['frames'].append(frame)


    # Copying Images
    for f in testDict['frames']:
        shutil.copyfile(f"./digitalTwin/{f['file_path']}",
                        f"./digitalTwin/test_folder/{f['file_path'][-15:]}")
        
    for f in trainDict['frames']:
        shutil.copyfile(f"./digitalTwin/{f['file_path']}",
                        f"./digitalTwin/train_folder/{f['file_path'][-15:]}")

    # Saving test transforms
    json_object = json.dumps(testDict, indent=4)
    with open("./digitalTwin/test_folder/test_transforms.json", "w") as outfile:
        outfile.write(json_object)

    # Save original transforms.json
    shutil.copyfile(f"digitalTwin/transforms.json",
                        f"./digitalTwin/transform_jsons/transforms_og.json")

    # Removing old Transforms 
    os.remove("./digitalTwin/transforms.json")

    # Saving new (training) transforms
    json_object = json.dumps(trainDict, indent=4)
    with open("./digitalTwin/transforms.json", "w") as outfile:
        outfile.write(json_object)

    # Save original train_transforms.json
    shutil.copyfile(f"digitalTwin/transforms.json",
                        f"./digitalTwin/transform_jsons/transforms_train_og.json")

    # TODO rename folders
    os.rename("./digitalTwin/images","./digitalTwin/images_original")
    os.rename("./digitalTwin/train_folder","./digitalTwin/images")



    

