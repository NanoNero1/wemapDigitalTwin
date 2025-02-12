print('Hello world')

import argparse
import os
import subprocess
import shutil

########################################################### PRACTICAL FUNCTIONS


def main(args):

    ##### Setup 

    # Variables
    dataPath = args.dataPath
    myOS = "windows"
    myPath = os.getcwd()

    # Change the current directory
    os.chdir(dataPath)

    # Setup the necessary folders
    folderDir = os.path.join(dataPath,'hopeWorks')
    if os.path.exists(folderDir):
        shutil.rmtree(folderDir)
        os.makedirs(folderDir)
    #commandParse("mkdir hopeWorks")

    # Copies the 'sparse' folder. Might cause an error on Linux
    shutil.copytree(os.path.join(dataPath,'sparse'), os.path.join(dataPath,'hopeWorks/sparse'))
    

    ##### Processing Data
    processData()

    ##### Training Model
    trainModel()


    ##### Rendering TODO

    print(myPath)
    print(dataPath)


def processData():

    # TODO: remove blurred images

    # run process data command
    processDataCommand = f"ns-process-data images --verbose --skip-colmap --colmap-model-path sparse/0 --num-downscales 4 --data ./images --output-dir ./hopeWorks" 
    commandParse(processDataCommand)

def trainModel():

    # Run training command
    trainCommand = f"ns-train nerfacto --data ./hopeWorks --pipeline.model.camera-optimizer.mode off" 

    try:
        commandParse(trainCommand)
    except:
        print('Training run failed, retrying')
        commandParse(trainCommand)
        



def renderCamera():
    pass


########################################################### UTILITY FUNCTIONS

def commandParse(commandString):
    # Usally for running nerfstudio commands
    commandList = commandString.split()
    print(commandList)
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

    parser.add_argument("dataPath")
    args = parser.parse_args()

    main(args)







