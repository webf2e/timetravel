import json,logging
import os,oss2,datetime,requests
import mysql.connector
from util.Global import gloVar
from service import TravelService,RedisService
from util.RedisKey import redisKey
from util import TimeUtil,NetInfoUtil,LocationUtil,PushUtil,SmsUtil
from git import *


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

def getServiceStatus(isCheckSendMsg):
    #-1，服务器异常 0，业务异常 1，正常
    result = {}
    result["checkTime"] = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
    #mysql
    try:
        list = TravelService.getTravelInfoById(1)
        if len(list) == 0:
            result["mysql"] = 0
        else:
            result["mysql"] = 1
    except:
        result["mysql"] = -1
    #redis
    try:
        RedisService.getSetting(redisKey.isNeedFenceInOutNotify)
        result["redis"] = 1
    except:
        result["redis"] = -1
    #git
    try:
        g = Git(gloVar.gitFilePath)
        if g.log("-1").find("Author") == -1:
            result["git"] = 0
        else:
            result["git"] = 1
    except:
        result["git"] = -1
    #oss
    try:
        auth = oss2.Auth('LTAIOWHFyQYc3gQN', 'kkN3gdS3x32g4etD7lpYbNnpYZmlmr')
        bucket = oss2.Bucket(auth, 'http://oss-cn-hongkong-internal.aliyuncs.com', 'timetravelbak')
        fileInOss = {}
        for obj in oss2.ObjectIterator(bucket, delimiter='/'):
            fileInOss[obj.key] = bucket.get_object_meta(obj.key).headers['Content-Length']
        if len(fileInOss) > 0:
            result["oss"] = 1
        else:
            result["oss"] = 0
    except:
        result["oss"] = -1
    #聚合万年历接口
    try:
        r = TimeUtil.getJuHeCalendar(datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d"))
        if None == r:
            result["聚合万年历接口"] = 0
        else:
            result["聚合万年历接口"] = 1
    except:
        result["聚合万年历接口"] = -1
    #猫眼电影
    try:
        r = NetInfoUtil.getMovieType("泰坦尼克号")
        if r.find("灾难") == -1:
            result["猫眼电影抓取"] = 0
        else:
            result["猫眼电影抓取"] = 1
    except:
        result["猫眼电影抓取"] = -1
    #百度编码API
    try:
        r = LocationUtil.getAddressByLonLat(116.251672,40.079037)
        if "country" in r:
            result["百度编码API"] = 1
        else:
            result["百度编码API"] = 0
    except:
        result["百度编码API"] = -1
    #百度鹰眼
    try:
        service_id = 207270
        entity_name = "你的小可爱"
        ak = "fd2PMcjfqa7hRP0xoqGta5w2IODQ2kig"
        url = "http://yingyan.baidu.com/api/v3/track/getlatestpoint?service_id={}&entity_name={}&coord_type_output=bd09ll&" \
              "process_option=need_denoise=1,radius_threshold=80,need_mapmatch=0,transport_mode=auto&ak={}" \
            .format(service_id, entity_name, ak)
        r = requests.get(url).text
        if r.find("\"status\":0") == -1:
            result["百度鹰眼API-末次位置"] = 0
        else:
            result["百度鹰眼API-末次位置"] = 1
    except:
        result["百度鹰眼API-末次位置"] = -1
    if isCheckSendMsg:
        #个推
        try:
            r = PushUtil.pushToSingle("推送测试","收到这条消息说明推送没有问题","")
            if r.find("successed_online") == -1:
                result["消息推送"] = 0
            else:
                result["消息推送"] = 1
        except:
            result["消息推送"] = -1
        #短信
        try:
            r = SmsUtil.sendSmsBytempId("15210650960",153176)
            if r == "OK":
                result["短信通知"] = 1
            else:
                result["短信通知"] = 0
        except:
            result["短信通知"] = -1
    RedisService.set(redisKey.serviceCheck,json.dumps(result))
    return result