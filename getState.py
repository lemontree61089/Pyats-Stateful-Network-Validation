#!/usr/bin/env python3
from jinja2 import Environment, FileSystemLoader
import os
import sys
import socket 

def get_ip(hostname): 
    try:
        return socket.gethostbyname(hostname)  
    except: 
       print("Unable to get IP, might want to double-check the hostname") 
       exit()

def write_template(username,hostname,directory):
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    template = env.get_template('./jinja2/testbed.j2')
    output = template.render(username=username, hostname=hostname, directory=directory, ip=get_ip(hostname))
    f = open("./testbed.yml", 'w')
    f.write(output)
    f.close()

def get_models(argv):
    i = 4
    models = ""
    while i <= len(argv) - 1:
        models = models+argv[i]+" "
        i = i + 1
    return models

def main(username, hostname, directory, models):
    write_template(username, hostname, directory)
    print('template written')
    print('Launching container to get State')
    os.system("docker run -it --rm -v /opt/scripts/pyats/:/automation ciscotestautomation/pyats:latest pyats learn "+models+ \
    "--testbed-file /automation/testbed.yml --output /automation/res/"+directory)
    print('Done')

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Error, usage: ./getState.py username hostname directory model1 model2 ...")
        print("At least one model has to be provided")
        exit()
    else:  
       username = sys.argv[1]
       hostname = sys.argv[2]
       directory = sys.argv[3]
       models = get_models(sys.argv)
       main(username, hostname, directory, models)
