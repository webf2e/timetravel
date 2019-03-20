from flask import Blueprint
from flask import request,Response
import os
from util.Global import gloVar
from util.RedisKey import redisKey
from util import YingYanUtil,LocationUtil,PushUtil,SmsUtil,EmailUtil
import datetime
import json,logging
from service import RedisService

appRoute = Blueprint('appRoute', __name__)

@appRoute.route('/uploadLocationData',methods=["POST"])
def uploatLocationData():
    data = request.form.get("locData")
    print("locationData:{}".format(data))
    if("" != data and None != data):
        jsonData = LocationUtil.changeLocationData(data)
        jsonData["dataSource"] = "local"
        #保存到文件
        fileName = jsonData["time"]
        fileName = fileName[:fileName.find(":")].replace(" ","-")+".txt"
        locFile = open(os.path.join(gloVar.locationPath,fileName),"a+")
        locFile.write(str(jsonData)+"\n")
        locFile.close()
        #保存末次位置到redis中
        RedisService.set(redisKey.lastLocation,str(jsonData))
        #发送到鹰眼
        try:
            YingYanUtil.addPoint(jsonData)
        except Exception as e:
            logging.warning(e)

    #围栏判断，定位半径精度小于80时开始进行判断。
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
                RedisService.setWithTtl(redisKey.lastFenceTime, str(datetime.datetime.now()), 60 * 10)
                RedisService.set(redisKey.lastFenceState, state)
                if (int(RedisService.getSetting(redisKey.isNeedFenceInOutNotify)) == 1 and not RedisService.isExist(redisKey.fenceNotifySlience)):
                    PushUtil.pushToSingle("围栏有变更", str(compareState), "")
                    SmsUtil.sendFenceModify(compareState)
                else:
                    PushUtil.pushToSingle("围栏有变更，亲爱的收不到", str(compareState), "")


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
        RedisService.setSetting(redisKey.cid, cid)
    return "OK"


@appRoute.route('/appStart', methods=["POST"])
def appStart():
    logging.warning("app启动")
    EmailUtil.sendEmail("app启动","app在{}启动".format(datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")))
    return "OK"