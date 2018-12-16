import requests
import json, logging
from service import RedisService

service_id = 207270
entity_name = "你的小可爱"
ak = "fd2PMcjfqa7hRP0xoqGta5w2IODQ2kig"

def addPoint(jsonData):
    url = "http://yingyan.baidu.com/api/v3/track/addpoint"
    data = {}
    data["ak"] = ak
    data["service_id"] = service_id
    data["entity_name"] = entity_name
    data["latitude"] = jsonData["lat"]
    data["longitude"] = jsonData["lon"]
    data["loc_time"] = jsonData["timestramp"] // 1000
    data["coord_type_input"] = "bd09ll"
    data["dataSource"] = "baidu"
    if "height" in jsonData:
        data["height"] = jsonData["height"]

    if "radius" in jsonData:
        data["radius"] = jsonData["radius"]

    if "addr" in jsonData:
        data["addr"] = jsonData["addr"]

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

    if "time" in jsonData:
        data["time"] = jsonData["time"]

    results = requests.post(url, data=json.loads(str(data).replace("'","\""))).text
    return json.loads(results)

def getLatestPoint():
    data = RedisService.get("lastLocationFromBaidu")
    if None != data:
        logging.warning("从缓存中获取")
        return json.loads(json.dumps(eval(str(data))))
    url = "http://yingyan.baidu.com/api/v3/track/getlatestpoint?service_id={}&entity_name={}&coord_type_output=bd09ll&" \
          "process_option=need_denoise=1,radius_threshold=80,need_mapmatch=0,transport_mode=auto&ak={}"\
        .format(service_id,entity_name,ak)
    results = requests.get(url).text
    results = results.replace("latitude","lat")\
        .replace("longitude","lon")\
        .replace("loc_time","timestramp")
    RedisService.setWithTtl("lastLocationFromBaidu", results, 10)
    return json.loads(results)

def getDistance(startTime,endTime):
    url = "http://yingyan.baidu.com/api/v3/track/getdistance?ak={}&service_id={}&entity_name={}&is_processed=1&" \
          "process_option=need_denoise=1,radius_threshold=80,need_mapmatch=0,transport_mode=auto&" \
          "supplement_mode=walking&low_speed_threshold=20&start_time={}&end_time={}" \
        .format(ak, service_id, entity_name, startTime, endTime)
    results = requests.get(url).text
    return json.loads(results)

def getTrack(startTime,endTime,pageIndex,pageSize):
    url = "http://yingyan.baidu.com/api/v3/track/gettrack?ak={}&service_id={}&entity_name={}&is_processed=1&" \
          "process_option=need_denoise=1,need_vacuate=1,radius_threshold=80,need_mapmatch=1,transport_mode=auto&" \
          "supplement_mode=walking&low_speed_threshold=20&coord_type_output=bd09ll&sort_type=asc&" \
          "start_time={}&end_time={}&page_index={}&page_size={}" \
        .format(ak, service_id, entity_name, startTime, endTime, pageIndex, pageSize)
    results = requests.get(url).text
    return json.loads(results)


def getStayPoint(startTime,endTime,stayTime,stayRadius):
    url = "http://yingyan.baidu.com/api/v3/analysis/staypoint?ak={}&service_id={}&entity_name={}&" \
          "start_time={}&end_time={}&stay_time={}&stay_radius={}&coord_type_output=bd09ll&" \
          "process_option=need_denoise=1,need_vacuate=1,radius_threshold=80,need_mapmatch=0,transport_mode=auto" \
        .format(ak, service_id, entity_name, startTime, endTime, stayTime, stayRadius)
    results = requests.get(url).text
    return json.loads(results)