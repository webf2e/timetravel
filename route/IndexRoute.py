from flask import Blueprint,Response
import json,os
from util.Global import gloVar
from util import TimeUtil
from random import choice

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
