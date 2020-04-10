#!/usr/bin/env python3
import os
import sys


if len(sys.argv) != 4:
  print("Error, usage: ./getState.py directory1 directory2 diffDirectory")
  exit()
  
directory1 = sys.argv[1]
directory2 = sys.argv[2]
diffDirectory = sys.argv[3]


os.system("docker run -it --rm -v /opt/scripts/pyats/:/automation ciscotestautomation/pyats:latest pyats diff \
/automation/res/"+directory1+" /automation/res/"+directory2+" --output /automation/diff/"+diffDirectory)


