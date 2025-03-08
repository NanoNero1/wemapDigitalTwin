#print('Hello world')

import argparse
import os
import subprocess
import shutil
from splitTrainTest import splitData
from utils import commandParse
from renderTestImages import renderTestImages

########################################################### PRACTICAL FUNCTIONS


def main(args):

    ##### Setup 


    print(args)
    print(args.dataPath)
    

    actions = args.actions.split(',')



    #print(actions)

    #error

    # Variables
    dataPath = args.dataPath
    myOS = "windows"
    myPath = os.getcwd()

    # Change the current directory
    os.chdir(dataPath)
    

    ##### Processing Data

    if 'process' in actions:
        processData(dataPath)
        splitData()
        #error

    if 'train' in actions:
        ##### Training Model
        trainModel()

    if 'eval' in actions:
        renderTestImages(args.modelName)
        #calculatPSNR


    ##### Rendering TODO

    #print(myPath)
    #print(dataPath)


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


def trainModel():

    # Run training command
    trainCommand = f"ns-train nerfacto --data ./digitalTwin --pipeline.model.camera-optimizer.mode off" 


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

    parser.add_argument("--modelName", help="Name of the model in the outputs/digitalTwin/ folder. E.g. nerfacto/2025-03-08_200149")

    #parser.add_argument("outPath")


    args = parser.parse_args()

    main(args)







