from util.Global import gloVar
import datetime,os,json
from util import TimeUtil

def isInPoly(aLon, aLat, pointList):
    '''
    :param aLon: double 经度
    :param aLat: double 纬度
    :param pointList: list [(lon, lat)...] 多边形点的顺序需根据顺时针或逆时针，不能乱
    '''

    iSum = 0
    iCount = len(pointList)

    if (iCount < 3):
        return False

    for i in range(iCount):

        pLon1 = pointList[i][0]
        pLat1 = pointList[i][1]

        if (i == iCount - 1):

            pLon2 = pointList[0][0]
            pLat2 = pointList[0][1]
        else:
            pLon2 = pointList[i + 1][0]
            pLat2 = pointList[i + 1][1]

        if ((aLat >= pLat1) and (aLat < pLat2)) or ((aLat >= pLat2) and (aLat < pLat1)):

            if (abs(pLat1 - pLat2) > 0):

                pLon = pLon1 - ((pLon1 - pLon2) * (pLat1 - aLat)) / (pLat1 - pLat2);

                if (pLon < aLon):
                    iSum += 1

    if (iSum % 2 != 0):
        return True
    else:
        return False

def getFenceState(lon,lat):
    result = {}
    for fenceName,fencePoints in gloVar.fences.items():
        state = isInPoly(lon,lat,fencePoints)
        if state:
            state = 1
        else:
            state = 0
        result[fenceName] = state
    return result

def compareState(lastState,state):
    result = {}
    for name,oldState in lastState.items():
        if state[name] != oldState:
            result[name] = state[name]
    return result

def locationTongji():
    dateFormatStr = "%Y-%m-%d"
    timeFormatStr = "%H:%M"
    currentDate = datetime.datetime.strftime(datetime.datetime.now(),dateFormatStr)
    files = os.listdir(gloVar.locationPath)
    files.sort()
    addrCountMap = {}
    addrTimestrampMap = {}
    tongjiEndTime = ""
    for file in files:
        if not file.startswith(currentDate):
            continue
        filePath = os.path.join(gloVar.locationPath, file)
        lines = open(filePath,"r+")
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
            #添加addrCountMap
            if locationDescribe in addrCountMap:
                addrCountMap[locationDescribe] = addrCountMap[locationDescribe] + 1
            else:
                addrCountMap[locationDescribe] = 1
            #添加addrTime
            if locationDescribe in addrTimestrampMap:
                addrTimestrampMap[locationDescribe][1] = jsonData["timestramp"]
            else:
                addrTimestrampMap[locationDescribe] = [jsonData["timestramp"],jsonData["timestramp"]]
            tongjiEndTime = jsonData["time"]
    countList = []
    for count in addrCountMap.values():
        countList.append(int(count))
    countList.sort(reverse=True)
    #获取top3
    if len(countList) > 3:
        countList = countList[0:3]
    result = {}
    addrMap = {}
    #获取每个地点的时间
    for c in countList:
        for addr,count in addrCountMap.items():
            if c == count:
                times = addrTimestrampMap[addr]
                delay = times[1] - times[0]
                addrMap[addr] = [TimeUtil.getTimeStrFromTimestramp(times[0],timeFormatStr),
                                  TimeUtil.getTimeStrFromTimestramp(times[1],timeFormatStr), delay]
                break
    result["data"] = addrMap
    result["tongjiTime"] = tongjiEndTime
    return result