import requests
from bs4 import BeautifulSoup

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

def _getWeatherCity():
    domain = "http://www.tianqihoubao.com"
    url = "http://www.tianqihoubao.com/lishi/"
    r = requests.get(url)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text,"html.parser")
    hrefs = soup.find_all(class_="citychk")[0].find_all("a")
    for href in hrefs:
        if str(href).find("<b>") != -1:
            itemUrl = domain+href["href"]
            r = requests.get(itemUrl)
            r.encoding = "utf-8"
            print(r.text)
            break

_getWeatherCity()