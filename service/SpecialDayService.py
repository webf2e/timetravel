import json
import logging
import mysql.connector
from util.Global import gloVar

def selectByMonthDay(monthDay):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "select * from specialDay where monthDay='{}'".format(monthDay)
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data


def getRemainDaysFoSpecialDay(remainDays):
    db = mysql.connector.connect(
        host=gloVar.dbHost,
        user=gloVar.dbUser,
        passwd=gloVar.dbPwd,
        database=gloVar.dbName
    )
    cursor = db.cursor()
    sql = "select wd.* from (select *,datediff(str_to_date(concat(date_format(now(),'%Y'),monthDay),'%Y%m%d'),now()) as delay " \
          "from specialDay where (monthDay like '%1%' or monthDay like '%0%')) wd where delay <={} and delay >= 0".format(remainDays)
    logging.warning("[sql]:{}".format(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    db.close()
    return data