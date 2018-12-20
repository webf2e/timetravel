import os
import time


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


def kill(pid):
    # 返回0，成功，其他失败
    if isStarted():
        return os.system("kill -9 {}".format(pid))
    return "NOT_STARTED"


def start():
    if not isStarted():
        return os.system("sh /root/python_proj/timetravel/run.sh")
    return "ALREADY_STARTED"


def restart():
    shell = "sh /root/python_proj/timetravel/restart.sh {} &".format(getPid())
    print(shell)
    return os.system(shell)


def isStarted():
    if getPid() == None:
        return False
    return True