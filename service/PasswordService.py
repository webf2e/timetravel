from util.Global import gloVar
import json
import datetime
import mysql.connector

def getCurrentPassword():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    cursor.execute("SELECT id,password,useTime FROM password where useTime is not null")
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data

def resetAllPassword():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    cursor.execute("update password set useTime = null")
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

def updateRandomPassword():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    cursor.execute("update password set useTime = '{}' ORDER BY RAND() LIMIT 1".format(datetime.datetime.now()))
    db.commit()
    db.close()
