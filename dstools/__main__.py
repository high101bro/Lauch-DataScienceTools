import sys
import click
import six
from pyfiglet import figlet_format
from termcolor import colored
import docker
from dstools.launcher import launch_tool


def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)

@click.group()
@click.version_option("0.1.0")
def main():
    """
    A Data Science Tool Launcher CLI
    """
    log("Data Science Tools!", color="blue", figlet=True)
    log("Welcome to the Data Science Tools CLI", "green")
    try:
        client = docker.from_env()
    except:
        log("Docker is not installed! Visit https://docs.docker.com/get-docker/",color="red")

@main.command()
@click.argument('keyword', required=False)
def menu(**kwargs):
    """Select from a menu of tools"""
    

@main.command()
@click.argument('name', required=False)
def id(**kwargs):
    """Launch a tool if you know the ID"""
    pass


if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("Data Science Tools!")
    main()

