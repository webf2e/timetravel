from util.Global import gloVar
import json
import os
import mysql.connector
from util.Global import gloVar

def getAllPoint():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT travelName,lon,lat FROM travel ORDER BY travelName DESC"
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    fields = cursor.description
    db.commit()
    db.close()
    return changeToJsonStr(fields,data)

def getTravelTimeGroup():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT DATE_FORMAT(travelTime,'%Y年%m月') AS ym FROM travel GROUP BY ym"
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    fields = cursor.description
    db.commit()
    db.close()
    return changeToJsonStr(fields, data)

def getNew4():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "select * from travel ORDER BY travelTime DESC limit 4"
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    fields = cursor.description
    db.commit()
    db.close()
    return changeToJsonStr(fields, data)

def getByLonLat(lon,lat):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "select * from travel where lon='{}' and lat='{}'".format(lon,lat)
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    fields = cursor.description
    db.commit()
    db.close()
    return changeToJsonStr(fields, data)

def changeToJsonStr(fields,data):
    finalResult = "["
    column_list = []
    for i in fields:
        column_list.append(i[0])
    for row in data:
        result = {}
        for i in range(0, len(column_list)):
            result[column_list[i]] = str(row[i])
            if(column_list[i] == "id"):
                result["hasImg"] = str(isShowImgText(row[0]))

        finalResult += str(json.dumps(result, ensure_ascii=False)) + ","

    finalResult = finalResult[0:-1] + "]"
    return finalResult

def getByDate(date):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT * FROM travel where DATE_FORMAT(travelTime,'%Y年%m月') = '{}' ORDER BY travelTime desc".format(date)
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    fields = cursor.description
    db.commit()
    db.close()
    return changeToJsonStr(fields, data)

def getTypes():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT type FROM travel group by type"
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    fields = cursor.description
    db.commit()
    db.close()
    return changeToJsonStr(fields, data)

def getAllTravelNames():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT id,travelName FROM travel order by travelTime desc"
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    fields = cursor.description
    db.commit()
    db.close()
    return changeToJsonStr(fields, data)

def getTravelInfoById(id):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT * FROM travel where id = {}".format(id)
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    fields = cursor.description
    db.commit()
    db.close()
    return changeToJsonStr(fields, data)

def getTravelNameById(id):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT travelName FROM travel where id = {}".format(id)
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data[0][0]

def updateImgBy(id,imgPath):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "update travel set indexImg='{}' where id={}".format(imgPath,id)
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    db.commit()
    db.close()

def insert(travelName,type,content,lon,lat,travelTime):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "insert into travel(travelName,type,content,lon,lat,travelTime) VALUES ('{}','{}','{}',{},{},'{}')"\
        .format(travelName,type,content,lon,lat,travelTime)
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    db.commit()
    db.close()

def updateById(id,travelName,type,content,lon,lat,travelTime):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "update travel set travelName = '{}',type='{}',content='{}',lon={},lat={},travelTime='{}' where id={}"\
        .format(travelName,type,content,lon,lat,travelTime,id)
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    db.commit()
    db.close()

def getIdTimeLast3Month():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "select id,DATE_FORMAT(travelTime,'%Y%m') as ym from travel where DATE_FORMAT(travelTime,'%Y年%m月') in (select ym from (SELECT DATE_FORMAT(travelTime,'%Y年%m月') AS ym FROM travel GROUP BY ym ORDER BY ym desc limit 3) ymt) order by id DESC"
    print("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data

def isShowImgText(id):
    filePath = os.path.join(gloVar.galleryImgPath,str(id))
    if not os.path.exists(filePath):
        return 0
    if len(os.listdir(filePath)) == 0:
        return 0
    return 1