from util.Global import gloVar
import configparser
import os
from service import TravelService

def init():
    print("doInit")
    configFilePath = os.path.join(os.getcwd(), "config/application.config")
    print("读取配置文件地址：%s" % configFilePath)
    if not os.path.exists(configFilePath):
        print("配置文件不存在，请检查")
        exit(0)
    conf = configparser.ConfigParser()
    conf.read(configFilePath, encoding="UTF-8")
    gloVar.chatDirPath = conf.get('ChatConfig', 'dirPath')
    gloVar.travelIndexImgPath = conf.get('TravelConfig', 'indexImgPath')
    gloVar.galleryImgPath = conf.get('GalleryConfig', 'galleryImgPath')
    gloVar.dbHost = conf.get('MysqlConfig', 'host')
    gloVar.dbUser = conf.get('MysqlConfig', 'user')
    gloVar.dbPwd = conf.get('MysqlConfig', 'password')
    gloVar.dbName = conf.get('MysqlConfig', 'db')
    gloVar.wordCloudFontPath = conf.get('wordCloudConfig', 'wordCloudFontPath')
    gloVar.staticPath = conf.get('staticConfig', 'staticPath')
    gloVar.systemTongjiPath = conf.get('systemConfig', 'systemTongjiPath')
    gloVar.locationPath = conf.get('locationConfig', 'locationPath')
    TravelService.updateMostDirection()
    #初始化围栏数据
    fencePoints = conf.get('fenceConfig', 'fencePoints')
    gloVar.notifyMobile = conf.get('fenceConfig', 'notifyMobile')
    fences = fencePoints.split("|")
    for fence in fences:
        name = fence[:fence.find(":")]
        points = fence[fence.find(":") + 1:].split(";")
        data = []

        for point in points:
            lonlat = point.split(",")
            lonlat = (float(lonlat[0]),float(lonlat[1]))
            data.append(lonlat)
        gloVar.fences[name] = data
