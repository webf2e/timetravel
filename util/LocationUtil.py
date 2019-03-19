from util.Global import gloVar
import datetime,os,json,logging
from util import TimeUtil
import requests,json

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
    addrTimestrampMap = {}
    addrDelayMap = {}
    addrLastTimeMap = {}
    addrLonLatMap = {}
    lastAddr = ""
    tongjiEndTime = ""
    maxTimestramp = 0
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
            #添加addrTime
            if locationDescribe in addrTimestrampMap:
                addrTimestrampMap[locationDescribe][1] = jsonData["timestramp"]
            else:
                addrTimestrampMap[locationDescribe] = [jsonData["timestramp"],jsonData["timestramp"]]
            tongjiEndTime = jsonData["time"]
            #添加添加addrLonLatMap
            if locationDescribe in addrLonLatMap:
                #使用精度最高的数据
                if addrLonLatMap[locationDescribe][2] > jsonData["radius"]:
                    addrLonLatMap[locationDescribe] = [jsonData["lon"], jsonData["lat"], jsonData["radius"]]
            else:
                addrLonLatMap[locationDescribe] = [jsonData["lon"], jsonData["lat"], jsonData["radius"]]
            #计算停留时间
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
    delay = maxTimestramp - addrLastTimeMap[lastAddr]
    if lastAddr in addrDelayMap:
        addrDelayMap[lastAddr] = addrDelayMap[lastAddr] + delay
    else:
        addrDelayMap[lastAddr] = delay
    timeList = []
    for time in addrDelayMap.values():
        timeList.append(int(time))
        timeList.sort(reverse=True)
    #获取top3
    if len(timeList) > 3:
        timeList = timeList[0:3]
    result = {}
    addrMap = {}
    #获取每个地点的时间
    for t in timeList:
        for addr,time in addrDelayMap.items():
            if t == time:
                times = addrTimestrampMap[addr]
                addrMap[addr] = [TimeUtil.getTimeStrFromTimestramp(times[0],timeFormatStr),
                                  TimeUtil.getTimeStrFromTimestramp(times[1],timeFormatStr), addrDelayMap[addr],
                                 addrLonLatMap[addr][0], addrLonLatMap[addr][1], addrLonLatMap[addr][2]]
                break
    result["data"] = addrMap
    result["tongjiTime"] = tongjiEndTime
    logging.warning("位置统计结果：{}".format(result))
    return result

def getAddressByLonLat(lon,lat):
    keys = ["country", "province", "city", "district", "street"]
    result = {}
    url = "http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&location={},{}" \
          "&output=json&latest_admin=1&ak=0LSHte0xuZrXWUrnkEDIIMfwlOnYfiTA".format(lat,lon)
    r = requests.get(url)
    jsonStr = r.text
    jsonStr = jsonStr.replace("renderReverse&&renderReverse(","")[0:-1]
    logging.warning("getAddressByLonLat:{}".format(jsonStr))
    if jsonStr.find("addressComponent") == -1:
        for key in keys:
            result[key] = ""
        return result
    jsonObj = json.loads(jsonStr)
    jsonObj = jsonObj["result"]["addressComponent"]
    for key in keys:
        if key in jsonObj:
            result[key] = jsonObj[key]
        else:
            result[key] = ""
    return result

#orgData，上传上来的原始数据
def changeLocationData(orgData):
    dstData = {}
    if "e" in orgData:
        dstData["errorCode"] = orgData["e"]
    if "h" in orgData:
        dstData["height"] = orgData["h"]
    if "b" in orgData:
        dstData["lat"] = orgData["b"]
    if "ld" in orgData:
        dstData["locationDescribe"] = orgData["ld"]
    if "l" in orgData:
        dstData["lon"] = orgData["l"]
    if "r" in orgData:
        dstData["radius"] = orgData["r"]
    if "b" in orgData and "l" in orgData:
        cpcdData = getAddressByLonLat(orgData["l"],orgData["b"])
        dstData["country"] = cpcdData["country"]
        dstData["province"] = cpcdData["province"]
        dstData["city"] = cpcdData["city"]
        dstData["district"] = cpcdData["district"]
        dstData["street"] = cpcdData["street"]
        addr = cpcdData["country"]
        if cpcdData["province"] != cpcdData["city"]:
            addr += cpcdData["province"]
        addr += cpcdData["city"]
        addr += cpcdData["district"]
        addr += cpcdData["street"]
        dstData["addr"] = addr
    time = datetime.datetime.now()
    dstData["time"] = datetime.datetime.strftime(time,"%Y-%m-%d %H:%M:%S")
    dstData["timestramp"] = int(time.timestamp() * 1000)
    return dstData