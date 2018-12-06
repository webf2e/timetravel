import requests
import json

def addPoint(jsonData):
    url = "http://yingyan.baidu.com/api/v3/track/addpoint"
    data = {}
    data["ak"] = "fd2PMcjfqa7hRP0xoqGta5w2IODQ2kig"
    data["service_id"] = 207270
    data["entity_name"] = "你的小可爱"
    data["latitude"] = jsonData["lat"]
    data["longitude"] = jsonData["lon"]
    data["loc_time"] = jsonData["timestramp"]
    data["coord_type_input"] = "bd09ll"
    if "height" in jsonData:
        data["height"] = jsonData["height"]

    if "radius" in jsonData:
        data["radius"] = jsonData["radius"]

    if "addr" in jsonData:
        data["address"] = jsonData["addr"]

    if "locationDescribe" in jsonData:
        data["locationDescribe"] = jsonData["locationDescribe"]

    if "country" in jsonData:
        data["country"] = jsonData["country"]

    if "province" in jsonData:
        data["province"] = jsonData["province"]

    if "city" in jsonData:
        data["city"] = jsonData["city"]

    if "district" in jsonData:
        data["district"] = jsonData["district"]

    if "street" in jsonData:
        data["street"] = jsonData["street"]

    if "errorCode" in jsonData:
        data["errorCode"] = jsonData["errorCode"]
    results = requests.post(url, data=json.loads(str(data).replace("'","\""))).text
    print(results)

jsonData={}
jsonData["lat"] = 40.07853
jsonData["lon"] = 116.25201
jsonData["city"] = "北京"
jsonData["timestramp"] = 1544009304000
addPoint(jsonData)