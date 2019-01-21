from service import TravelService
from service import RedisService

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
    json = str(tongjiMap).replace("'", "\"")
    RedisService.setTongji("travel", json)
