#!/usr/bin/env python3
import docker, webbrowser

client = docker.from_env()

localhost = "http://localhost"
image     = "afcai2c/jlab-cv"
tag       = "latest"
port      = 8888
def startTool(image,tag,port):
    imageName = "{0}:{1}".format(image,tag)
    print('after the container starts')
    tool = client.containers.run(
        imageName,
        ports={port:port},
        detach=True)
    return(tool)

startTool(image,tag,port)
launchUrl = "{0}:{1}".format(localhost,port)
webbrowser.open(launchUrl)
