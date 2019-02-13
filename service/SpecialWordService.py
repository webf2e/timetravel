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
    sql = "SELECT time,word,themeColor,festival FROM specialWord where time='{}'".format(date)
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    fields = cursor.description
    db.commit()
    db.close()
    return changeOneToJsonStr(fields, data)

def getAllByBelowDate(date):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT time,word,themeColor,festival FROM specialWord where datetime <= '{}' order by datetime desc".format(date)
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    fields = cursor.description
    db.commit()
    db.close()
    return changeToJsonStr(fields, data)

def getAllSpecialDayTime():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT time from specialWord order by datetime desc"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return json.dumps(data)

def insert(time,word,themeColor,festival,dateTime):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "insert into specialWord(time,word,themeColor,festival,dateTime) VALUES ('{}','{}','{}','{}','{}')"\
        .format(time,word,themeColor,festival,dateTime)
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    db.commit()
    db.close()

def updateByTime(time,word,themeColor,festival,dateTime):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "update specialWord set word='{}',themeColor='{}',festival='{}',dateTime='{}' where time='{}'"\
        .format(word,themeColor,festival,dateTime,time)
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

    finalResult = finalResult[0:-1] + "]"
    return finalResult