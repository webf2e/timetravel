import json
import os
import mysql.connector
from util.Global import gloVar

def getByImgName(imgName):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT * FROM chat where imgName='{}'".format(imgName)
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data

def insert(imgName, imgPath, result, createTime):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "insert into chat(imgName,imgPath,result,createTime) VALUES ('{}','{}','{}','{}')"\
        .format(imgName, imgPath, result, createTime)
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    db.commit()
    db.close()

def getAllData():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT * FROM chat"
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data

def operateChatMessage():
    gloVar.dbHost = "localhost"
    gloVar.dbUser = "root"
    gloVar.dbPwd = "123456"
    gloVar.dbName = "timetravel"
    datas = getAllData()
    a = 0
    for data in datas:
        #解析每一张
        #print(data[1])
        id = data[0]
        jsonData = json.loads(data[3].replace("\"\"","\"'").replace("\"撤回","'撤回"))
        times = set()
        lastHeight = 0
        lastTop = 0
        totalWord = ""
        voiceCount = 0
        voiceTime = 0
        for wl in (jsonData["words_result"]):
            #解析每一行
            top = wl["location"]["top"]
            left = wl["location"]["left"]
            width = wl["location"]["width"]
            height = wl["location"]["height"]
            word = str(wl["words"]).strip()
            #去掉头部
            if top < 240:
                lastHeight = height
                lastTop = top
                continue
            #过滤
            if not isVaild(word):
                lastHeight = height
                lastTop = top
                continue
            #解析时间
            if len(word) == 5 and word[2] == ":":
                times.add(getHourTime(word))
                lastHeight = height
                lastTop = top
                continue

            if word.startswith("昨天") and len(word) == 7 and word[4] == ":":
                times.add(getHourTime(word[2:]))
                lastHeight = height
                lastTop = top
                continue

            if word.startswith("聊天时长"):
                voiceTime += getVoiceTime(word)
                voiceCount += 1
                continue
            #判断是否是一行
            #print("word:{},loc:{}".format(word,(int(top) - (int(lastTop) + int(lastHeight)))))
            if int(top) - (int(lastTop) + int(lastHeight)) > 50:
                totalWord += "\n"
            totalWord += word;
            lastHeight = height
            lastTop = top
        print("*****************************")
        print(totalWord)
        print("voiceTime:{}".format(voiceTime))
        print("voiceCount:{}".format(voiceCount))
        print("times:{}".format(changeSetTimeToStr(times)))
        print("wordLength:{}".format(len(totalWord)))
        a += len(totalWord)
        print("-----------------------------")
        #updateById
    print(a)

def getHourTime(time):
    return time[0:3] + "00"

def changeSetTimeToStr(time):
    result = ""
    for t in time:
        result += t + ","
    return result[0:-1]

def getVoiceTime(word):
    voiceTime = word.replace("聊天时长","")
    voiceTimes = voiceTime.split(":")
    return int(voiceTimes[0]) * 60 + int(voiceTimes[1])

def isVaild(word):
    if word.isdigit():
        return False
    elif word == "对方无应答":
        return False
    elif word == "对方已取消":
        return False
    elif word.find("撤回了一条消息") != -1:
        return False
    elif word == "连接失败":
        return False
    elif word == "对方忙线中":
        return False
    elif word == "+":
        return False
    elif word == "已取消":
        return False
    return True

operateChatMessage()