from service import TravelService
from service import RedisService
from util.Global import gloVar
import os

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
