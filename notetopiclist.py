#!/usr/bin/python
import os
from sys import argv
from notelib import createTitle, dirname

if len(argv) > 2:
    query = argv[2]
else:
    query = ""

flog = open("/tmp/somelog.txt", "w")
flog.write(query)
flog.write("\n")

for f in os.listdir(dirname):
    if len(f) >= len(query) and query.lower()[0:len(query)] == f.lower()[0:len(query)] and not f[0] == "." and not f[-1] == "~":
        print f
    content = open(dirname + "/" + f).read()
    lastTitle = dict()
    for line in content.split("\n"):
        if len(line) > 0 and line[0] == "#":
            title = createTitle(line, lastTitle)
            flog.write(title + "\n")
            flog.write(query.lower()[0:len(query)] + " == " + title.lower()[0:len(query)] + "\n")
            if len(title) >= len(query) and query.lower()[0:len(query)] == title.lower()[0:len(query)]:
                print title
flog.close()