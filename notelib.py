from os.path import expanduser
from ConfigParser import ConfigParser
import os

def createTitle(line, lastTitle):
    if len(line) > 0 and line[0:3] == "###":
        lastTitle[2] = line.replace("# ", "").replace(" #", "").replace("#", "").replace(" ", "_")
    elif len(line) > 0 and line[0:2] == "##":
        lastTitle[1] = line.replace("# ", "").replace(" #", "").replace("#", "").replace(" ", "_")
        if lastTitle.has_key(2):
            lastTitle.pop(2)
    elif len(line) > 0 and line[0] == "#":
        lastTitle[0] = line.replace("# ", "").replace(" #", "").replace("#", "").replace(" ", "_")
        if lastTitle.has_key(1):
            lastTitle.pop(1)
        if lastTitle.has_key(2):
            lastTitle.pop(2)
    title = ""
    if lastTitle.has_key(0):
        title += lastTitle[0]
    if lastTitle.has_key(1):
        title += "/" + lastTitle[1]
    if lastTitle.has_key(2):
        title += "/" + lastTitle[2]
    return title
    

homeDir = expanduser("~")
configDir = homeDir + "/.config/notestxt"
configFile = configDir + "/config.ini"

dirname=homeDir + "/notes"

if os.path.exists(configFile):
    configParser = ConfigParser()
    configParser.read(configFile)
    if configParser.has_section("General"):
        if configParser.has_option("General", "notesdir"):
            dirname=configParser.get("General", "notesdir")

if not os.path.exists(dirname):
    os.makedirs(dirname)