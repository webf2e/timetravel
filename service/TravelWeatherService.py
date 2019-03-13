import json,logging
import mysql.connector
from util.Global import gloVar

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


def insert(dayIcon,nightIcon,dayWeather,nightWeather,maxTemp,minTemp,travelId):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "insert into travelWeather(dayIcon,nightIcon,dayWeather,nightWeather,maxTemp,minTemp,travelId) VALUES ('{}','{}','{}','{}',{},{},{})"\
        .format(dayIcon,nightIcon,dayWeather,nightWeather,maxTemp,minTemp,travelId)
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    db.commit()
    db.close()

def update(dayIcon,nightIcon,dayWeather,nightWeather,maxTemp,minTemp,travelId):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "update travelWeather set dayIcon = '{}',nightIcon = '{}',dayWeather='{}',nightWeather='{}',maxTemp={},minTemp={} where travelId={}"\
        .format(dayIcon,nightIcon,dayWeather,nightWeather,maxTemp,minTemp,travelId)
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    db.commit()
    db.close()

def getByTravelId(travelId):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "select * from travelWeather where travelId = {}".format(travelId)
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data