from flask import Blueprint
from flask import session,request,Response
import os
from util.Global import gloVar
import json

memoryRoute = Blueprint('memoryRoute', __name__)

@memoryRoute.route('/getImagePath',methods=["POST"])
def getImagePath():
    date = request.form.get("date");
    if(date == None or "" == date):
        return Response({}, mimetype='application/json')
    dates = date.split("-");
    year = dates[0]
    month = int(dates[1])
    if(month < 10):
        month = "0" + str(month)
    day = int(dates[2])
    if(day < 10):
        day = "0" + str(day)
    dirPath = os.path.join(str(gloVar.chatDirPath), str(year), str(month), str(day))
    if not os.path.exists(dirPath):
        return Response({}, mimetype='application/json')
    fileNames = []
    for fileName in os.listdir(dirPath):
        if fileName.startswith("20"):
            fileNames.append(os.path.join("/static/chatImg",str(year),str(month),str(day),fileName))
    fileNames.sort()
    return Response(json.dumps(fileNames, ensure_ascii=False), mimetype='application/json')

@memoryRoute.route('/getLastChatDate',methods=["POST"])
def getLastChatDate():
    year = max(os.listdir(str(gloVar.chatDirPath)))
    month = max(os.listdir(os.path.join(str(gloVar.chatDirPath), year)))
    day = max(os.listdir(os.path.join(str(gloVar.chatDirPath), year, month)))
    return "{}-{}-{}".format(year,month,day)