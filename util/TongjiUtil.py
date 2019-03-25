from service import TravelService
from service import RedisService
from util.Global import gloVar
import os,datetime,json,logging
from util import TimeUtil
from util.RedisKey import redisKey

def getTravelTongji():
    tongjiMap = {}
    movieTypes = TravelService.getAllMovieType()
    movieTypeCountMap = {}
    for movieType in movieTypes:
        movieType = movieType[0]
        if movieType == "暂无类型":
            continue
        mts = movieType.split(",")
        for mt in mts:
            if mt in movieTypeCountMap:
                movieTypeCountMap[mt] = movieTypeCountMap[mt] + 1
            else:
                movieTypeCountMap[mt] = 1
    maxMovieType = sorted(movieTypeCountMap,key=lambda x:movieTypeCountMap[x])[-1]
    maxMovieTypeCount = movieTypeCountMap[maxMovieType]
    tongjiMap["maxMovieType"] = maxMovieType
    tongjiMap["maxMovieTypeCount"] = maxMovieTypeCount
    tongjiMap["movieCount"] = len(movieTypes)

    foodTypes = TravelService.getAllFoodType()
    foodTypeCountMap = {}
    for foodType in foodTypes:
        foodType = foodType[0]
        fts = foodType.split(",")
        for ft in fts:
            if ft in foodTypeCountMap:
                foodTypeCountMap[ft] = foodTypeCountMap[ft] + 1
            else:
                foodTypeCountMap[ft] = 1
    maxFoodType = sorted(foodTypeCountMap, key=lambda x: foodTypeCountMap[x])[-1]
    maxFoodTypeCount = foodTypeCountMap[maxFoodType]
    tongjiMap["maxFoodType"] = maxFoodType
    tongjiMap["maxFoodTypeCount"] = maxFoodTypeCount
    tongjiMap["foodCount"] = len(foodTypes)
    #统计去了哪些景点
    travelTotalCount = TravelService.getTravelTotalCount()
    tongjiMap["travelTotalCount"] = travelTotalCount
    #统计哪些景点留下的照片
    travelPicPaths = os.listdir(gloVar.galleryImgPath)
    tongjiMap["travelHasPicCount"] = len(travelPicPaths)
    #一共有多少张图片
    maxPicCountTravelId = 0
    maxPicCountTravelCount = 0
    totalPicCount = 0
    for travelPicPath in travelPicPaths:
        travelId = travelPicPath
        travelPicPath = os.path.join(gloVar.galleryImgPath,travelPicPath)
        travelPicCount = len(os.listdir(travelPicPath))
        totalPicCount += travelPicCount
        if travelPicCount > maxPicCountTravelCount:
            maxPicCountTravelCount = travelPicCount
            maxPicCountTravelId = travelId
    tongjiMap["totalPicCount"] = totalPicCount
    tongjiMap["maxPicTravelId"] = maxPicCountTravelId
    tongjiMap["maxPicTravelName"] = TravelService.getTravelNameById(maxPicCountTravelId)
    tongjiMap["maxPicTravelCount"] = maxPicCountTravelCount
    json = str(tongjiMap).replace("'", "\"")
    RedisService.setTongji("travel", json)

def locationTongji():
    dateFormatStr = "%Y-%m-%d"
    timeFormatStr = "%H:%M"
    currentDate = datetime.datetime.strftime(datetime.datetime.now(), dateFormatStr)
    files = os.listdir(gloVar.locationPath)
    files.sort()
    addrTimestrampMap = {}
    addrDelayMap = {}
    addrLastTimeMap = {}
    addrLonLatMap = {}
    lastAddr = ""
    tongjiEndTime = ""
    maxTimestramp = 0
    heatMapPoint = {}
    for file in files:
        if not file.startswith(currentDate):
            continue
        filePath = os.path.join(gloVar.locationPath, file)
        lines = open(filePath, "r+")
        for line in lines:
            line = line.strip()
            if line.find("locationDescribe") == -1:
                continue
            jsonData = json.loads(json.dumps(eval(line)))
            locationDescribe = str(jsonData["locationDescribe"])
            if locationDescribe.startswith("在"):
                locationDescribe = locationDescribe[1:]
            if locationDescribe.endswith("附近"):
                locationDescribe = locationDescribe[:-2]
            # 添加addrTime
            if locationDescribe in addrTimestrampMap:
                addrTimestrampMap[locationDescribe][1] = jsonData["timestramp"]
            else:
                addrTimestrampMap[locationDescribe] = [jsonData["timestramp"], jsonData["timestramp"]]
            tongjiEndTime = jsonData["time"]
            # 添加添加addrLonLatMap
            if locationDescribe in addrLonLatMap:
                # 使用精度最高的数据
                if addrLonLatMap[locationDescribe][2] > jsonData["radius"]:
                    addrLonLatMap[locationDescribe] = [jsonData["lon"], jsonData["lat"], jsonData["radius"]]
            else:
                addrLonLatMap[locationDescribe] = [jsonData["lon"], jsonData["lat"], jsonData["radius"]]
            # 计算停留时间
            if "" == lastAddr:
                lastAddr = locationDescribe
                addrLastTimeMap[lastAddr] = jsonData["timestramp"]

            if lastAddr != locationDescribe:
                delay = jsonData["timestramp"] - addrLastTimeMap[lastAddr]
                if lastAddr in addrDelayMap:
                    addrDelayMap[lastAddr] = addrDelayMap[lastAddr] + delay
                else:
                    addrDelayMap[lastAddr] = delay
                addrLastTimeMap[locationDescribe] = jsonData["timestramp"]
            lastAddr = locationDescribe
            maxTimestramp = jsonData["timestramp"]
            #准备热力图数据
            heatMapLng = int(jsonData["lon"] * 100000) / 100000
            heatMapLat = int(jsonData["lat"] * 100000) / 100000
            key = "{}_{}".format(heatMapLng, heatMapLat)
            if key in heatMapPoint:
                heatPointData = heatMapPoint[key]
                heatPointData["count"] = heatPointData["count"] + 1
            else:
                heatPointData = {}
                heatPointData["lng"] = heatMapLng
                heatPointData["lat"] = heatMapLat
                heatPointData["count"] = 1
            heatMapPoint[key] = heatPointData
    delay = maxTimestramp - addrLastTimeMap[lastAddr]
    if lastAddr in addrDelayMap:
        addrDelayMap[lastAddr] = addrDelayMap[lastAddr] + delay
    else:
        addrDelayMap[lastAddr] = delay
    timeList = []
    for time in addrDelayMap.values():
        timeList.append(int(time))
        timeList.sort(reverse=True)
    # 获取top3
    if len(timeList) > 3:
        timeList = timeList[0:3]
    result = {}
    addrMap = {}
    # 获取每个地点的时间
    for t in timeList:
        for addr, time in addrDelayMap.items():
            if t == time:
                times = addrTimestrampMap[addr]
                addrMap[addr] = [TimeUtil.getTimeStrFromTimestramp(times[0], timeFormatStr),
                                 TimeUtil.getTimeStrFromTimestramp(times[1], timeFormatStr), addrDelayMap[addr],
                                 addrLonLatMap[addr][0], addrLonLatMap[addr][1], addrLonLatMap[addr][2]]
                break
    result["data"] = addrMap
    result["tongjiTime"] = tongjiEndTime
    #处理热力图数据
    result["points"] = list(heatMapPoint.values())
    logging.warning("位置统计结果：{}".format(result))
    RedisService.set(redisKey.locationTongji, json.dumps(result))