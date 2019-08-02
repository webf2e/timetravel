from util import FileUtil,OcrUtil,SmsUtil,PushUtil,TongjiUtil,TimeUtil
from util.Global import gloVar
from util.RedisKey import redisKey
from service import ChatService,RedisService,TravelService,SpecialDayService,MessageService,SettingService
import psutil
import datetime
import time
import os
import json
import logging,shutil

def moveChatFileJob():
    if RedisService.isExist(redisKey.moveChatImgFlag):
        logging.warning("转移聊天记录文件开始")
        FileUtil.renameAndMove(gloVar().chatDirPath)
        logging.warning("转移聊天记录文件结束")

def makeBigHeartJob():
    logging.warning("开始制作首页心形图片")
    FileUtil.makeHeartImg()
    logging.warning("制作首页心形图片结束")

def systemTongjiJob():
    #获取时间
    t = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
    hour = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d-%H")
    memory = psutil.virtual_memory().percent
    FileUtil.writeSystemTongji("memory",hour,"{}\t{}".format(t,memory))
    disk = psutil.disk_usage("/").percent
    #添加磁盘容量报警
    if disk > 80:
        #判断是否需要报警
        if not RedisService.isExist(redisKey.diskAlarm):
            #需要报警
            PushUtil.pushToSingle("磁盘空间报警","当前磁盘使用率已经大于80%，请登录服务器查看","")
            RedisService.setWithTtl(redisKey.diskAlarm,"1", 60 * 60 * 6)
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
    maxDay = 10
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
                            logging.warning("超过限额，退出")
                            isOverLimit = True
                            break
                        result = str(result).replace("'","\"")
                        ChatService.insert(img, imgPath, result, str(datetime.datetime.now()))
                        time.sleep(5)
        if isOverLimit:
            break
    logging.warning("开始处理chat表中的数据")
    ChatService.operateChatMessage()
    logging.warning("转化聊天图片成文字结束")

def checkLastLocationJob():
    jsonStr = RedisService.get(redisKey.lastLocation)
    if None == jsonStr:
        return
    jsonData = json.loads(json.dumps(eval(jsonStr)))
    lastLocationTime = jsonData["timestramp"] // 1000
    currentTime = int(datetime.datetime.now().timestamp())
    logging.warning("最后末次位置的时间差：{}".format(currentTime - lastLocationTime))
    if RedisService.getSetting(redisKey.isNeedLocationNotUpdateForAppNotify) == "1":
        if currentTime - lastLocationTime > 120:
            if not RedisService.isExist(redisKey.locationNotUpdatePush):
                RedisService.setWithTtl(redisKey.locationNotUpdatePush,"1",300)
                PushUtil.pushToSingle("末次位置未更新","末次位置已经超过两分钟未更新","")

    if RedisService.getSetting(redisKey.isNeedLocationNotUpdateForSmsNotify) == "1":
        if currentTime - lastLocationTime > 5 * 60:
            if not RedisService.isExist(redisKey.locationNotUpdateSms):
                RedisService.setWithTtl(redisKey.locationNotUpdateSms, "1", 600)
                SmsUtil.sendSmsBytempId("15210650960",121042)

def locationTongjiJob():
    TongjiUtil.locationTongji()

def setFenceNotifySlienceJob():
    RedisService.setWithTtl(redisKey.fenceNotifySlience, "1", 60 * 60 * 7)

def splitLogJob():
    time = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(hours=1),"%Y%m%d")
    newLogFilePath = gloVar.loggingFilePath.replace(".log","-{}.log".format(time))
    #复制文件
    shutil.copyfile(gloVar.loggingFilePath,newLogFilePath)
    #清空文件
    f = open(gloVar.loggingFilePath, "w+")
    f.truncate()
    f.close()
    #清除过期文件
    parentDir = gloVar.loggingFilePath[:gloVar.loggingFilePath.rfind("/")]
    files = os.listdir(parentDir)
    oldLogFiles = []
    for file in files:
        if file.startswith("timeTravel-"):
            oldLogFiles.append(os.path.join(parentDir, file))
    while len(oldLogFiles) > 30:
        oldLogFiles.sort()
        logging.warning("删除文件：{}".format(oldLogFiles[0]))
        os.remove(oldLogFiles[0])
        oldLogFiles.remove(oldLogFiles[0])

def delOtherLogJob():
    logDir = gloVar.loggingFilePath[:gloVar.loggingFilePath.rfind("/")]
    files = os.listdir(logDir)
    for file in files:
        if not file.startswith("timeTravel"):
            f = open(os.path.join(logDir,file), "w+")
            f.truncate()
            f.close()

def makeSpecialDayJob():
    logging.warning("开始生成首页滚动字幕和dailycolor.css文件")
    color = "f1a693"
    specialHead = ""
    now = datetime.datetime.now()
    ymd = datetime.datetime.strftime(now, "%Y-%m-%d")
    message = MessageService.getLastestMessage()[0][1]
    redisKey = "special_{}".format(ymd)
    monthDay = datetime.datetime.strftime(now, "%m%d")
    specialDays = SpecialDayService.selectByMonthDay(monthDay)
    if len(specialDays) == 0:
        data = TimeUtil.getJuHeCalendar(ymd)
        if None != data:
            lunar = data["lunar"]
            specialDays = SpecialDayService.selectByMonthDay(lunar)
            if len(specialDays) == 0:
                logging.warning("{}不是特殊节日".format(ymd))
            else:
                # 农历判断
                (specialHead, color) = dealSpecialDaysFromDB(specialDays, now)
    else:
        # 阳历判断
        (specialHead, color) = dealSpecialDaysFromDB(specialDays, now)
    result = {}
    result["specialHead"] = specialHead
    result["message"] = message
    result["color"] = color
    RedisService.setWithTtl(redisKey, json.dumps(result), 60 * 60 * 25)
    #将文件写入dailycolor.css
    tempFilePath = os.path.join(gloVar.staticPath,"css/temp/dailycolor.tmp")
    cssContent = ""
    lines = open(tempFilePath, "r+")
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if line.find("[color]") != -1:
            line = line.replace("[color]",color)
        cssContent += line + "\n"
    lines.close()
    dailycolorFilePath = os.path.join(gloVar.staticPath,"css/dailycolor.css")
    dailycolorFile = open(dailycolorFilePath,"w+")
    dailycolorFile.write(cssContent)
    dailycolorFile.close()
    #
    specialDaysRemain = SpecialDayService.getRemainDaysFoSpecialDay(5)
    if len(specialDaysRemain) > 0:
        for specialDayRemain in specialDaysRemain:
            if specialDayRemain[3] == None or "" == specialDayRemain[3]:
                # 没有年
                specialInfo = "{}".format(specialDayRemain[2])
            else:
                delay = str(now.year - int(specialDayRemain[3]))
                specialInfo = "{}".format(specialDayRemain[2].replace("X", delay))

            if specialDayRemain[4] == 0:
                PushUtil.pushToSingle("特殊节日通知","今天是{}".format(specialInfo),"")
            else:
                PushUtil.pushToSingle("特殊节日通知", "距离{}还有{}天".format(specialInfo,specialDayRemain[4]), "")
    logging.warning("生成首页滚动字幕和dailycolor.css文件结束")

def dealSpecialDaysFromDB(specialDays, now):
    sd = specialDays[0]
    color = sd[1]
    if sd[3] == None or "" == sd[3]:
        # 没有年
        specialHead = "【{}】".format(sd[2])
    else:
        delay = str(now.year - int(sd[3]))
        specialHead = "【{}】".format(sd[2].replace("X", delay))
    return (specialHead,color)

def serviceCheckJob():
    r = SettingService.getServiceStatus(False)
    errorItem = ""
    for item,status in r.items():
        if item == "checkTime":
            continue
        if status != 1:
            errorItem += item+","
    errorItem = errorItem[:-1]
    if errorItem != "":
        PushUtil.pushToSingle("服务有异常",errorItem,"")

