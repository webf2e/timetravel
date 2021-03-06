from util.Global import gloVar
import json
import datetime
import mysql.connector

def getRandomQuestions():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    cursor.execute("SELECT id,question FROM question ORDER BY RAND() LIMIT 3")
    data = cursor.fetchall()
    fields = cursor.description
    db.commit()
    db.close()
    return changeToJsonStr(fields,data)

def getAnswerByIds(ids):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    cursor.execute("SELECT id,answer,question FROM question where id in ({})".format(ids))
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data

def updateErrorQuestion(id):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "update question set errorTimes = errorTimes + 1,useTimes = useTimes + 1,lastUseTime='{}' where id={}".format(datetime.datetime.now(),id)
    cursor.execute(sql)
    db.commit()
    db.close()

def updateCorrectQuestion(id):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "update question set correctTimes = correctTimes + 1,useTimes = useTimes + 1,lastUseTime='{}' where id={}".format(datetime.datetime.now(),id)
    cursor.execute(sql)
    db.commit()
    db.close()

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