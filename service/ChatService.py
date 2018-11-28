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