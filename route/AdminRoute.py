from flask import Blueprint
from flask import abort,request,Response
import os,oss2
from util.Global import gloVar
import json
from service import TravelService,ChatService,RedisService,SpecialDayService,AnniversaryService,TravelWeatherService,QuestionService,MessageService
from util import FileUtil,NetInfoUtil,TongjiUtil,TimeUtil,ImgUtil,SmsUtil
import datetime
import logging
from util.RedisKey import redisKey

adminRoute = Blueprint('adminRoute', __name__)

@adminRoute.route('/admin/upChatImg',methods=["POST"])
def upChatImg():
    #先判断文件夹下有没有文件，如果有就等一下
    RedisService.setWithTtl(redisKey.moveChatImgFlag,"1",30)
    for f in os.listdir(gloVar.chatDirPath):
        if(os.path.isfile(os.path.join(gloVar.chatDirPath, f))):
            return "稍等一下，暂时有文件没有转移"
    files = str(request.files)
    print("上传聊天图片：{}".format(files))
    date = str(request.form.get("date"))
    dates = date.split("_")
    index = 0
    #先判断文件夹是否存在
    filePath = os.path.join(gloVar.chatDirPath, dates[0], dates[1], dates[2])
    if os.path.exists(filePath):
        if len(os.listdir(filePath)) != 0:
            index = str(max(os.listdir(filePath)))
            index = int(index[index.rfind("_") + 1:index.rfind(".")])
    else:
        os.makedirs(filePath)
    count = 0
    for i in range(0,2):
        typeName = "file{}".format(i)
        if files.rfind("'{}'".format(typeName)) == -1:
            print("上传聊天图片：{}，continue".format(typeName))
            continue
        file = request.files[typeName]
        index += 1
        file.save(os.path.join(gloVar.chatDirPath, "{}_{}.png".format(date, index)))
        count += 1
    return '成功上传{}个文件'.format(count)

@adminRoute.route('/admin/getLastChatImg',methods=["POST"])
def getLastChatImg():
    year = sorted(os.listdir(gloVar.chatDirPath))[-1]
    month = sorted(os.listdir(os.path.join(gloVar.chatDirPath, year)))[-1]
    date = sorted(os.listdir(os.path.join(gloVar.chatDirPath, year, month)))[-1]
    pic = sorted(os.listdir(os.path.join(gloVar.chatDirPath, year, month, date)))[-1]
    result = {}
    result["year"] = year
    result["month"] = month
    result["date"] = date
    result["pic"] = pic
    return Response(json.dumps(result, ensure_ascii=False), mimetype='application/json')

@adminRoute.route('/admin/showImages',methods=["POST"])
def showImages():
    date = request.form.get("date")
    dates = date.split("_")
    filePath = os.path.join(gloVar.chatDirPath, dates[0], dates[1], dates[2])
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
    print(TravelService.getAllTravelNames())
    return Response(TravelService.getAllTravelNames(), mimetype='application/json')

@adminRoute.route('/admin/getTravelInfoById',methods=["POST"])
def getTravelInfoById():
    id = request.form.get("id")
    travels = json.loads(TravelService.getTravelInfoById(id))
    for travel in travels:
        travel["delay"] = TimeUtil.subDay(travel["travelTime"]) - 1
        del travel["travelId"]
        del travel["weatherId"]
    return Response(json.dumps(travels), mimetype='application/json')

@adminRoute.route('/admin/upTravelIndexImg',methods=["POST"])
def upTravelIndexImg():
    id = str(request.form.get("id"))
    file = request.files["file"]
    filePath = os.path.join(gloVar.travelIndexImgPath, "{}.png".format(id))
    file.save(filePath)
    FileUtil.resizeImg(filePath, 300, 260)
    TravelService.updateImgBy(id, os.path.join("/static/travelIndexImg","{}.png".format(id)))
    return "文件上传成功"

@adminRoute.route('/admin/changeWeather',methods=["POST"])
def changeWeather():
    id = request.form.get("id")
    dayIcon = request.form.get("weatherDay")
    nightIcon = request.form.get("weatherNight")
    weatherDay = json.loads(gloVar.weatherNames)[dayIcon]
    weatherNight = json.loads(gloVar.weatherNames)[nightIcon[:-2]]
    minTemp = request.form.get("minTemp")
    maxTemp = request.form.get("maxTemp")
    # 更新相同地点和日期的其他景点的天气
    travelInfo = json.loads(TravelService.getTravelInfoById(id))[0]
    travelTime = travelInfo["travelTime"]
    travelTime = travelTime.split(" ")[0]
    travels = TravelService.getByCityAndDate(travelInfo["country"], travelInfo["province"], travelInfo["city"],travelTime)
    travels = json.loads(travels)
    for t in travels:
        #判断id是否在travelWeather中(travelId)，如果在就更新，不在就添加
        travelWeathers = TravelWeatherService.getByTravelId(t["id"])
        if len(travelWeathers) > 0:
            #更新
            TravelWeatherService.update(dayIcon, nightIcon, weatherDay, weatherNight, maxTemp, minTemp,t["id"])
        else:
            #添加
            TravelWeatherService.insert(dayIcon,nightIcon,weatherDay,weatherNight,maxTemp,minTemp,t["id"])
    return "天气更新成功"


@adminRoute.route('/admin/addTravelInfo',methods=["POST"])
def addTravelInfo():
    travelName = request.form.get("travelName")
    type = request.form.get("type")
    content = request.form.get("content")
    lon = request.form.get("lon")
    lat = request.form.get("lat")
    travelTime = request.form.get("travelTime")
    keyword = request.form.get("keyword")
    movieName = request.form.get("movieName")
    foodType = request.form.get("foodType")
    movieType = ""
    weekDay = TimeUtil.getWeekNumByDate(travelTime)
    holiday = TimeUtil.getHoliday(travelTime.split(" ")[0])
    if "" != movieName:
        movieType = NetInfoUtil.getMovieType(movieName)
    TravelService.insert(travelName,type,content,lon,lat,travelTime,keyword,movieName,foodType,movieType,weekDay,holiday)
    TravelService.updateMostDirection()
    TongjiUtil.getTravelTongji()
    TravelService.updateCountryToDistrict()
    TravelService.updateTrack(travelTime.split(" ")[0])
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
    keyword = request.form.get("keyword")
    movieName = request.form.get("movieName")
    foodType = request.form.get("foodType")
    movieType = ""
    weekDay = TimeUtil.getWeekNumByDate(travelTime)
    holiday = TimeUtil.getHoliday(travelTime.split(" ")[0])
    if "" != movieName:
        movieType = NetInfoUtil.getMovieType(movieName)
    TravelService.updateById(id,travelName,type,content,lon,lat,travelTime,keyword,movieName,foodType,movieType,weekDay,holiday)
    TravelService.updateMostDirection()
    TongjiUtil.getTravelTongji()
    TravelService.updateCountryToDistrict()
    TravelService.updateTrack(travelTime.split(" ")[0])
    return "修改成功"

@adminRoute.route('/admin/tongji/getChatImageCount',methods=["POST"])
def getChatImageCount():
    imgCountMap = {}
    years = os.listdir(gloVar.chatDirPath)
    years.sort()
    for year in years:
        months = os.listdir(os.path.join(gloVar.chatDirPath, year))
        months.sort()
        for month in months:
            days = os.listdir(os.path.join(gloVar.chatDirPath, year, month))
            days.sort()
            for day in days:
                images = os.listdir(os.path.join(gloVar.chatDirPath, year, month, day))
                imgCountMap["{}-{}-{}".format(year,month,day)] = len(images)
    return Response(json.dumps(imgCountMap, ensure_ascii=False), mimetype='application/json')

@adminRoute.route('/admin/tongji/getChatTimes',methods=["POST"])
def getChatTimes():
    timeCountMap = {}
    times = ChatService.getChatTimes()
    for time in times:
        if time[0].find(",") != -1:
            ts = time[0].split(",")
            for t in ts:
                if t not in timeCountMap:
                    timeCountMap[t] = 1
                else:
                    timeCountMap[t] = timeCountMap[t] + 1
        else:
            if time[0] not in timeCountMap:
                timeCountMap[time[0]] = 1
            else:
                timeCountMap[time[0]] = timeCountMap[time[0]] + 1
    json = "["
    list = []
    for k in timeCountMap.keys():
        list.append(k)
    list.sort()
    for t in list:
        json += "{\"time\":\""+t+"\",\"count\":"+str(timeCountMap[t])+"},"
    json = json[:-1] + "]"
    return Response(json, mimetype='application/json')


@adminRoute.route('/admin/tongji/getContent',methods=["POST"])
def getContent():
    resultMap = {}
    contents = TravelService.getContent()
    wordCount = 0
    w = ""
    for content in contents:
        wordCount += len(content[0])
        w += content[0] + "。"
    resultMap["wordCount"] = wordCount
    fileName = "wordcloud.png"
    #FileUtil.makeCloudWord(w, os.path.join(gloVar.staticPath, "images", fileName))
    resultMap["wordCloudPath"] = os.path.join("/static/images",fileName)
    return Response(json.dumps(resultMap, ensure_ascii=False), mimetype='application/json')

@adminRoute.route('/admin/tongji/getGalleryCount',methods=["POST"])
def getGalleryCount():
    resultMap = {}
    galleryImgCount = 0
    gallerys = os.listdir(gloVar.galleryImgPath)
    resultMap["galleryCount"] = len(gallerys)
    for galleryDir in gallerys:
        galleryImgCount += len(os.listdir(os.path.join(gloVar.galleryImgPath, galleryDir)))
    resultMap["galleryImgCount"] = galleryImgCount
    return Response(json.dumps(resultMap, ensure_ascii=False), mimetype='application/json')

@adminRoute.route('/admin/tongji/getOSSFile',methods=["POST"])
def getOSSFile():
    auth = oss2.Auth('LTAIOWHFyQYc3gQN', 'kkN3gdS3x32g4etD7lpYbNnpYZmlmr')
    bucket = oss2.Bucket(auth, 'http://oss-cn-hongkong-internal.aliyuncs.com', 'timetravelbak')
    fileInOss = {}
    for obj in oss2.ObjectIterator(bucket, delimiter='/'):
        fileInOss[obj.key] = bucket.get_object_meta(obj.key).headers['Content-Length']
    return Response(json.dumps(fileInOss, ensure_ascii=False), mimetype='application/json')

@adminRoute.route('/admin/tongji/downloadOSSFile',methods=["POST"])
def downloadOSSFile():
    resultMap = {}
    fileName = str(request.form.get("fileName"))
    fileName = fileName.replace("_"," ")
    FileUtil.clearStaticDownloadFiles()
    auth = oss2.Auth('LTAIOWHFyQYc3gQN', 'kkN3gdS3x32g4etD7lpYbNnpYZmlmr')
    bucket = oss2.Bucket(auth, 'http://oss-cn-hongkong-internal.aliyuncs.com', 'timetravelbak')
    bucket.get_object_to_file(fileName, os.path.join(gloVar.staticPath, "download", fileName.replace(" ", "")))
    resultMap["filePath"] = os.path.join("/static/download",fileName.replace(" ",""))
    resultMap["fileName"] = fileName
    return Response(json.dumps(resultMap, ensure_ascii=False), mimetype='application/json')

@adminRoute.route('/admin/upGalleryImg',methods=["POST"])
def upGalleryImg():
    id = str(request.form.get("id"))
    gallery = request.files["file"]
    originFilePath = os.path.join(gloVar.galleryOriginImgPath, id)
    filePath = os.path.join(gloVar.galleryImgPath, id)
    if not os.path.exists(originFilePath):
        os.makedirs(originFilePath)
    originImgPath = os.path.join(originFilePath, gallery.filename)
    imgPath = os.path.join(filePath, gallery.filename)
    gallery.save(originImgPath)
    #将原始图片保存到缩略图中
    ImgUtil.compress(originImgPath,imgPath)
    TongjiUtil.getTravelTongji()
    return os.path.join("/static/gallery",id,gallery.filename)

@adminRoute.route('/admin/upGalleryImgTar',methods=["POST"])
def upGalleryImgTar():
    file = request.files["file"]
    originImgPath = os.path.join("/root", file.filename)
    logging.warning("originImgPath:"+originImgPath)
    file.save(originImgPath)
    return "OK"

@adminRoute.route('/admin/deleteChatImg',methods=["POST"])
def deleteChatImg():
    path = str(request.form.get("path"))
    path = os.path.join(gloVar.chatDirPath, path.replace("/static/chatImg/", ""))
    os.remove(path)
    return "删除成功"

@adminRoute.route('/admin/rotateImg',methods=["POST"])
def rotateImg():
    path = str(request.form.get("path"))
    degree = int(request.form.get("degree"))
    absPath = os.path.join(gloVar.galleryImgPath, path.replace("/static/gallery/", ""))
    originAbsPath = os.path.join(gloVar.galleryOriginImgPath, path.replace("/static/gallery/", ""))
    FileUtil.rotateImgByDegree(absPath,degree)
    FileUtil.rotateImgByDegree(originAbsPath,degree)
    return path

@adminRoute.route('/admin/getGalleryByIdAndPage',methods=["POST"])
def getGalleryByIdAndPage():
    id = str(request.form.get("id"))
    page = int(request.form.get("page"))
    dirPath = os.path.join(gloVar.galleryImgPath, id)
    if(not os.path.exists(dirPath)):
        return Response("{}", mimetype='application/json')
    imgs = os.listdir(dirPath)
    imgCount = len(imgs)
    if(imgCount == 0):
        return Response("{}", mimetype='application/json')
    if page < 1:
        page = imgCount
    if page > imgCount:
        page = 1
    img = imgs[page - 1]
    result = {}
    result["path"] = os.path.join("/static/gallery/",id,img)
    result["pageNum"] = page
    result["totalCount"] = imgCount
    return Response(json.dumps(result, ensure_ascii=False), mimetype='application/json')

@adminRoute.route('/admin/deleteGalleryImg',methods=["POST"])
def deleteGalleryImg():
    path = str(request.form.get("path"))
    realPath = path.replace("/static/gallery/", "")
    smallPath = os.path.join(gloVar.galleryImgPath, realPath)
    originPath = os.path.join(gloVar.galleryOriginImgPath, realPath)
    try:
        os.remove(smallPath)
    except Exception as e:
        print(e)
    try:
        os.remove(originPath)
    except Exception as e:
        print(e)
    TongjiUtil.getTravelTongji()
    return "删除成功"

@adminRoute.route('/admin/system/cpu',methods=["POST"])
def systemCPU():
    startTime = request.form.get("startTime")
    endTime = request.form.get("endTime")
    if startTime == '' or startTime == None:
        startTime = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(hours=1),"%Y-%m-%d-%H")
    if endTime == '' or endTime == None:
        endTime = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d-%H")
    return Response(json.dumps(FileUtil.getSystemTongji("cpu",startTime,endTime), ensure_ascii=False), mimetype='application/json')

@adminRoute.route('/admin/system/disk',methods=["POST"])
def systemDisk():
    startTime = request.form.get("startTime")
    endTime = request.form.get("endTime")
    if startTime == '' or startTime == None:
        startTime = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(hours=1), "%Y-%m-%d-%H")
    if endTime == '' or endTime == None:
        endTime = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d-%H")
    return Response(json.dumps(FileUtil.getSystemTongji("disk",startTime,endTime), ensure_ascii=False), mimetype='application/json')

@adminRoute.route('/admin/system/memory',methods=["POST"])
def systemMemory():
    startTime = request.form.get("startTime")
    endTime = request.form.get("endTime")
    if startTime == '' or startTime == None:
        startTime = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(hours=1), "%Y-%m-%d-%H")
    if endTime == '' or endTime == None:
        endTime = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d-%H")
    return Response(json.dumps(FileUtil.getSystemTongji("memory",startTime,endTime), ensure_ascii=False), mimetype='application/json')

@adminRoute.route('/admin/system/net',methods=["POST"])
def systemNet():
    startTime = request.form.get("startTime")
    endTime = request.form.get("endTime")
    netId = request.form.get("netId")
    if startTime == '' or startTime == None:
        startTime = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(hours=1), "%Y-%m-%d-%H")
    if endTime == '' or endTime == None:
        endTime = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d-%H")
    return Response(json.dumps(FileUtil.getSystemTongji("net-{}".format(netId),startTime,endTime), ensure_ascii=False), mimetype='application/json')

@adminRoute.route('/admin/tongji/getServerStartTime',methods=["POST"])
def getServerStartTime():
    return RedisService.get(redisKey.serverStartTime)

@adminRoute.route('/admin/getWeatherList',methods=["POST"])
def getWeatherList():
    return Response(gloVar.weatherNames,mimetype='application/json')

@adminRoute.route('/admin/addAnniversaryDay',methods=["POST"])
def addAnniversaryDay():
    time = request.form.get("time")
    content = request.form.get("content")
    dateTime = time.replace("年","-").replace("月","-").replace("日"," ") + "00:00:00"
    AnniversaryService.insert(time,content,dateTime)
    return "添加成功"

@adminRoute.route('/admin/editAnniversaryDay',methods=["POST"])
def editAnniversaryDay():
    time = request.form.get("time")
    content = request.form.get("content")
    dateTime = time.replace("年","-").replace("月","-").replace("日"," ") + "00:00:00"
    AnniversaryService.updateByTime(time,content,dateTime)
    return "修改成功"

@adminRoute.route('/admin/getAllAnniversaryTime',methods=["POST"])
def getAllAnniversaryTime():
    return Response(AnniversaryService.getAllAnniversaryTime(), mimetype='application/json')

@adminRoute.route('/admin/getAnniversaryByTime',methods=["POST"])
def getAnniversaryByTime():
    time = request.form.get("time")
    return Response(AnniversaryService.getByDate(time), mimetype='application/json')

@adminRoute.route('/admin/getAllQuestion',methods=["POST"])
def getAllQuestion():
    questions = QuestionService.getAll()
    return Response(questions, mimetype='application/json')

@adminRoute.route('/admin/updateQuestion',methods=["POST"])
def updateQuestion():
    id = request.form.get("id")
    question = request.form.get("question")
    answer = request.form.get("answer")
    if id == "0":
        #添加
        QuestionService.insert(question,answer)
        return "添加成功"
    else:
        #更新
        QuestionService.update(question,answer,id)
        return "修改成功"

@adminRoute.route('/admin/compressGallery',methods=["POST"])
def compressGallery():
    id = str(request.form.get("id"))
    #查看有没有origin目录
    originPath = os.path.join(gloVar.galleryOriginImgPath,id)
    galleryPath = os.path.join(gloVar.galleryImgPath,id)
    if not os.path.exists(originPath):
        return "该地点没有原始图片"
    if not os.path.exists(galleryPath):
        os.mkdir(galleryPath)
    originImgs = os.listdir(originPath)
    for originImg in originImgs:
        try:
            ImgUtil.compress(os.path.join(originPath, originImg), os.path.join(galleryPath, originImg))
        except Exception as e:
            print("ERROR:{}".format(e))
    return "压缩成功"

@adminRoute.route('/admin/addMessage',methods=["POST"])
def adminAddMessage():
    message = request.form.get("msg")
    now = datetime.datetime.now()
    dateTime = datetime.datetime.strftime(now,"%Y-%m-%d %H:%M:%S")
    # 添加短信通知
    SmsUtil.sendSmsBytempId(gloVar.notifyMobile,146624)
    MessageService.insert(message,dateTime,1)
    #修改redis中保存的值
    redisKey = "special_{}".format(datetime.datetime.strftime(now, "%Y-%m-%d"))
    specialStr = RedisService.get(redisKey)
    result = json.loads(specialStr)
    result["message"] = message
    RedisService.setWithTtl(redisKey, json.dumps(result), 60 * 60 * 25)
    return "留言成功"

@adminRoute.before_request
def print_request_info():
    urlPath = str(request.path)
    if(urlPath.find("admin") != -1 and urlPath.find("upGalleryImgTar") == -1):
        agent = str(request.headers.get("User-agent"))
        logging.warning("访问admin的agent：{}".format(agent))
        if(agent.find("MI 9 Transparent Edition") == -1):
            if gloVar.isCheck400 == "1":
                abort(400)