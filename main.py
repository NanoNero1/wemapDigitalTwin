print('Hello world')

import argparse
import os



def main(test):
    print(test)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    #parser.add_argument("square", type=int,
    #                help="display the square of a given number")

    parser.add_argument("test")
    args = parser.parse_args()

    main(args.test)

"""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
args = parser.parse_args()
print(args.echo)
"""


def processData():

    # run process command





