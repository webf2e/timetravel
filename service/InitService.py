from util.Global import gloVar
import configparser
import os

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