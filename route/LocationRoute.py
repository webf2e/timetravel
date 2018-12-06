from flask import Blueprint
from flask import session,request,Response
import os
from util.Global import gloVar
import json
from util import YingYanUtil

locationRoute = Blueprint('locationRoute', __name__)

@locationRoute.route('/uploatLocationData',methods=["POST"])
def uploatLocationData():
    data = request.form.get("locData")
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
    return "OK"

@locationRoute.route('/getLastLocation',methods=["POST"])
def getLastLocation():
    list = os.listdir(gloVar.locationPath)
    filePath = os.path.join(gloVar.locationPath, max(list))
    datas = open(filePath,"r+")

    for data in datas:
        data = data.strip()
        if "" == data:
            continue
        lastLocation = data
    lastLocation = lastLocation.replace("'","\"")
    return Response(lastLocation, mimetype='application/json')