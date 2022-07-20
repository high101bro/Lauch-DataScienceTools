#!/usr/bin/env python3
import docker, click, webbrowser, requests, json, time, re, os
from operator import itemgetter
from pathlib import Path

# Placeholders
localhost = 'http://localhost'
image = None
tag = None
port = None
start = None
stop_tool = None

client = docker.from_env()


#####################################################################
# update to this
# client.images.search('afcai2c')
#####################################################################

# This list contains images to exclude from being displayed
excludedImages = [
    'afcai2c/ubi8',
    'afcai2c/python36',
    'afcai2c/python36-ai',
    'afcai2c/python38',
    'afcai2c/python38-ai',
    'afcai2c/python-r-ai',
    'afcai2c/jupyterlab',
    'afcai2c/r-base',
    'afcai2c/r-studio',
    'afcai2c/r-studio-valex',
    'afcai2c/tensorboard',
    'afcai2c/openjdk11'
    ]

# #create(name='dsVolume', driver='local')
# client.volumes.prune()
# print(
#    client.volumes.list()
#    )
# client.volumes.prune()

##### Start Method 1 #####
dsToolDict = client.images.search('afcai2c')
dsToolDict = sorted(dsToolDict, key=itemgetter('name'))
print("%-30s %-10s %s" %('Image Name','Stars','Description'))
for tool in dsToolDict:
    if tool['name'] not in excludedImages:
        print("%-30s %-10s %s" %(tool['name'],tool['star_count'],tool['description']))
#print(dsToolDict[0]['name'])
##### End Method 1 #####

print("\nData Science tools detected:")
print("%-35s %-20s %s" %('Image','ID','Status'))
containers = client.containers.list(all=True)

runningTools = False
stoppedTools = False
lastRunningContainer = None
lastStoppedContainer = None
for i in containers:
    c = str(i).split(':')[1].rstrip(">").strip()
    attrs = client.containers.get(c).attrs
    # print("======================{}".format(attrs['State']))
    pattern = re.compile("^afcai2c/*")
    if pattern.match(attrs['Config']['Image']) and attrs['State']['Running'] :
        runningTools = True
        print("%-35s %-20s %s" %(attrs['Config']['Image'],attrs['Config']['Hostname'],attrs['State']['Running']))
        lastRunningContainer = attrs['Config']['Hostname']
    if pattern.match(attrs['Config']['Image']) and attrs['State']['Running'] == False :
        stoppedTools = True
        print("%-35s %-20s %s" %(attrs['Config']['Image'],attrs['Config']['Hostname'],attrs['State']['Running']))
        lastStoppedContainer = attrs['Config']['Hostname']

if runningTools:
    stopTool = bool(input("\nA running tool has been detected, do you want to stop it? [False] ") or False)
    if stopTool:
        message = "Enter the container ID: [{0}] ".format(lastRunningContainer)
        containerID = str(input(message) or lastRunningContainer)
        containerToStop = client.containers.get(containerID)
        containerToStop.stop()
        print('Attempting to stop the container.')
        quit()

if stoppedTools:
    startTool = bool(input("\nA stopped tool has been detected, do you want to restart it? [False] ") or False)
    if startTool:
        message = "Enter the container ID: [{0}] ".format(lastStoppedContainer)
        containerID = str(input(message) or lastStoppedContainer)
        containerToStop = client.containers.get(containerID)
        containerToStop.start()
        print('Attempting to restart the container.')
        quit()
    elif startTool == False:
        removeTool = bool(input("--- Do you want to remove the tool? [False] ") or False)
        if removeTool:
            message = "Enter the container ID: [{0}] ".format(lastStoppedContainer)
            containerID = str(input(message) or lastStoppedContainer)
            containerToStop = client.containers.get(containerID)
            containerToStop.remove()
            print('Attempting to remove the container.')
            quit()


if not runningTools and not stoppedTools:
        print("%-35s %-20s %s" %(None,None,None))


@click.command()   
@click.option(
    '--image', 
    prompt  = '\nEnter the desired data science tool to run.', 
    default = 'afcai2c/jlab-eda',
    help    = 'Make a selection - each tools has AI/ML packages installed specifically their respetive purposes.'
    )
@click.option(
    '--tag',
    prompt  = '\nRun the latest build or specify the tag.',
    default = 'latest',
    help    = 'The latest tag is normally your best option.'
    )
@click.option(
    '--port',
    prompt  = "\nList of the default tool ports: \
\n   JupyterLab     8888\
\n   R-Studio       8787\
\n   Dash           8050\
\n   R-Shiny        3838\
\n   Label Studio   8080\
\n   Metabase       3000\
\n   SuperSet       8088\
\n   nginx          8080\\8443\
\nEnter the port to bind:",
    default = 8888,
    help    = "The tool will be accessible within the browser at http://localhost:[PORT]"
    )

def startTool(image,tag,port):
    imageName = "{0}:{1}".format(image,tag)
    localhostHome = Path.home()
    dsToolsVolume = "{0}/dsTools".format(localhostHome)
    command = "mkdir -p {0}".format(dsToolsVolume)
    os.system(command)
    command = "chmod 777 {0}".format(dsToolsVolume)
    os.system(command)
    time.sleep(2)
    tool = client.containers.run(
        image  = imageName,
        ports  = {port:port},
        detach = True,
        volumes = {
            dsToolsVolume: {
                'bind': '/home/localhost/dsTools', 
                'mode': 'rw'
                },
            '/tmp': {
                'bind': '/home/localhost/tmp', 
                'mode': 'rw'}
            },
        working_dir = '/home'
        )
    launchUrl = "{0}:{1}".format(localhost,port)
    webbrowser.open(launchUrl)
    message = "\
\n[!] {0} will be hosted at: {1}\
\n\n[!] The following paths have been mounted within the tool:".format(image,launchUrl)
    print(message)
    print("    %-20s %-10s" %('localhost',"tool (" + image + ")"))
    print("    %-20s %-10s" %(localhostHome,"/home/localhost"))
    print("    %-20s %-10s" %("/tmp","/tmp/localhost"))

    return(tool)

startTool(image,tag,port)

if __name__ == '__main__':
    startTool()









# 'Id': 'fceb81301cb15dc9c80b2bd9b938cd43069de104360b7b0915f2e8efc002b6f8', 
# 'Created': '2022-07-20T03:44:56.4379156Z', 
# 'Path': 'bash', 
# 'Args': [], 
# 'State': {
#     'Status': 'exited', 
#     'Running': False, 
#     'Paused': False, 
#     'Restarting': False, 
#     'OOMKilled': False, 
#     'Dead': False, 
#     'Pid': 0, 
#     'ExitCode': 0, 
#     'Error': '', 
#     'StartedAt': '2022-07-20T03:44:56.8708248Z', 
#     'FinishedAt': '2022-07-20T03:44:56.9009506Z'}, 
# 'Image': 'sha256:27941809078cc9b2802deb2b0bb6feed6c236cde01e487f200e24653533701ee', 
# 'ResolvConfPath': '/var/lib/docker/containers/fceb81301cb15dc9c80b2bd9b938cd43069de104360b7b0915f2e8efc002b6f8/resolv.conf', 
# 'HostnamePath': '/var/lib/docker/containers/fceb81301cb15dc9c80b2bd9b938cd43069de104360b7b0915f2e8efc002b6f8/hostname', 
# 'HostsPath': '/var/lib/docker/containers/fceb81301cb15dc9c80b2bd9b938cd43069de104360b7b0915f2e8efc002b6f8/hosts', 
# 'LogPath': '/var/lib/docker/containers/fceb81301cb15dc9c80b2bd9b938cd43069de104360b7b0915f2e8efc002b6f8/fceb81301cb15dc9c80b2bd9b938cd43069de104360b7b0915f2e8efc002b6f8-json.log', 
# 'Name': '/blissful_banach', 
# 'RestartCount': 0, 
# 'Driver': 'overlay2', 
# 'Platform': 'linux', 
# 'MountLabel': '', 
# 'ProcessLabel': '', 
# 'AppArmorProfile': '', 
# 'ExecIDs': None, 
# 'HostConfig': {
#     'Binds': None, 
#     'ContainerIDFile': '', 
#     'LogConfig': {
#         'Type': 'json-file', 
#         'Config': {}}, 
#         'NetworkMode': 'default', 
#         'PortBindings': None, 
#         'RestartPolicy': {
#             'Name': '', 
#             'MaximumRetryCount': 0
#             }, 
#         'AutoRemove': False, 
#         'VolumeDriver': '', 
#         'VolumesFrom': None, 
#         'CapAdd': None, 
#         'CapDrop': None, 
#         'CgroupnsMode': 'host', 
#         'Dns': None, 
#         'DnsOptions': None, 
#         'DnsSearch': None, 
#         'ExtraHosts': None, 
#         'GroupAdd': None, 
#         'IpcMode': 'private', 
#         'Cgroup': '', 
#         'Links': None, 
#         'OomScoreAdj': 0, 
#         'PidMode': '', 
#         'Privileged': False, 
#         'PublishAllPorts': False, 
#         'ReadonlyRootfs': False, 
#         'SecurityOpt': None, 
#         'UTSMode': '', 
#         'UsernsMode': '', 
#         'ShmSize': 67108864, 
#         'Runtime': 'runc', 
#         'ConsoleSize': [0, 0], 
#         'Isolation': '', 
#         'CpuShares': 0, 
#         'Memory': 0, 
#         'NanoCpus': 0, 
#         'CgroupParent': '', 
#         'BlkioWeight': 0, 
#         'BlkioWeightDevice': None, 
#         'BlkioDeviceReadBps': None, 
#         'BlkioDeviceWriteBps': None, 
#         'BlkioDeviceReadIOps': None, 
#         'BlkioDeviceWriteIOps': None, 
#         'CpuPeriod': 0, 
#         'CpuQuota': 0, 
#         'CpuRealtimePeriod': 0, 
#         'CpuRealtimeRuntime': 0, 
#         'CpusetCpus': '', 
#         'CpusetMems': '', 
#         'Devices': None, 
#         'DeviceCgroupRules': None, 
#         'DeviceRequests': None, 
#         'KernelMemory': 0, 
#         'KernelMemoryTCP': 0, 
#         'MemoryReservation': 0, 
#         'MemorySwap': 0, 
#         'MemorySwappiness': None, 
#         'OomKillDisable': False, 
#         'PidsLimit': None, 
#         'Ulimits': None, 
#         'CpuCount': 0, 
#         'CpuPercent': 0, 
#         'IOMaximumIOps': 0, 
#         'IOMaximumBandwidth': 0, 
#         'MaskedPaths': ['/proc/asound', '/proc/acpi', '/proc/kcore', '/proc/keys', '/proc/latency_stats', '/proc/timer_list', '/proc/timer_stats', '/proc/sched_debug', '/proc/scsi', '/sys/firmware'], 
#         'ReadonlyPaths': ['/proc/bus', '/proc/fs', '/proc/irq', '/proc/sys', '/proc/sysrq-trigger']
#     }, 
#     'GraphDriver': {
#         'Data': {
#             'LowerDir': '/var/lib/docker/overlay2/9d3e9f912e3f4eedee056c05d94d48023a28a1b088c1214d4b1d4b8b245bd295-init/diff:/var/lib/docker/overlay2/3663b2437dd129e7680d800c11f0da1099ba44738bf72738f7cf15a10deb6682/diff', 
#             'MergedDir': '/var/lib/docker/overlay2/9d3e9f912e3f4eedee056c05d94d48023a28a1b088c1214d4b1d4b8b245bd295/merged', 
#             'UpperDir': '/var/lib/docker/overlay2/9d3e9f912e3f4eedee056c05d94d48023a28a1b088c1214d4b1d4b8b245bd295/diff', 
#             'WorkDir': '/var/lib/docker/overlay2/9d3e9f912e3f4eedee056c05d94d48023a28a1b088c1214d4b1d4b8b245bd295/work'
#         }, 
#         'Name': 'overlay2'
#     }, 
#     'Mounts': [], 
#     'Config': {
#         'Hostname': 'fceb81301cb1', 
#         'Domainname': '', 
#         'User': '', 
#         'AttachStdin': False, 
#         'AttachStdout': True, 
#         'AttachStderr': True, 
#         'Tty': False, 
#         'OpenStdin': False, 
#         'StdinOnce': False, 
#         'Env': ['PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'], 
#         'Cmd': ['bash'], 
#         'Image': 'ubuntu', 
#         'Volumes': None, 
#         'WorkingDir': '', 
#         'Entrypoint': None, 
#         'OnBuild': None, 
#         'Labels': {
#             'desktop.docker.io/wsl-distro': 'Ubuntu'
#         }
#     }, 
#     'NetworkSettings': {
#         'Bridge': '', 
#         'SandboxID': '0f2710c5456e89654e3ffe46503e57762ebdea9c37c2a55a86e6488bdcc49301', 
#         'HairpinMode': False, 
#         'LinkLocalIPv6Address': '', 
#         'LinkLocalIPv6PrefixLen': 0, 
#         'Ports': {}, 
#         'SandboxKey': '/var/run/docker/netns/0f2710c5456e', 
#         'SecondaryIPAddresses': None, 
#         'SecondaryIPv6Addresses': None, 
#         'EndpointID': '', 
#         'Gateway': '', 
#         'GlobalIPv6Address': '', 
#         'GlobalIPv6PrefixLen': 0, 
#         'IPAddress': '', 
#         'IPPrefixLen': 0, 
#         'IPv6Gateway': '', 
#         'MacAddress': '', 
#         'Networks': {
#             'bridge': {
#                 'IPAMConfig': None, 
#                 'Links': None, 
#                 'Aliases': None, 
#                 'NetworkID': 'd12fbd448db6e8e677a350763341ae48497981288beeaa7947d5abc80032a067', 
#                 'EndpointID': '', 
#                 'Gateway': '', 
#                 'IPAddress': '', 
#                 'IPPrefixLen': 0, 
#                 'IPv6Gateway': '', 
#                 'GlobalIPv6Address': '', 
#                 'GlobalIPv6PrefixLen': 0, 
#                 'MacAddress': '', 
#                 'DriverOpts': None
#             }
#         }
#     }
# }
