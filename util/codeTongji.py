import os,json

path = "/home/liuwenbin/PycharmProjects/timetravel"

tongjiMap = {}
tongjiMap["frontEnd"] = 0
tongjiMap["backEnd"] = 0

def getLineCount(path):
    lines = open(path,"r+")
    totalCount = 0
    for line in lines:
        line = line.strip()
        if "" == line:
            continue
        totalCount += 1
    lines.close()
    return totalCount

def getFile(path):
    if os.path.isfile(path):
        if path.endswith(".py"):
            tongjiMap["backEnd"] = tongjiMap["backEnd"] + getLineCount(path)
        elif path.endswith(".html") or path.endswith(".css") or path.endswith(".js"):
            tongjiMap["frontEnd"] = tongjiMap["frontEnd"] + getLineCount(path)
    else:
        files = os.listdir(path)
        for file in files:
            getFile(os.path.join(path,file))