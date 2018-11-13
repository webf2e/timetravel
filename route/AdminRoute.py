from flask import Blueprint
from flask import session,request,Response
import os
from util.Global import gloVar
import json
from service import TravelService
from util import FileUtil

adminRoute = Blueprint('adminRoute', __name__)

@adminRoute.route('/admin/upChatImg',methods=["POST"])
def upChatImg():
    #先判断文件夹下有没有文件，如果有就等一下
    for f in os.listdir(gloVar.chatDirPath):
        if(os.path.isfile(os.path.join(gloVar.chatDirPath,f))):
            return "稍等一下，暂时有文件没有转移"
    files = str(request.files)
    date = str(request.form.get("date"))
    dates = date.split("_")
    index = 0;
    #先判断文件夹是否存在
    filePath = os.path.join(gloVar.chatDirPath,dates[0],dates[1],dates[2])
    if os.path.exists(filePath):
        index = str(max(os.listdir(filePath)))
        index = int(index[index.rfind("_")+1:index.rfind(".")])
    else:
        os.makedirs(filePath)
    count = 0
    for i in range(0,100):
        typeName = "file{}".format(i)
        if files.rfind("'{}'".format(typeName)) == -1:
            continue
        file = request.files[typeName]
        fn = str(file.filename)
        if not fn.lower().endswith("png"):
            continue
        index += 1
        file.save(os.path.join(gloVar.chatDirPath, "{}_{}.png".format(date,index)))
        count += 1
    return '成功上传{}个文件'.format(count)


@adminRoute.route('/admin/showImages',methods=["POST"])
def showImages():
    date = request.form.get("date")
    dates = date.split("_")
    filePath = os.path.join(gloVar.chatDirPath,dates[0],dates[1],dates[2])
    if not os.path.exists(filePath):
        return Response("{}", mimetype='application/json')

    fileNames = []
    for fileName in os.listdir(filePath):
        fileNames.append(os.path.join("/static/chatImg/",dates[0],dates[1],dates[2],fileName))
    fileNames.sort()
    return Response(json.dumps(fileNames, ensure_ascii=False), mimetype='application/json')

@adminRoute.route('/admin/getType',methods=["POST"])
def getType():
    return Response(TravelService.getTypes(), mimetype='application/json')

@adminRoute.route('/admin/getAllTravelNames',methods=["POST"])
def getAllTravelNames():
    return Response(TravelService.getAllTravelNames(), mimetype='application/json')

@adminRoute.route('/admin/getTravelInfoById',methods=["POST"])
def getTravelInfoById():
    id = request.form.get("id")
    return Response(TravelService.getTravelInfoById(id), mimetype='application/json')

@adminRoute.route('/admin/upTravelIndexImg',methods=["POST"])
def upTravelIndexImg():
    id = str(request.form.get("id"))
    file = request.files["file"]
    filePath = os.path.join(gloVar.travelIndexImgPath, "{}.png".format(id))
    file.save(filePath)
    FileUtil.resizeImg(filePath, 150, 130)
    TravelService.updateImgBy(id, os.path.join("/static/travelIndexImg","{}.png".format(id)))
    return "文件上传成功"

@adminRoute.route('/admin/addTravelInfo',methods=["POST"])
def addTravelInfo():
    travelName = request.form.get("travelName")
    type = request.form.get("type")
    content = request.form.get("content")
    lon = request.form.get("lon")
    lat = request.form.get("lat")
    travelTime = request.form.get("travelTime")
    TravelService.insert(travelName,type,content,lon,lat,travelTime)
    return "添加成功"

@adminRoute.route('/admin/editTravelInfo',methods=["POST"])
def editTravelInfo():
    id = request.form.get("id")
    travelName = request.form.get("travelName")
    type = request.form.get("type")
    content = request.form.get("content")
    lon = request.form.get("lon")
    lat = request.form.get("lat")
    travelTime = request.form.get("travelTime")
    TravelService.updateById(id,travelName,type,content,lon,lat,travelTime)
    return "修改成功"