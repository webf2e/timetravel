from util import FileUtil,OcrUtil,SmsUtil,PushUtil
from util.Global import gloVar
from service import ChatService,RedisService
import psutil
import datetime
import time
import os
import json

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

def removeFileJob():
    FileUtil.removeSystemTongjiFile(240)
    FileUtil.removeLocationFile(240)

def getChatMessageFromChatImg():
    #todo 后期该值需要调小
    maxDay = 100
    isOverLimit = False
    for i in range(0,maxDay):
        t = datetime.datetime.now() - datetime.timedelta(days=i)
        year = t.year
        month = t.month
        if (month < 10):
            month = "0" + str(month)
        day = t.day
        if (day < 10):
            day = "0" + str(day)
        dirPath = str(os.path.join(str(gloVar.chatDirPath), str(year), str(month), str(day)))
        if os.path.exists(dirPath) and os.path.isdir(dirPath):
            imgPath = dirPath.split("static")[1]
            imgs = os.listdir(dirPath)
            imgs.sort()
            for img in imgs:
                if img.startswith("20"):
                    absImgPath = os.path.join(dirPath,img)
                    data = ChatService.getByImgName(img)
                    if len(data) == 0:
                        #没有数据，需要添加到mysql，调用百度ocr获取数据
                        result = OcrUtil.getContent(absImgPath)
                        if result == "":
                            print("超过限额，退出")
                            isOverLimit = True
                            break
                        result = str(result).replace("'","\"")
                        ChatService.insert(img, imgPath, result, str(datetime.datetime.now()))
                        time.sleep(5)
        if isOverLimit:
            break
    print("开始处理chat表中的数据")
    ChatService.operateChatMessage()
    print("转化聊天图片成文字结束")

def checkLastLocationJob():
    jsonStr = FileUtil.getLastLocationInFile()
    jsonData = json.loads(json.dumps(eval(jsonStr)))
    lastLocationTime = jsonData["timestramp"] // 1000
    currentTime = int(datetime.datetime.now().timestamp())
    if currentTime - lastLocationTime > 60:
        if not RedisService.isExist("LocationNotUpdatePush"):
            RedisService.setWithTtl("LocationNotUpdatePush","1",300)
            PushUtil.pushToSingle("末次位置未更新","末次位置已经超过1分钟未更新","")
    if currentTime - lastLocationTime > 3 * 60:
        if not RedisService.isExist("LocationNotUpdateSms"):
            RedisService.setWithTtl("LocationNotUpdateSms", "1", 600)
            SmsUtil.sendSmsBytempId("15210650960",121042)