#!/usr/bin/env python3
import os
import sys

def main(directory1, directory2, diff_directory):
    os.system("docker run -it --rm -v /opt/scripts/pyats/:/automation ciscotestautomation/pyats:latest pyats diff \
    /automation/res/"+directory1+" /automation/res/"+directory2+" --output /automation/diff/"+diff_directory)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Error, usage: ./diffState.py directory1 directory2 diffDirectory")
        exit()
    else:
        directory1 = sys.argv[1]
        directory2 = sys.argv[2]
        diff_directory = sys.argv[3]
        main(directory1, directory2, diff_directory)
