from flask import Blueprint
from flask import session,request,Response
import os
from util.Global import gloVar
import json
from util import YingYanUtil
import datetime
from util import PushUtil,FileUtil
import json

locationRoute = Blueprint('locationRoute', __name__)

@locationRoute.route('/uploatLocationData',methods=["POST"])
def uploatLocationData():
    data = request.form.get("locData")
    if("" != data and None != data):
        jsonData = json.loads(data)
        fileName = jsonData["time"]
        fileName = fileName[:fileName.find(":")].replace(" ","-")+".txt"
        locFile = open(os.path.join(gloVar.locationPath,fileName),"a+")
        locFile.write(str(jsonData)+"\n")
        locFile.close()
        #发送到鹰眼
        #判断间隔时间是否大于5秒，超过5s才上传
        try:
            YingYanUtil.addPoint(jsonData)
        except Exception as e:
            print(e)

    #获取最后的数据
    location= FileUtil.getLastLocationInFile()
    l = json.loads(location)
    ld = "暂无地理数据"
    if "locationDescribe" in l:
        ld = l["locationDescribe"]
    return "{} {}".format(l["time"],ld)

@locationRoute.route('/getLastLocation',methods=["POST"])
def getLastLocation():
    #先从百度鹰眼获取，如果不成功，从本地文件获取
    try:
        data = YingYanUtil.getLatestPoint()
        return Response(json.dumps(eval(str(data["latest_point"]))), mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(FileUtil.getLastLocationInFile(), mimetype='application/json')

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
