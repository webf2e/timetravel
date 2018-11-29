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

def getNotFinished():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT * FROM chat where isFinish = 0"
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data

def updateById(voiceTime, content, voiceCount, wordLength, times, id):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "update chat set voiceTime = {},content='{}',voiceCount={},wordLength={},times='{}',isFinish=1 where id={}"\
        .format(voiceTime, content, voiceCount, wordLength, times, id)
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    db.commit()
    db.close()

def getChatSumTongji():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT sum(voiceTime) as voiceTime, sum(voiceCount) as voiceCount, sum(wordLength) as wordLength FROM chat where isFinish = 1"
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    fields = cursor.description
    db.commit()
    db.close()
    return changeToJsonStr(fields, data)

def getChatTimes():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT times FROM chat where times != '' and times is not null"
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data


def changeToJsonStr(fields,data):
    finalResult = "["
    column_list = []
    for i in fields:
        column_list.append(i[0])
    for row in data:
        result = {}
        for i in range(0, len(column_list)):
            result[column_list[i]] = str(row[i])
        finalResult += str(json.dumps(result, ensure_ascii=False)) + ","

    finalResult = finalResult[0:-1] + "]"
    return finalResult
###########################分割############################

def operateChatMessage():
    datas = getNotFinished()
    print("chat表中有{}数据没有处理".format(len(datas)))
    for data in datas:
        try:
            # 解析每一张
            # print(data[1])
            id = data[0]
            jsonData = json.loads(data[3].replace("\"\"", "\"'").replace("\"撤回", "'撤回"))
            times = set()
            lastHeight = 0
            lastTop = 0
            totalWord = ""
            voiceCount = 0
            voiceTime = 0
            for wl in (jsonData["words_result"]):
                # 解析每一行
                top = wl["location"]["top"]
                height = wl["location"]["height"]
                word = str(wl["words"]).strip()
                # 去掉头部
                if top < 240:
                    lastHeight = height
                    lastTop = top
                    continue
                # 过滤
                if not isVaild(word):
                    lastHeight = height
                    lastTop = top
                    continue
                # 解析时间
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
                # 判断是否是一行
                if int(top) - (int(lastTop) + int(lastHeight)) > 50:
                    totalWord += "\n"
                totalWord += word
                lastHeight = height
                lastTop = top
            totalWord = totalWord.replace("'", "\"")
            updateById(voiceTime, totalWord, voiceCount, len(totalWord), changeSetTimeToStr(times), id)
        except Exception as e:
            print("处理chat数据报错：{}".format(str(e)))

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