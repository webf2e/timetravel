from flask import Blueprint
from flask import session,request,Response
import os
from util.Global import gloVar
from util import YingYanUtil,LocationUtil
import datetime
from util import PushUtil,FileUtil,SmsUtil
import json
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
        #保存到redis中
        RedisService.set("lastLocation",str(jsonData))
        #发送到鹰眼
        try:
            YingYanUtil.addPoint(jsonData)
        except Exception as e:
            print(e)

    #围栏判断，定位半径精度小于100时开始进行判断。
    if float(jsonData["radius"]) < 80:
        if not RedisService.isExist("lastFenceTime"):
            lon = float(jsonData["lon"])
            lat = float(jsonData["lat"])
            state = LocationUtil.getFenceState(lon,lat)
            #从redis中获取上次围栏状态，判断是否要报警
            lastState = RedisService.get("lastFenceState")
            if None == lastState:
                RedisService.set("lastFenceState", state)
                lastState = state
            else:
                lastState = lastState.replace("'","\"")
                lastState = json.loads(lastState)
            #比较当前状态和历史状态
            compareState = LocationUtil.compareState(lastState, state)
            #状态有更新
            if(len(compareState) > 0):
                RedisService.setWithTtl("lastFenceTime", str(datetime.datetime.now()), 120)
                RedisService.set("lastFenceState", state)
                PushUtil.pushToSingle("围栏有变更", str(compareState), "")
                SmsUtil.sendFenceModify(compareState)


    #获取最后的数据
    location = RedisService.get("lastLocation")
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
        if int(datetime.datetime.now().timestamp()) - data["latest_point"]["loc_time"] < 60:
            return Response(json.dumps(eval(str(data["latest_point"]))), mimetype='application/json')
        else:
            return Response(RedisService.get("lastLocation"), mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(RedisService.get("lastLocation"), mimetype='application/json')


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
    print(jsonData)
    if(jsonData["type"] == 2):
        PushUtil.pushToSingle("百度鹰眼","围栏通知","");
    return Response("{\"status\":0,\"message\":\"成功\"}",headers={"SignId": "baidu_yingyan"}, mimetype='application/json')

