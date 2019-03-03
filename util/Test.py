import requests,json,logging,datetime,time,random,os
from bs4 import BeautifulSoup

def downloadFile(url,filePath):
    r = requests.get(url,timeout=20)
    with open(filePath, "wb") as code:
        code.write(r.content)

def getWeather(address,date):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
        url = "http://www.tianqihoubao.com/lishi/{}/{}.html".format(address, date)
        r = requests.get(url,headers,timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        div = soup.find(id="content")
        imgs = div.find_all("img")
        result = ""
        for img in imgs:
            name = img["src"]
            name = name[name.rfind("/") + 1:name.rfind(".")]
            result += name + "-"
        result = result[:-1]
        fileWrite("weather_url:{}，time：{}，result：{}".format(url, datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S"),result))
        return result
    except Exception as e:
        print(e)
        return None

def fileWrite(content):
    file = open("weatherUrl.txt","a+")
    print(content)
    file.write(content+"\r\n")
    file.close()


def downloadWeatherImg(weather,filePath):
    ws = weather.split("-")
    for w in ws:
        imgUrl = "http://www.tianqihoubao.com/legend/{}.gif".format(w)
        filePathAndName = os.path.join(filePath,"{}.gif".format(w))
        if os.path.exists(filePathAndName):
            continue
        downloadFile(imgUrl, filePathAndName)

def getWeatherImg():
    timeout = 20
    domain = "http://www.tianqihoubao.com"
    url = "http://www.tianqihoubao.com/lishi/"
    print(url)
    r = requests.get(url,timeout=timeout)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text,"html.parser")
    hrefs = soup.find_all(class_="citychk")[0].find_all("a")
    for href in hrefs:
        try:
            if str(href).find("<b>") != -1:
                itemUrl = domain + href["href"]
                provinceCname = str(href.text).strip()
                logging.warning("当前加载天气的省份：%s" % provinceCname)
                r = requests.get(itemUrl,timeout=timeout)
                r.encoding = "utf-8"
                soup = BeautifulSoup(r.text, "html.parser")
                dls = soup.find_all(class_="citychk")[0].find_all("dl")
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
                        date = datetime.datetime.now()
                        print(areaName)
                        for i in range(1, 366):
                            try:
                                nowDate = date - datetime.timedelta(days=i)
                                nowDate = datetime.datetime.strftime(nowDate, "%Y%m%d")
                                weather = getWeather(areaEName, nowDate)
                                downloadWeatherImg(weather, "/home/liuwenbin/Desktop/program/wi/")
                            except Exception as e:
                                print(e)
        except Exception as e:
            print(e)

getWeatherImg()
