print('Hello world')

import argparse
import os
import subprocess




def main(test):
    print(test)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    #parser.add_argument("square", type=int,
    #                help="display the square of a given number")

    parser.add_argument("test")

    parser.add_argument("dataPath")
    args = parser.parse_args()

    myOS = "windows"
    myPath = os.getcwd()

    dataPath = ""

    print(myPath)

    main(args.test)

"""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
args = parser.parse_args()
print(args.echo)
"""


def processData():

    # setup the folders

    # TODO: remove blurred images

    # TODO run process data command
    processDataCommand = f"ns-process-data images --verbose --skip-colmap --colmap-model-path sparse/0 --num-downscales 4 --data ./images --output-dir ./hopeWorks" 

    #os.





def trainModel():
    pass



def renderCamera():
    pass



# Utility Functions

def commandParse(commandString):
    commandList = commandString.split()
    subprocess.call([c for c in commandList])
    #subprocess.call(["ls", "-l"])

def commandRaw(commandString):
    os.system(commandString)







