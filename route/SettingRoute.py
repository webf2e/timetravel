from flask import Blueprint
from flask import abort,request,Response
import json
from service import SettingService,RedisService
import logging
from util import SysUtil

settingRoute = Blueprint('settingRoute', __name__)

@settingRoute.route('/setting/getSettings',methods=["POST"])
def getSettings():
    result = []
    jsonData = SettingService.getAllSetting()
    redisData = RedisService.getSettings()
    for d in jsonData:
        if d["name"] in redisData:
            d["value"] = redisData[d["name"]]
            result.append(d)
    return Response(json.dumps(result), mimetype='application/json')

@settingRoute.route('/setting/setSetting',methods=["POST"])
def setSetting():
    name = request.form.get("name")
    value = request.form.get("value")
    if RedisService.isSettingExist(name):
        RedisService.setSetting(name,value)
    return "OK"


@settingRoute.route('/setting/getPid',methods=["POST"])
def getPid():
    return str(SysUtil.getPid())


@settingRoute.route('/setting/isStarted',methods=["POST"])
def isStarted():
    return str(SysUtil.isStarted())

@settingRoute.route('/setting/startServer',methods=["POST"])
def startServer():
    return str(SysUtil.start())

@settingRoute.route('/setting/stopServer',methods=["POST"])
def stopServer():
    return str(SysUtil.kill(SysUtil.getPid()))

@settingRoute.route('/setting/restartServer',methods=["POST"])
def restartServer():
    return str(SysUtil.restart())



@settingRoute.before_request
def print_request_info():
    urlPath = str(request.path)
    if(urlPath.find("setting") != -1):
        agent = str(request.headers.get("User-agent"))
        logging.warning("访问admin的agent：{}".format(agent))
        if(agent.find("MI 8 Explorer Edition") == -1):
            #abort(400)
            pass