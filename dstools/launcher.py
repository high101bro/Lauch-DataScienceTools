#!/usr/bin/env python3
from sys import float_repr_style
import docker, click, webbrowser, requests, json, time, re

# Placeholders
localhost = 'http://localhost'
image = None
tag = None
port = None
start = None
stop_tool = None

client = docker.from_env()

# Queries Docker Hub for Data Science Tools
url = "https://hub.docker.com/v2/repositories/afcai2c"
dsToolsByte = requests.get(url).content
dsToolsStr  = dsToolsByte.decode()
dsToolsDict = json.loads(dsToolsStr)
dsToolsList = dsToolsDict['results']

# This list contains images to exclude from being displayed
excludedImages = ['afcai2c/python36','afcai2c/python36-ai','afcai2c/python38','afcai2c/python38-ai']

#print(dsToolsList[0])

# Prints out the images available to run
print("{0:30}{1:30}{2:65}".format('Image Name','Last Updated','Pull Count'))
for tool in dsToolsList:
    imageName = "{0}/{1}".format(tool['namespace'],tool['name'])
    #print(imageName)
    imageInfo = "{0:30}{1:30}{2:10}".format(imageName,tool['last_updated'],tool['pull_count'])
    if imageName not in excludedImages:
        print(imageInfo)

print("\nRunning data science tools:")
print("{0:30}{1:30}".format('   Image','   ID'))
containers = client.containers.list(all=True)

runningTools = False
lastContainer = None
for i in containers:
    c = str(i).split(':')[1].rstrip(">").strip()
    attrs = client.containers.get(c).attrs
    
    pattern = re.compile("^afcai2c/*")
    if pattern.match(attrs['Config']['Image']) and attrs['State']['Running'] :
        runningTools = True
        print
        print("   {0:30}{1:30}".format(attrs['Config']['Image'],attrs['Config']['Hostname']))
        lastContainer = attrs['Config']['Hostname']

if runningTools == False:
    print("   {0:30}{1:30}".format('None','None'))
else:
    stopTool = bool(input("\nA tool is already running, do you want to stop it? [False] ") or False)
    if stopTool:
        message = "Enter the container ID: [{0}] ".format(lastContainer)
        containerID = str(input(message) or lastContainer)
        containerToStop = client.containers.get(containerID)
        containerToStop.stop()
        quit()


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
\n   JupyterLab    = 8888\
\n   R-Studio      = 8787\
\n   Dash          = 8050\
\n   R-Shiny       = 3838\
\n   Label Studio  = 8080\
\nEnter the port to bind:",
    default = 8888,
    help    = "The tool will be accessible within the browser at http://localhost:[PORT]"
    )

def startTool(image,tag,port):
    imageName = "{0}:{1}".format(image,tag)
    tool = client.containers.run(
        image  = imageName,
        ports  = {port:port},
        detach = True        )
    launchUrl = "{0}:{1}".format(localhost,port)
    webbrowser.open(launchUrl)
    message = "\n{0} will be hosted at: http://localhost:{1}".format(image,port)
    print(message)
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
