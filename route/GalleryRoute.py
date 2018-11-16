from flask import Blueprint
from flask import abort,request,Response
import math
from util.Global import gloVar
import json
import os
from service import TravelService

galleryRoute = Blueprint('galleryRoute', __name__)

@galleryRoute.route('/getImageByIdPage',methods=["POST"])
def getImageByIdPage():
    countInOnePage = 6
    resultMap = {}
    id = request.form.get("id")
    page = int(request.form.get("page"))
    filePath = os.path.join(gloVar.galleryImgPath,id)
    if not os.path.exists(filePath):
        return Response(json.dumps(resultMap, ensure_ascii=False), mimetype='application/json')
    files = os.listdir(filePath)
    files.sort()
    imgs = []
    for file in files:
        imgs.append(os.path.join("/static/gallery",id,file))
    imgLength = len(imgs)
    if imgLength == 0:
        return Response(json.dumps(resultMap, ensure_ascii=False), mimetype='application/json')
    resultMap["totalImgCount"] = imgLength
    totalPageNum = int(math.ceil(imgLength / countInOnePage))
    resultMap["totalPageNum"] = totalPageNum
    if page > totalPageNum:
        page = totalPageNum
    elif page < 1:
        page = 1
    resultMap["currentPageNum"] = page
    if totalPageNum == page:
        resultMap["imgList"] = imgs[(page - 1) * countInOnePage:]
    else:
        resultMap["imgList"] = imgs[(page - 1) * countInOnePage:page * countInOnePage]

    resultMap["travelName"] = TravelService.getTravelNameById(id)
    return Response(json.dumps(resultMap, ensure_ascii=False), mimetype='application/json')

@galleryRoute.route('/getImageByMonthPage',methods=["POST"])
def getImageByMonthPage():
    countInOnePage = 6
    resultMap = {}
    month = request.form.get("month")
    page = int(request.form.get("page"))
    if not month in gloVar.monthImgMap:
        return Response(json.dumps(resultMap, ensure_ascii=False), mimetype='application/json')
    imgs = gloVar.monthImgMap[month]
    imgLength = len(imgs)
    if imgLength == 0:
        return Response(json.dumps(resultMap, ensure_ascii=False), mimetype='application/json')
    resultMap["totalImgCount"] = imgLength
    totalPageNum = int(math.ceil(imgLength / countInOnePage))
    resultMap["totalPageNum"] = totalPageNum
    if page > totalPageNum:
        page = totalPageNum
    elif page < 1:
        page = 1
    resultMap["currentPageNum"] = page
    print(imgs)
    if totalPageNum == page:
        resultMap["imgList"] = imgs[(page - 1) * countInOnePage:]
    else:
        resultMap["imgList"] = imgs[(page - 1) * countInOnePage:page * countInOnePage]
    return Response(json.dumps(resultMap, ensure_ascii=False), mimetype='application/json')