from util import FileUtil
from util.Global import gloVar
import psutil
import datetime
import time

def moveChatFileJob():
    print("转移聊天记录文件开始")
    FileUtil.renameAndMove(gloVar().chatDirPath)
    print("转移聊天记录文件结束")

def makeBigHeartJob():
    FileUtil.makeHeartImg()

def systemTongjiJob():
    #获取时间
    t = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
    hour = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d-%H")
    memory = psutil.virtual_memory().percent
    FileUtil.writeSystemTongji("memory",hour,"{}\t{}".format(t,memory))
    disk = psutil.disk_usage("/").percent
    FileUtil.writeSystemTongji("disk", hour, "{}\t{}".format(t, disk))
    cpu = psutil.cpu_percent(0)
    FileUtil.writeSystemTongji("cpu", hour, "{}\t{}".format(t, cpu))

    lastData = {}
    key_info = psutil.net_io_counters(pernic=True).keys()
    for key in key_info:
        if str(key).startswith("eth"):
            recv = psutil.net_io_counters(pernic=True).get(key).bytes_recv
            sent = psutil.net_io_counters(pernic=True).get(key).bytes_sent
            lastData[key] = (recv,sent)
    time.sleep(1)
    for key in key_info:
        if str(key).startswith("eth"):
            recv = psutil.net_io_counters(pernic=True).get(key).bytes_recv - lastData[key][0]
            sent = psutil.net_io_counters(pernic=True).get(key).bytes_sent - lastData[key][1]
            FileUtil.writeSystemTongji("{}-{}".format("net",key), hour, "{}\t{}\t{}".format(t, recv, sent))

def removeSystemFileJob():
    FileUtil.removeSystemTongjiFile(240)