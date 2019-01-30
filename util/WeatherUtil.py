import requests,json,logging
from bs4 import BeautifulSoup
from service import RedisService
from util.RedisKey import redisKey


#http://www.tianqihoubao.com/lishi/beijing/20190129.html

def getWeather(address,date):
    try:
        url = "http://www.tianqihoubao.com/lishi/{}/{}.html".format(address, date)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        div = soup.find(id="content")
        imgs = div.find_all("img")
        result = ""
        for img in imgs:
            name = img["src"]
            name = name[name.rfind("/") + 1:name.rfind(".")]
            result += name + "-"
        result = result[:-1]
        return result
    except Exception as e:
        print(e)
        return None

def getWeatherCity():
    domain = "http://www.tianqihoubao.com"
    url = "http://www.tianqihoubao.com/lishi/"
    r = requests.get(url)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text,"html.parser")
    hrefs = soup.find_all(class_="citychk")[0].find_all("a")
    for href in hrefs:
        if str(href).find("<b>") != -1:
            itemUrl = domain+href["href"]
            provinceCname = str(href.text).strip()
            logging.warning("当前加载天气的省份：%s" % provinceCname)
            r = requests.get(itemUrl)
            r.encoding = "utf-8"
            soup = BeautifulSoup(r.text,"html.parser")
            dls = soup.find_all(class_="citychk")[0].find_all("dl")
            jsonStr = "{"
            for dl in dls:
                cityCname = dl.find_all("dt")[0].text
                areas = dl.find_all("dd")[0].find_all("a")
                for area in areas:
                    areaName = str(area.text).strip()
                    finalName = cityCname
                    if cityCname != areaName:
                        finalName += areaName
                    areaEName = area["href"]
                    areaEName = areaEName[areaEName.rfind("/") + 1:areaEName.rfind(".")]
                    jsonStr += "\"" + finalName + "\":\"" + areaEName + "\","
            jsonStr = jsonStr[0:-1] + "}"
            logging.warning("天气城市数据为：%s" % jsonStr)
            RedisService.setMap(redisKey.weatherCityName,provinceCname,jsonStr)
