#print('Hello world')

import argparse
import os
import subprocess
import shutil

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

    if 'train' in actions:
        ##### Training Model
        trainModel()


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

def commandParse(commandString):
    # Usally for running nerfstudio commands
    commandList = commandString.split()
    #print(commandList)
    subprocess.call(commandList,shell=True)
    #subprocess.call(["ls", "-l"])

def commandRaw(commandString):
    # Warning, don't use this unless necessary
    os.system(commandString)


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

    #parser.add_argument("outPath")


    args = parser.parse_args()

    main(args)







