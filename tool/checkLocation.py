import requests,json,time,os
from util import LocationUtil

path = "/home/liuwenbin/location/"
filePathName = os.path.join(path,max(os.listdir(path)))
print(filePathName)
lines = open(filePathName, "r+")
lastLon = 0
lastLat = 0
lastTime = 0
lastAddr = ""
count = 0
for line in lines:
    try:
        line = line.strip()
        if "" == line:
            continue
        line = line.replace("'", "\"")
        jsonObj = json.loads(line)
        if lastLon == 0:
            lastLon = jsonObj["lon"]
            lastLat = jsonObj["lat"]
            lastTime = jsonObj["timestramp"]
            lastAddr = jsonObj["locationDescribe"]
            print(line)
            continue
        timeDelay = (jsonObj["timestramp"] - lastTime) // 1000
        distance = int(LocationUtil.getDistance(jsonObj["lon"],jsonObj["lat"],lastLon,lastLat))
        if timeDelay <= 0:
            continue
        speed = int((distance / timeDelay))
        if speed > 111:
            # print("{} 时间：{}s，距离：{}m，速度：{}m/s，从{}到{}".format("跳过", timeDelay, distance, speed, lastAddr,jsonObj["locationDescribe"]))
            count += 1
            continue
        #print("时间：{}s，距离：{}m，速度：{}m/s，从{}到{}".format(timeDelay,distance,speed,lastAddr,jsonObj["locationDescribe"]))
        lastLon = jsonObj["lon"]
        lastLat = jsonObj["lat"]
        lastTime = jsonObj["timestramp"]
        lastAddr = jsonObj["locationDescribe"]
        print(line)
    except Exception as e:
        print(e)
lines.close()

print("去掉了{}个点".format(count))