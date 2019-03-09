import requests,json,logging,datetime,time,random,os
from bs4 import BeautifulSoup

weatherMap = {}
weatherFile = "/home/liuwenbin/PycharmProjects/timetravel/util/weatherUrl.txt"
lines = open(weatherFile,"r+")
for line in lines:
    line = line.strip()
    if line == "":
        continue
    weather = line.split("result：")[1]
    weathers = weather.split("-")
    weatherUrl = line.replace("weather_url:","").split("，time")[0]
    if weathers[0].find("nopic") == -1:
        weatherMap[weathers[0]] = weatherUrl
    if weathers[1].find("nopic") == -1:
        weatherMap[weathers[1]] = weatherUrl

def getWeatherCNameFromUrl(url,weather):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
    r = requests.get(url, headers, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    imgs = soup.find_all("img")
    cName = ""
    for img in imgs:
        if(str(img).find(weather) != -1):
            cName = img["alt"]
    return cName

path = "/home/liuwenbin/Desktop/program/wi/"
files = sorted(os.listdir(path))
finalMap = {}
for file in files:
    weather = file.replace(".gif","")
    if weather in weatherMap:
        url = weatherMap[weather]
        print(url)
        cName = getWeatherCNameFromUrl(url,weather)
        if weather.find("_1") != -1:
            weather = weather.replace("_1","")
        if weather not in finalMap:
            finalMap[weather] = cName
    else:
        print(weather)

print(finalMap)

