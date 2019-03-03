import os,logging
import traceback,requests
from PIL import Image
import pytesseract
from util.Global import gloVar
import jieba,time
#import matplotlib.pyplot as plt
from wordcloud import WordCloud
import random
from util import ImgUtil

def renameAndMove(dirPath):
    try:
        files = os.listdir(dirPath)
        for file in files:
            fileName = str(file)
            if os.path.isdir(os.path.join(dirPath, fileName)):
                continue
            if not fileName.startswith("20"):
                continue;
            end = fileName[fileName.rfind("_"):]
            newFileName = fileName
            if len(end) == 6:
                afterEnd = end.replace("_", "_0")
                newFileName = fileName.replace(end, afterEnd)
                logging.warning("{} -> {}".format(fileName, newFileName))
                os.rename(os.path.join(dirPath, fileName), os.path.join(dirPath, newFileName))
            #转移文件夹
            fileNames = newFileName.split("_")
            dPath = os.path.join(dirPath, fileNames[0], fileNames[1], fileNames[2])
            logging.warning(dPath)
            if not os.path.exists(dPath):
                os.makedirs(dPath)
            os.rename(os.path.join(dirPath, newFileName), os.path.join(dPath, newFileName))
    except Exception as e:
        logging.warning("move chat fileError",traceback.format_exc())


def resizeImg(file,width,height):
    img = Image.open(file)
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save(file)

def getText(filePath):
    text=pytesseract.image_to_string(Image.open(filePath),lang='chi_sim')
    logging.warning(text)

def getGalleryImgByMonth(ids):
    list = []
    for id in ids:
        list = list + getGalleryImgPathById(id)
    return list

def getGalleryImgPathById(id):
    filePath = []
    dirPath = os.path.join(gloVar.galleryImgPath, str(id))
    if(not os.path.exists(dirPath)):
        return filePath
    files = os.listdir(dirPath)
    files.sort()
    for file in files:
        filePath.append(os.path.join("/static/gallery",str(id),file))
    return filePath

def compressImg(path):
    im = Image.open(path)
    im.save(path, 'JPEG', quality=80)

def rotateImg(path):
    im = Image.open(path)
    out = im.transpose(Image.ROTATE_90)
    out.save(path)

def makeCloudWord(w,imgPath):
    cut = jieba.cut(w)
    words = ' '.join(cut)
    wordcloud = WordCloud(background_color="white", max_words=2000, scale=20,
                          max_font_size=120, random_state=42,
                          font_path=gloVar.wordCloudFontPath).generate(words)
    #plt.imshow(wordcloud)
    wordcloud.to_file(imgPath)

def clearStaticDownloadFiles():
    filePath = os.path.join(gloVar.staticPath, "download")
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    else:
        files = os.listdir(filePath)
        for file in files:
            os.remove(os.path.join(filePath,file))

def makeHeartImg():
    #获取了所有的图片
    multiple = 3
    totalImgCount = 47
    imgList = []
    travelIds = os.listdir(gloVar.galleryImgPath)
    flag = True
    while flag:
        for travelId in travelIds:
            img = random.sample(os.listdir(os.path.join(gloVar.galleryImgPath, travelId)), 1)
            img = os.path.join(gloVar.galleryImgPath, travelId, img[0])
            if img not in imgList:
                imgList.append(img)
                if len(imgList) == totalImgCount:
                    flag = False
                    break
    #获取宽高比
    whMap = {}
    for imgPath in imgList:
        percent = ImgUtil.getWHPercent(imgPath)
        if percent in whMap:
            list = whMap[percent]
        else:
            list = []
        list.append(imgPath)
        whMap[percent] = list
    #读取配置文件
    configFilePath = os.path.join(os.path.dirname(gloVar.staticPath), "config", "heartLocation.config")
    lines = open(configFilePath, "r")
    im = Image.open(os.path.join(gloVar.staticPath, "images", "bkimage.jpg"))
    #im = Image.new("RGBA",(2040,1785))
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        line = line.replace("\t", ",")
        vals = line.split(",")
        width = int(vals[2]) * multiple
        height = int(vals[3]) * multiple
        mask = (int(vals[0]) * multiple, int(vals[1]) * multiple, width + int(vals[0]) * multiple, height + int(vals[1]) * multiple)
        imgPath,key = getCommonImg(whMap,width,height)
        l = whMap[key]
        l.remove(imgPath)
        if len(l) == 0:
            whMap.pop(key)
        else:
            whMap[key] = l
        img = getCorrectImg(imgPath, width, height)
        im.paste(img, mask)
    im.save(os.path.join(gloVar.staticPath, "images", "bigHeart.png"))
    lines.close()

def getCommonImg(whMap,width,height):
    percent = round(width / height, 2)
    pList = []
    for per in whMap.keys():
        pList.append(abs(percent - per))
    pList.sort()
    if (pList[0] + percent) in whMap:
        key = (pList[0] + percent)
    elif (pList[0] - percent) in whMap:
        key = (pList[0] - percent)
    else:
        key = (percent - pList[0])
    return (random.sample(whMap[key],1)[0],key)

def getCorrectImg(imgPath,width,height):
    img = Image.open(imgPath)
    imgWidth = img.size[0]
    imgHeight = img.size[1]
    wPercent = imgWidth / width
    hPercent = imgHeight / height
    if wPercent < hPercent:
        img = img.resize((int(imgWidth / wPercent), int(imgHeight / wPercent)), Image.ANTIALIAS)
        x = 0
        y = int(imgHeight / wPercent / 2 - height / 2)
        height = height + y
    else:
        img = img.resize((int(imgWidth / hPercent), int(imgHeight / hPercent)), Image.ANTIALIAS)
        x = int(imgWidth / hPercent / 2 - width / 2)
        y = 0
        width = width + x
    img = img.crop((x,y,width,height))
    return img

def writeSystemTongji(type,hour,data):
    filePath = os.path.join(gloVar.systemTongjiPath,type)
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    f = open(os.path.join(filePath, "{}-{}.txt".format(type,hour)),"a+")
    f.write(data + "\n")
    f.close()

def readSystemTongji(type,fileName):
    list = []
    f = open(os.path.join(gloVar.systemTongjiPath, type, fileName),"r+")
    for line in f:
        line = line.strip()
        if line == "":
            continue
        list.append(line.split("\t"))
    f.close()
    return list

def getSystemTongji(type,startTime,endTime):
    list = []
    filePath = os.path.join(gloVar.systemTongjiPath, type)
    files = os.listdir(filePath)
    files.sort()
    isStart = False
    for file in files:
        if file.find(startTime) != -1:
            isStart = True
        if isStart:
            list += readSystemTongji(type, file)
        if file.find(endTime) != -1:
            isStart = False
    return list

def removeSystemTongjiFile(maxcount):
    typePaths = os.listdir(gloVar.systemTongjiPath)
    for typePath in typePaths:
        filePath = os.path.join(gloVar.systemTongjiPath, typePath)
        files = os.listdir(filePath)
        files.sort()
        if len(files) > maxcount:
            os.remove(os.path.join(filePath, files[0]))

def removeLocationFile(maxcount):
    locationFiles = os.listdir(gloVar.locationPath)
    locationFiles.sort()
    if len(locationFiles) > maxcount:
        os.remove(os.path.join(gloVar.locationPath, locationFiles[0]))

def getLastLocationInFile():
    list = os.listdir(gloVar.locationPath)
    filePath = os.path.join(gloVar.locationPath, max(list))
    datas = open(filePath, "r+")
    for data in datas:
        data = data.strip()
        if "" == data:
            continue
        lastLocation = data
    lastLocation = lastLocation.replace("'", "\"")
    lastLocation = lastLocation.replace("lon", "longitude")
    lastLocation = lastLocation.replace("lat", "latitude")
    return lastLocation

def downloadFile(url,filePath):
    r = requests.get(url)
    with open(filePath, "wb") as code:
        code.write(r.content)

def downloadWeatherImg(weather,filePath):
    ws = weather.split("-")
    for w in ws:
        imgUrl = "http://www.tianqihoubao.com/legend/{}.gif".format(w)
        filePathAndName = os.path.join(filePath,"{}.gif".format(w))
        if os.path.exists(filePathAndName):
            continue
        downloadFile(imgUrl, filePathAndName)

def downloadWeatherImgUseLoop():
    while True:
        filePath = "/home/liuwenbin/Desktop/program/wi"
        files = os.listdir(filePath)
        for file in files:
            if file.find("_1") != -1:
                file = file.replace("_1", "")
            else:
                file = file.replace(".gif", "_1.gif")
            if file in files:
                continue
            imgUrl = "http://www.tianqihoubao.com/legend/{}".format(file)
            print("下载：{}".format(file))
            downloadFile(imgUrl, os.path.join(filePath, file))
        time.sleep(1)