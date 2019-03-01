import json,logging
import os
import mysql.connector
from util.Global import gloVar
from util import NetInfoUtil,LocationUtil,TimeUtil

def getAllPoint():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT travelName,lon,lat FROM travel ORDER BY travelTime ASC"
    logging.warning("[sql]:{}".format(sql))
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
    sql = "SELECT DATE_FORMAT(travelTime,'%Y年%m月') AS ym FROM travel GROUP BY ym order by ym desc"
    logging.warning("[sql]:{}".format(sql))
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
    logging.warning("[sql]:{}".format(sql))
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
    logging.warning("[sql]:{}".format(sql))
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
            if column_list[i] == "id":
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
    logging.warning("[sql]:{}".format(sql))
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
    logging.warning("[sql]:{}".format(sql))
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
    logging.warning("[sql]:{}".format(sql))
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
    logging.warning("[sql]:{}".format(sql))
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
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data[0][0]

def getContent():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "SELECT content FROM travel"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data

def updateImgBy(id,imgPath):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "update travel set indexImg='{}' where id={}".format(imgPath,id)
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    db.commit()
    db.close()

def updateMostDirection():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "update travel set direction=''"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)

    sql = "update travel set direction='最东边的点' where lon = (select maxLon from (select max(lon) as maxLon from travel) tr);"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)

    sql = "update travel set direction='最西边的点' where lon = (select minLon from (select min(lon) as minLon from travel) tr);"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)

    sql = "update travel set direction='最北边的点' where lat = (select maxLat from (select max(lat) as maxLat from travel) tr);"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)

    sql = "update travel set direction='最南边的点' where lat = (select minLat from (select min(lat) as minLat from travel) tr);"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    db.commit()
    db.close()

def insert(travelName,type,content,lon,lat,travelTime,keyword,movieName,foodType,movieType,weather,weekDay,holiday):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "insert into travel(travelName,type,content,lon,lat,travelTime,keyword,direction,movieName,foodType,movieType,weather,weekDay,holiday) VALUES ('{}','{}','{}',{},{},'{}','{}','','{}','{}','{}','{}','{}','{}')"\
        .format(travelName,type,content,lon,lat,travelTime,keyword,movieName,foodType,movieType,weather,weekDay,holiday)
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    db.commit()
    db.close()

def updateById(id,travelName,type,content,lon,lat,travelTime,keyword,movieName,foodType,movieType,weekDay,holiday):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "update travel set travelName = '{}',type='{}',content='{}',lon={},lat={},travelTime='{}',keyword='{}',direction='',movieName='{}',foodType='{}',movieType='{}',weekDay='{}',holiday='{}' where id={}"\
        .format(travelName,type,content,lon,lat,travelTime,keyword,movieName,foodType,movieType,weekDay,holiday,id)
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    db.commit()
    db.close()

def getIdsByMonth(month):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "select id from travel where DATE_FORMAT(travelTime,'%Y%m')='{}' order by id DESC".format(month)
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data


def getAllMovieType():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "select movieType from travel where movieType != ''"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data


def getAllFoodType():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "select foodType from travel where foodType != ''"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data

def getAllNullWeather():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "select id,weatherCity,DATE_FORMAT(travelTime,'%Y%m%d') from travel where weather = '' or weather is null or weather = 'None'"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data

def isShowImgText(id):
    filePath = os.path.join(gloVar.galleryImgPath, str(id))
    if not os.path.exists(filePath):
        return 0
    if len(os.listdir(filePath)) == 0:
        return 0
    return 1

def updateMovieType():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "select id,movieName from travel where movieName != '' and (movieType = '' or movieType is null)"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    for d in data:
        updateSql = "update travel set movieType = '{}' where id={}".format(NetInfoUtil.getMovieType(d[1]), d[0])
        logging.warning("[sql]:{}".format(updateSql))
        cursor.execute(updateSql)
    db.commit()
    db.close()

def updateCountryToDistrict():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "select id,lon,lat from travel where country = '' or country is null"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    for d in data:
        cpcd = LocationUtil.getAddressByLonLat(d[1], d[2])
        updateSql = "update travel set country = '{}',province = '{}',city = '{}',district = '{}' where id={}"\
            .format(cpcd["country"],cpcd["province"],cpcd["city"],cpcd["district"],d[0])
        logging.warning("[sql]:{}".format(updateSql))
        cursor.execute(updateSql)
    db.commit()
    db.close()

def updateWeather(id,weather):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "update travel set weather = '{}' where id={}".format(weather, id)
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    db.commit()
    db.close()

def updateWeekDay():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "select id,DATE_FORMAT(travelTime,'%Y-%m-%d %H:%i:%S') from travel where weekDay = '' or weekDay is null"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    for d in data:
        weekDay = TimeUtil.getWeekNumByDate(d[1])
        updateSql = "update travel set weekDay = '{}' where id={}"\
            .format(weekDay,d[0])
        logging.warning("[sql]:{}".format(updateSql))
        cursor.execute(updateSql)
    db.commit()
    db.close()

def updateHoliday():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "select id,DATE_FORMAT(travelTime,'%Y-%m-%d') from travel where holiday is null"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    for d in data:
        holiday = TimeUtil.getHoliday(d[1])
        updateSql = "update travel set holiday = '{}' where id={}"\
            .format(holiday,d[0])
        logging.warning("[sql]:{}".format(updateSql))
        cursor.execute(updateSql)
    db.commit()
    db.close()

def getWeatherForIcon():
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "select weather from travel where weather != '' and weather is not null and weather != 'None' group by weather"
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data