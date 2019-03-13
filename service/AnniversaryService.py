import json
import logging
import mysql.connector
from util.Global import gloVar

def getByDate(date):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT time,content FROM anniversary where time='{}'".format(date)
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    fields = cursor.description
    db.commit()
    db.close()
    return changeToJsonStr(fields, data)

def getAllAnniversary():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT time,content FROM anniversary order by dateTime desc"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    fields = cursor.description
    db.commit()
    db.close()
    return changeToJsonStr(fields, data)

def getAllAnniversaryTime():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT time from anniversary order by datetime desc"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return json.dumps(data)

def insert(time,content,dateTime):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "insert into anniversary(time,content,dateTime) VALUES ('{}','{}','{}')"\
        .format(time,content,dateTime)
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    db.commit()
    db.close()

def updateByTime(time,content,dateTime):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "update anniversary set content='{}',dateTime='{}' where time='{}'"\
        .format(content,dateTime,time)
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    db.commit()
    db.close()

def changeOneToJsonStr(fields,data):
    finalResult = ""
    column_list = []
    for i in fields:
        column_list.append(i[0])
    for row in data:
        result = {}
        for i in range(0, len(column_list)):
            result[column_list[i]] = str(row[i])
        finalResult = str(json.dumps(result, ensure_ascii=False))
        break
    return finalResult


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

    if finalResult == "[":
        finalResult = finalResult + "]"
    else:
        finalResult = finalResult[0:-1] + "]"
    return finalResult