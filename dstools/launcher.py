import docker

def launch_tool(t="afcai2c/jlab-cv",p=8888):
    client = docker.from_env()
    print('after the container starts')
    tool = client.containers.run(t,
        ports={p:p},
        detach=True)
    return(tool)
    

