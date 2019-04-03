from flask import Blueprint,send_from_directory
from flask import abort,request,Response
import math
from util.Global import gloVar
import json
import os
from service import TravelService
from util import FileUtil

galleryRoute = Blueprint('galleryRoute', __name__)

@galleryRoute.route('/getImageByIdPage',methods=["POST"])
def getImageByIdPage():
    countInOnePage = 6
    resultMap = {}
    id = request.form.get("id")
    page = int(request.form.get("page"))
    filePath = os.path.join(gloVar.galleryImgPath, id)
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
    dbIds = TravelService.getIdsByMonth(month)
    if len(dbIds) == 0:
        return Response(json.dumps(resultMap, ensure_ascii=False), mimetype='application/json')
    ids = []
    for dbId in dbIds:
        ids.append(dbId[0])
    imgs = FileUtil.getGalleryImgByMonth(ids)
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
    return Response(json.dumps(resultMap, ensure_ascii=False), mimetype='application/json')


@galleryRoute.route('/getImageInfo',methods=["POST"])
def getImageInfo():
    imgPath = request.form.get("imgPath")
    imgPath = imgPath.replace("/static/gallery/","")
    originImgPath = os.path.join(gloVar.galleryOriginImgPath, imgPath)
    smallImgPath = os.path.join(gloVar.galleryImgPath, imgPath)
    id = imgPath[0:imgPath.find("/")]
    imgName = imgPath[imgPath.rfind("/") + 1:]
    travel = json.loads(TravelService.getTravelInfoById(id))[0]
    result = {}
    result["travelName"] = travel["travelName"]
    result["address"] = "{}{}{}{}".format(travel["country"],travel["province"],travel["city"],travel["district"])
    result["imgName"] = imgName
    result["originImgSize"] = int(os.path.getsize(originImgPath) / 1024)
    result["smallImgSize"] = int(os.path.getsize(smallImgPath) / 1024)
    return Response(json.dumps(result), mimetype='application/json')


@galleryRoute.route("/download/GalleryImg", methods=['GET'])
def downloadGalleryImg():
    imgName = request.args.get("in")
    id = request.args.get("id")
    originImgPath = os.path.join(gloVar.galleryOriginImgPath, id)
    print(originImgPath)
    return send_from_directory(originImgPath, imgName, as_attachment=True)