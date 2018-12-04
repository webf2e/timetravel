from flask import Blueprint
from flask import session,request,Response
import os
from util.Global import gloVar
import json

locationRoute = Blueprint('locationRoute', __name__)

@locationRoute.route('/uploatLocationData',methods=["POST"])
def uploatLocationData():
    data = request.form.get("locData")
    jsonDatas = json.loads(data)
    for jsonData in jsonDatas:
        fileName = jsonData["time"]
        fileName = fileName[:fileName.find(":")].replace(" ","-")+".txt"
        locFile = open(os.path.join(gloVar.locationPath,fileName),"a+")
        locFile.write(str(jsonData)+"\n")
        locFile.close()
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