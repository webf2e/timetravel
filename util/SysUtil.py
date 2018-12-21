import os
import requests

url = "http://127.0.0.1:5000/server/{}"
def getPid():
    output = os.popen('ps -ef | grep uwsgiconfig.ini')
    lines = output.read().split("\n")
    pid = None
    for line in lines:
        ls = line.split()
        if len(ls) < 3:
            continue
        if ls[2] == "1":
            pid = ls[1]
            break
    return pid


def kill():
    # 返回0，成功，其他失败
    if isStarted():
        return requests.post(url.format("stopServer"))
    return "NOT_STARTED"


def start():
    if not isStarted():
        return requests.post(url.format("startServer"))
    return "ALREADY_STARTED"


def restart():
    return requests.post(url.format("restartServer"))


def isStarted():
    if getPid() == None:
        return False
    return True