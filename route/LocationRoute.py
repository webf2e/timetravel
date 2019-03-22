from flask import Blueprint
from flask import request,Response
import os
from util.Global import gloVar
from util.RedisKey import redisKey
from util import YingYanUtil,LocationUtil,PushUtil,SmsUtil
import datetime
import json,logging
from service import RedisService,FenceMessageService

locationRoute = Blueprint('locationRoute', __name__)


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
    title = "我的位置页面被访问"
    PushUtil.pushToSingle(title,"","")
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

@locationRoute.route('/getFenceMessageByDate', methods=["POST"])
def getFenceMessageByDate():
    date = request.form.get("date")
    return Response(FenceMessageService.getAllByDate(date), mimetype='application/json')


@locationRoute.route('/getLocationTongji', methods=["POST"])
def getLocationTongji():
    data = RedisService.get(redisKey.locationTongji)
    if None == data:
        return Response("{}", mimetype='application/json')
    return Response(json.dumps(eval(str(data))), mimetype='application/json')

@locationRoute.route('/getTrackByHour', methods=["POST"])
def getTrackByHour():
    hour = request.form.get("hour")
    files = sorted(os.listdir(gloVar.locationPath))
    files = files[-int(hour):]
    dataCount = 0
    datas = []
    result = {}
    startTime = ""
    endTime = ""
    lastHour = ""
    for file in files:
        fileName = os.path.join(gloVar.locationPath, file)
        fileLines = open(fileName,"r+")
        for fileLine in fileLines:
            fileLine = fileLine.strip()
            if "" == fileLine:
                continue
            data = json.loads(json.dumps(eval(str(fileLine))))
            if data["radius"] > 100:
                print(data["radius"])
                continue
            d = {}
            d["b"] = data["lat"]
            d["l"] = data["lon"]
            currentHour = data["time"][data["time"].find(" "):data["time"].find(":")]
            if currentHour != lastHour:
                d["t"] = data["time"]
                d["h"] = int(currentHour)
            lastHour = currentHour
            if "" == startTime:
                startTime = data["time"]
            endTime = data["time"]
            datas.append(d)
            dataCount += 1
        fileLines.close()
    result["data"] = datas
    result["count"] = dataCount
    result["startTime"] = startTime
    result["endTime"] = endTime
    return Response(json.dumps(result), mimetype='application/json')

@locationRoute.route('/getTrackByDate', methods=["POST"])
def getTrackByDate():
    date = request.form.get("date")
    result = {}
    #校验
    yestoday = int(datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=1), "%Y%m%d"))
    try:
        st = int(datetime.datetime.strptime(date, "%Y%m%d").timestamp())
    except:
        result["errorMsg"] = "输入的时间格式不正确，正确格式：{}".format(yestoday)
        return Response(json.dumps(result), mimetype='application/json')
    if int(date) > yestoday:
        result["errorMsg"] = "只能输入昨天或昨天前的日期哦"
        return Response(json.dumps(result), mimetype='application/json')

    rk = redisKey.trackByDate+date
    if RedisService.isExist(rk):
        return Response(RedisService.get(rk), mimetype='application/json')
    startTime = ""
    endTime = ""
    dataCount = 0
    datas = []
    et = st + 86399
    trackResult = YingYanUtil.getTrack(st,et,1,5000)
    lastHour = ""
    if "points" in trackResult:
        points = trackResult["points"]
        for point in points:
            if point["radius"] > 100:
                print(point["radius"])
                continue
            d = {}
            d["b"] = point["latitude"]
            d["l"] = point["longitude"]
            currentHour = point["create_time"][point["create_time"].find(" "):point["create_time"].find(":")]
            if currentHour != lastHour:
                d["t"] = point["create_time"]
                d["h"] = int(currentHour)
            lastHour = currentHour
            if "" == startTime:
                startTime = point["create_time"]
            endTime = point["create_time"]
            datas.append(d)
            dataCount += 1
    result["errorMsg"] = ""
    result["data"] = datas
    result["count"] = dataCount
    result["startTime"] = startTime
    result["endTime"] = endTime
    result = json.dumps(result)
    RedisService.setWithTtl(rk,result,60 * 60 * 48)
    return Response(result, mimetype='application/json')