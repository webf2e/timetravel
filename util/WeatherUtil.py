import requests,json,logging,datetime,time,random,os
from bs4 import BeautifulSoup
from service import RedisService
from util.RedisKey import redisKey

#http://www.tianqihoubao.com/lishi/beijing/20190129.html

def getWeather(address,date):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
        url = "http://www.tianqihoubao.com/lishi/{}/{}.html".format(address, date)
        logging.warning("weather_url:{}".format(url))
        r = requests.get(url,headers)
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