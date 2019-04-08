from flask import Blueprint
from flask import request,Response
import os
from util.Global import gloVar
from util.RedisKey import redisKey
from util import YingYanUtil,LocationUtil,PushUtil,SmsUtil,EmailUtil,CommonUtil
import datetime
import json,logging
from service import RedisService,FenceMessageService

appRoute = Blueprint('appRoute', __name__)

@appRoute.route('/uploadLocationData',methods=["POST"])
def uploatLocationData():
    data = request.form.get("locData")
    print("locationData:{}".format(data))
    if("" != data and None != data):
        jsonData = LocationUtil.changeLocationData(data)
        jsonData["dataSource"] = "local"
        #进行校验
        location = RedisService.get(redisKey.lastLocation)
        if None != location:
            l = json.loads(json.dumps(eval(location)))
            timeDelay = (jsonData["timestramp"] - l["timestramp"]) // 1000
            distance = int(LocationUtil.getDistance(jsonData["lon"], jsonData["lat"], l["lon"], l["lat"]))
            if timeDelay <= 0:
                return "{} {} {}".format(l["time"], "时间差小于等于0丢弃", RedisService.getSetting(redisKey.isNeedAutoRestartForApp))
            speed = int((distance / timeDelay))
            #最大400km/h
            #系数
            c = 1.2
            jsonData["speeds"] = []
            if "speeds" in l:
                logging.warning("在")
                speedLimit = c * (sum(l["speeds"]) / len(l["speeds"]))
            else:
                logging.warning("不在")
                speedLimit = 111

            jsonData["speeds"].append(speed)
            if len(jsonData["speeds"]) > 30:
                jsonData["speeds"].remove(jsonData["speeds"][0])

            logging.warning("时间差：{}秒，距离：{}米，速度：{}米/秒，限速：{}米/秒，速度队列大小：{}".format(timeDelay, distance, speed, speedLimit,len(jsonData["speeds"])))

            if speed > speedLimit:
                speedToHigh = "{} {} {}".format(l["time"], "速度过大，丢弃", RedisService.getSetting(redisKey.isNeedAutoRestartForApp))
                logging.warning("{}，限速为：{}，当前速度为：{}".format(speedToHigh, speedLimit, speed))
                return speedToHigh
        #保存到文件
        fileName = jsonData["time"]
        fileName = fileName[:fileName.find(":")].replace(" ","-")+".txt"
        locFile = open(os.path.join(gloVar.locationPath,fileName),"a+")
        locFile.write(str(jsonData)+"\n")
        locFile.close()
        #保存末次位置到redis中
        logging.warning("str(jsonData):{}".format(str(jsonData)))
        RedisService.set(redisKey.lastLocation,str(jsonData))
        #发送到鹰眼
        try:
            YingYanUtil.addPoint(jsonData)
        except Exception as e:
            logging.warning(e)

        #围栏判断，定位半径精度小于50时开始进行判断。
        if float(jsonData["radius"]) < 50:
            if not RedisService.isExist(redisKey.lastFenceTime):
                lon = float(jsonData["lon"])
                lat = float(jsonData["lat"])
                state = LocationUtil.getFenceState(lon,lat)
                #从redis中获取上次围栏状态，判断是否要报警
                lastState = RedisService.get(redisKey.lastFenceState)
                if None == lastState:
                    RedisService.set(redisKey.lastFenceState, state)
                    lastState = state
                else:
                    lastState = lastState.replace("'","\"")
                    lastState = json.loads(lastState)
                #比较当前状态和历史状态
                compareState = LocationUtil.compareState(lastState, state)
                #状态有更新
                if(len(compareState) > 0):
                    RedisService.setWithTtl(redisKey.lastFenceTime, str(datetime.datetime.now()), 60 * 15)
                    RedisService.set(redisKey.lastFenceState, state)
                    jsonMsg = CommonUtil.getTempIdAndContent(compareState)
                    if (int(RedisService.getSetting(redisKey.isNeedFenceInOutNotify)) == 1 and not RedisService.isExist(redisKey.fenceNotifySlience)):
                        PushUtil.pushToSingle("围栏有变更", jsonMsg["content"], "")
                        SmsUtil.sendSmsBytempId(gloVar.notifyMobile, jsonMsg["tempId"])
                    else:
                        PushUtil.pushToSingle("围栏有变更，亲爱的收不到", jsonMsg["content"], "")
                    #保存到数据库
                    time = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
                    FenceMessageService.insert(jsonMsg["content"],time,lon,lat)


    #获取最后的数据
    location = RedisService.get(redisKey.lastLocation)
    l = json.loads(json.dumps(eval(location)))
    ld = "暂无地理数据"
    if "locationDescribe" in l:
        ld = l["locationDescribe"]
    return "{} {} {}".format(l["time"],ld,RedisService.getSetting(redisKey.isNeedAutoRestartForApp))

@appRoute.route('/pushToApp',methods=["POST"])
def pushToApppos():
    title = request.form.get("title")
    content = request.form.get("content")
    if(None != title and "" != title and None != content and "" != content):
        PushUtil.pushToSingle(title,content,"")
    return "OK"

@appRoute.route('/updateCid', methods=["POST"])
def updateCid():
    cid = request.form.get("cid")
    if None != cid:
        logging.warning("cid:{}".format(cid))
        RedisService.setSetting(redisKey.cid, cid)
    return "OK"


@appRoute.route('/appStart', methods=["POST"])
def appStart():
    logging.warning("app启动")
    EmailUtil.sendEmail("app启动","app在{}启动".format(datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")))
    return "OK"