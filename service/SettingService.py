import json,logging
import os
import mysql.connector
from util.Global import gloVar

def getAllSetting():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT * FROM setting"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    fields = cursor.description
    db.commit()
    db.close()
    return json.loads(changeToJsonStr(fields, data))


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