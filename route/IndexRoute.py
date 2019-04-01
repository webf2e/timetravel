from flask import Blueprint,Response,request
import json,os,datetime
from util.Global import gloVar
from util import TimeUtil,PushUtil
from random import choice
from service import MessageService,RedisService

indexRoute = Blueprint('indexRoute', __name__)

@indexRoute.route('/getMeetingDays',methods=["POST"])
def getMeetingDays():
    timeList = []
    timeList.append("我们已经相遇{}天！".format(TimeUtil.subDay("2018-10-05 00:00:00")))
    timeList.append("我成为你的男朋友第{}天！".format(TimeUtil.subDay("2018-12-09 00:00:00")))
    return Response(json.dumps(timeList), mimetype='application/json')

@indexRoute.route('/getRandomIndexImg',methods=["POST"])
def getRandomIndexImg():
    imgDict = {}
    galleryPaths = sorted(map(int,os.listdir(os.path.join(gloVar.galleryImgPath))),reverse=True)[:5]
    for galleryPath in galleryPaths:
        path = os.path.join(gloVar.galleryImgPath, str(galleryPath))
        imgPath = os.path.join(path,choice(os.listdir(path)))
        imgDict[galleryPath] = imgPath.replace(gloVar.galleryImgPath,"")
    return Response(json.dumps(imgDict), mimetype='application/json')


@indexRoute.route('/getNewMessage',methods=["POST"])
def getNewMessage():
    count = request.form.get("count")
    return Response(MessageService.getNewMessage(count), mimetype='application/json')


@indexRoute.route('/addMessage',methods=["POST"])
def addMessage():
    message = request.form.get("msg")
    now = datetime.datetime.now()
    dateTime = datetime.datetime.strftime(now, "%Y-%m-%d %H:%M:%S")
    PushUtil.pushToSingle("有新的留言", message, "")
    MessageService.insert(message, dateTime, 0)
    # 清理redis
    dateStr = datetime.datetime.strftime(now, "%Y-%m-%d")
    redisKey = "special_{}".format(dateStr)
    if RedisService.isExist(redisKey):
        RedisService.delete(redisKey)
    return "OK"
