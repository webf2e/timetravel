from flask import Blueprint
from flask import request,Response
import os
from util.Global import gloVar
from util.RedisKey import redisKey
from util import YingYanUtil,LocationUtil,PushUtil,SmsUtil
import datetime
import json,logging
from service import RedisService

locationRoute = Blueprint('locationRoute', __name__)

@locationRoute.route('/uploatLocationData',methods=["POST"])
def uploatLocationData():
    data = request.form.get("locData")
    if("" != data and None != data):
        jsonData = json.loads(data)
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
    if float(jsonData["radius"]) < 80:
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
    return "{} {}".format(l["time"],ld)


@locationRoute.route('/getLastLocation',methods=["POST"])
def getLastLocation():
    #先从百度鹰眼获取，如果不成功，从本地文件获取
    try:
        data = YingYanUtil.getLatestPoint()
        #如果百度的数据是60秒内的，就用百度的数据，如果不是用本地数据
        logging.warning("百度定位和本地时间的时间差：{}".format(int(datetime.datetime.now().timestamp()) - data["latest_point"]["timestramp"]))
        if int(datetime.datetime.now().timestamp()) - data["latest_point"]["timestramp"] < 60:
            return Response(json.dumps(eval(str(data["latest_point"]))), mimetype='application/json')
        else:
            return Response(json.dumps(eval(str(RedisService.get(redisKey.lastLocation)))), mimetype='application/json')
    except Exception as e:
        logging.warning(e)
        logging.warning("报错，使用redis定位数据")
        return Response(json.dumps(eval(str(RedisService.get(redisKey.lastLocation)))), mimetype='application/json')


@locationRoute.route('/visitLocationPageNotify',methods=["POST"])
def visitLocationPageNotify():
    dateTime = str(datetime.datetime.now())
    title = "我的位置页面被访问"
    content = "访问时间：{}".format(dateTime)
    PushUtil.pushToSingle(title,content,"")
    return "OK"


@locationRoute.route('/fenceNotify',methods=["POST"])
def fenceNotify():
    requestData = request.get_data()
    jsonData = json.loads(requestData.decode('utf-8'))
    if(jsonData["type"] == 2):
        PushUtil.pushToSingle("百度鹰眼","围栏通知","");
    return Response("{\"status\":0,\"message\":\"成功\"}",headers={"SignId": "baidu_yingyan"}, mimetype='application/json')


@locationRoute.route('/getNeedNotify', methods=["POST"])
def getNeedNotify():
    slience = 0
    if RedisService.isExist(redisKey.fenceNotifySlience):
        slience = 1
    return "{}:{}".format(RedisService.getSetting(redisKey.isNeedFenceInOutNotify),slience)


@locationRoute.route('/updateNeedNotify', methods=["POST"])
def updateNeedNotify():
    isNeedNotify = request.form.get("isNeedNotify")
    RedisService.setSetting(redisKey.isNeedFenceInOutNotify, isNeedNotify)
    return "OK"


@locationRoute.route('/getFence', methods=["POST"])
def getFence():
    return Response(json.dumps(eval(str(gloVar.fences))), mimetype='application/json')


@locationRoute.route('/getLocationTongji', methods=["POST"])
def getLocationTongji():
    data = RedisService.get(redisKey.locationTongji)
    if None == data:
        return Response("{}", mimetype='application/json')
    return Response(json.dumps(eval(str(data))), mimetype='application/json')

@locationRoute.route('/updateCid', methods=["POST"])
def updateCid():
    cid = request.form.get("cid")
    if None != cid:
        RedisService.setSetting(redisKey.cid, cid)
    return "OK"
