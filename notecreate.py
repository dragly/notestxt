#!/usr/bin/python
from datetime import date
from sys import argv
import os
import subprocess
import re
from notelib import createTitle, dirname


filename=dirname + "/" + date.today().strftime("%Y-%m-%d.mkd")
notefiles=os.listdir(dirname)

if len(argv) < 2:
    print "Needs an argument"
    exit()

#    NUMARG=$#
#    OFFARG=${@:2:$NUMARG}
if argv[1] == "a" or argv[1] == "add":
    if len(argv) < 3:
        subprocess.call(["vim", "+", filename])
    else:
        f = open(filename, "a")
        title = ""
        for word in argv[2:]:
            title += word + " "
        f.write("\n# " + title + "#\n\n\n")
        f.close()
        subprocess.call(["vim", "+", filename])
    
if argv[1] == "ls":
    if len(argv) < 3:
        titles = []
        for f in os.listdir(dirname):
            lastTitle = dict()
            content = open(dirname + "/" + f).read()
            for line in content.split("\n"):
                if len(line) > 0 and line[0] == "#":
                    title = createTitle(line, lastTitle)
                    titles.append(title)
        titles.sort()
        for title in titles:
            print title
    else:
        searchPhrase = ""
        firstWord = True
        for word in argv[2:]:
            if not firstWord:
                searchPhrase += " "
            searchPhrase += word
            firstWord = False

        for f in os.listdir(dirname):
            lastTitle = dict()
            content = open(dirname + "/" + f).read()
            for line in content.split("\n"):
                title = createTitle(line, lastTitle)
                if searchPhrase.lower() in line.lower():
                    pattern = re.compile("(" + searchPhrase + ")", re.IGNORECASE)
                    #print f.replace(".mkd", "") + ": \033[1;32m" + title + "\033[0m" + ": " + pattern.sub("\033[1;31m\\1\033[0m", line)
                    print "\033[1;32m" + title + "\033[0m" + ": " + pattern.sub("\033[1;31m\\1\033[0m", line)
#    if [ "ls" == "$1" ]
#    then
#        if test "$2"
#        then
#            grep -i -n --color=auto "$OFFARG" $DIRNAME/*
#        else
#            vim $DIRNAME
#        fi
#    fi

if argv[1] == "e" or argv[1] == "edit":
    if len(argv) < 3:
        print "Needs a title"
        exit()
    
    searchPhrase = argv[2]
    matchingFiles = []
    matchingLines = []
    matchingLineNums = []
    for f in os.listdir(dirname):
        lastTitle = dict()
        fileNameA = dirname + "/" + f
        content = open(fileNameA).read()
        lines = content.split("\n")
        # If the file name matches
        if searchPhrase.replace("_", "").lower() in f.lower():
            matchingFiles.append(f)
            matchingLineSet = []
            for j in range(0, 4):
                if len(lines) > j:
                    matchingLineSet.append(lines[j])
            matchingLines.append(matchingLineSet)
            matchingLineNums.append(1)
        # Search for matching lines
        for i in range(len(lines)):
            line = lines[i]
            if len(line) > 0 and line[0] == "#":
                title = createTitle(line, lastTitle)
                if searchPhrase.lower() == title.lower():
                    matchingFiles.append(f)
                    matchingLineSet = []
                    for j in range(i, i+4):
                        if len(lines) > j and not lines[j] == "":
                            matchingLineSet.append(lines[j])
                    matchingLines.append(matchingLineSet)
                    matchingLineNums.append(i+1)
                    
    if len(matchingFiles) < 1:
        print "Title not found"
        exit()
    
    elif len(matchingFiles) == 1:
        #print "Found file", matchingFiles[0]
        subprocess.call(["vim", "+:" + str(matchingLineNums[0]), dirname + "/" + matchingFiles[0]])
    
    else:
        print "\033[1;33m" + "Found multiple possibilities:" + "\033[0m" 
        for i in range(len(matchingLines)):
            print "\033[1;32m" + str(i+1) + ": \033[1;30m"+ matchingFiles[i].replace(".mkd", "") + ":" + str(matchingLineNums[i]) + "\033[0m" 
            for line in matchingLines[i]:
                print line
        print "\n"
        try:
            choice=input("\033[1;33m" + 'Please make a selection [1-' + str(len(matchingLines)) + ']: ' + "\033[0m")
            choice = int(choice) - 1
        except KeyboardInterrupt:
            print ""
            exit()            
        subprocess.call(["vim", "+:" + str(matchingLineNums[choice]), dirname + "/" + matchingFiles[choice]])
            #vim $DIRNAME/$2
            #vim + $FILENAME
