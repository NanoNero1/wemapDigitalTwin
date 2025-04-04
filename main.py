#print('Hello world')

import argparse
import os
import subprocess
import shutil
import json
from splitTrainTest import splitData
from utils import commandParse, imageRangeTransform
from renderTestImages import renderTestImages
from getMaskedTransform import getMaskedTransform

########################################################### PRACTICAL FUNCTIONS


def main(args):

    # Variables
    actions = args.actions.split(',')
    dataPath = args.dataPath
    imageRange = args.imageRange

    #print(imageRange)
    #error

    myOS = "windows"
    myPath = os.getcwd()

    # Change the current directory
    os.chdir(dataPath)
    

    ##### Processing Data

    if 'process' in actions:
        processData(dataPath)
        splitData()

    if 'train' in actions:
        trainModel(args.modelType,imageRange)

    if 'eval' in actions:
        renderTestImages(args.modelName)
        #TODO calculatPSNR


def processData(dataPath):

    # TODO: remove blurred images

    # Setup the necessary folders
    folderDir = os.path.join(dataPath,'digitalTwin')
    if os.path.exists(folderDir):
        print("#PIPELINE# digitalTwin folder already exists, skipping processing")
        #shutil.rmtree(folderDir)
    else:
        commandParse("mkdir digitalTwin")
        # Copies the 'sparse' folder. Might cause an error on Linux
        shutil.copytree(os.path.join(dataPath,'sparse'), os.path.join(dataPath,'digitalTwin/sparse'))

        # run process data command
        processDataCommand = f"ns-process-data images --verbose --skip-colmap --colmap-model-path sparse/0 --data ./images --output-dir ./digitalTwin" 
        
        # TODO add masks?
        
        commandParse(processDataCommand)

def clipTransfom():
    pass

def resetTransformJSON():
    os.remove(f"digitalTwin/transforms.json")

    # Save original train_transforms.json
    shutil.copyfile(f"./digitalTwin/transform_jsons/transforms_train_og.json",
                    f"digitalTwin/transforms.json")
    
def resetImageFolder():
    if os.path.isdir('./digitalTwin/images_train_original'):
        # Switch Image folders
        os.rename('./digitalTwin/images','./digitalTwin/images_inpainted')
        os.rename('./digitalTwin/images_train_original','./digitalTwin/images')


def trainModel(modelType,imageRange=None):

    print(modelType)


    print()

    if (modelType == None) or (modelType == 'nerfacto-basic'):

        resetTransformJSON()
        resetImageFolder()

        # Run training command
        trainCommand = f"ns-train nerfacto --data ./digitalTwin --pipeline.model.camera-optimizer.mode off"
    elif modelType == 'nerfacto-masked':

        resetTransformJSON()
        resetImageFolder()

        # add the masks to the transform
        getMaskedTransform()

        #error


        # Masked nerfacto is actually the same command
        trainCommand = f"ns-train nerfacto --data ./digitalTwin --pipeline.model.camera-optimizer.mode off"
    elif modelType == 'depth-nerfacto-inpainted':

        resetTransformJSON()

        # Switch Image folders
        if not os.path.isdir('./digitalTwin/images_train_original'):
            os.rename('./digitalTwin/images','./digitalTwin/images_train_original')
            os.rename('./digitalTwin/images_inpainted','./digitalTwin/images')

        trainCommand = "ns-train depth-nerfacto --data ./digitalTwin --pipeline.model.camera-optimizer.mode off --pipeline.model.depth-loss-type SPARSENERF_RANKING"
    elif modelType == 'splatfacto-basic':
        resetTransformJSON()
        resetImageFolder()
        # TODO splatfacto-masked!

        print('')
        error
        trainCommand = "ns-train splatfacto --data ./digitalTwin --pipeline.model.camera-optimizer.mode off"

    else:
        print("Training method not found, please choose between: nerfacto-basic,nerfacto-masked,depth-nerfacto-inpainted")

    if imageRange != None:
        imageRangeTransform(imageRange)
        
    #error

    # Open and read the JSON file
    with open('./digitalTwin/transform_jsons/transforms_train_og.json', 'r') as file:
        checkSize = json.load(file)

    if (len(checkSize['frames']) > 500) and imageRange == None:
        print("Image dataset too big to run at once, please provide an image range, e.g. --imageRange 2700,3000")
        erorr

    #error

    commandParse(trainCommand)

    # try:
        
    # except:
    #     print('Training run failed, retrying')
    #     commandParse(trainCommand)
        



def renderCamera():
    pass


########################################################### UTILITY FUNCTIONS


########################################################### ARGUMENT PARSER
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    #parser.add_argument("square", type=int,
    #                help="display the square of a given number")
    #parser.add_argument("square", type=int,
    #                help="display the square of a given number")

    parser.add_argument("actions", help="which actions to carry out [process,train,test]",
                    type=str)

    parser.add_argument("dataPath")

    parser.add_argument("--modelType", help="The type of model to train: nerfacto-basic,nerfacto-masked,depth-nerfacto-inpainted")

    parser.add_argument("--modelName", help="Name of the model in the outputs/digitalTwin/ folder. E.g. nerfacto/2025-03-08_200149")

    parser.add_argument("--imageRange", help="Which images are")

    args = parser.parse_args()

    main(args)







