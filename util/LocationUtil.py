from util.Global import gloVar
import datetime,os,json,logging
from util import TimeUtil
import requests,json
from math import *

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

def getAddressByLonLat(lon,lat):
    keys = ["country", "province", "city", "district", "street"]
    result = {}
    url = "http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&location={},{}" \
          "&output=json&latest_admin=1&ak=0LSHte0xuZrXWUrnkEDIIMfwlOnYfiTA".format(lat,lon)
    print("locationUrl:{}".format(url))
    r = requests.get(url)
    jsonStr = r.text
    jsonStr = jsonStr.replace("renderReverse&&renderReverse(","")[0:-1]
    logging.warning("getAddressByLonLat:{}".format(jsonStr))
    if jsonStr.find("addressComponent") == -1:
        for key in keys:
            result[key] = ""
        result["sematic_description"] = ""
        return result
    jsonObj = json.loads(jsonStr)
    resultObj = jsonObj["result"]
    jsonObj = resultObj["addressComponent"]
    for key in keys:
        if key in jsonObj:
            result[key] = jsonObj[key]
        else:
            result[key] = ""

    if "sematic_description" in resultObj:
        result["sematic_description"] = resultObj["sematic_description"]
    else:
        result["sematic_description"] = ""
    print("locationResult:{}".format(result))
    return result

#orgData，上传上来的原始数据
def changeLocationData(dataStr):
    #e+"_"+b+"_"+l+"_"+h+"_"+r
    dstData = {}
    datas = dataStr.split("_")
    dstData["errorCode"] = int(datas[0])
    dstData["lat"] = float(datas[1])
    dstData["lon"] = float(datas[2])
    dstData["height"] = float(datas[3])
    dstData["radius"] = float(datas[4])

    cpcdData = getAddressByLonLat(dstData["lon"],dstData["lat"])
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
    if "sematic_description" in cpcdData:
        dstData["locationDescribe"] = cpcdData["city"]+cpcdData["district"]+cpcdData["sematic_description"]
    else:
        dstData["locationDescribe"] = dstData["addr"]
    time = datetime.datetime.now()
    dstData["time"] = datetime.datetime.strftime(time,"%Y-%m-%d %H:%M:%S")
    dstData["timestramp"] = int(time.timestamp() * 1000)
    return dstData


def rad(d):
    return d * pi / 180.0


def getDistance(lon_a, lat_a, lon_b, lat_b):
    if abs(lon_a - lon_b) < 0.000001 and abs(lat_a - lat_b) < 0.000001:
        return 0
    re = 6378140  # 赤道半径 (m)
    rp = 6356755  # 极半径 (m)
    oblateness = (re - rp) / re  # 地球扁率
    rad_lat_a = radians(lat_a)
    rad_lon_a = radians(lon_a)
    rad_lat_b = radians(lat_b)
    rad_lon_b = radians(lon_b)
    atan_a = atan(rp / re * tan(rad_lat_a))
    atan_b = atan(rp / re * tan(rad_lat_b))
    tmp = acos(sin(atan_a) * sin(atan_b) + cos(atan_a) * cos(atan_b) * cos(rad_lon_a - rad_lon_b))
    if tmp == 0:
        return 0
    c1 = (sin(tmp) - tmp) * (sin(atan_a) + sin(atan_b)) ** 2 / cos(tmp / 2) ** 2
    c2 = (sin(tmp) + tmp) * (sin(atan_a) - sin(atan_b)) ** 2 / sin(tmp / 2) ** 2
    dr = oblateness / 8 * (c1 - c2)
    distance = re * (tmp + dr)
    return distance