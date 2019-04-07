from util.Global import gloVar
from util.RedisKey import redisKey
import configparser
import os,logging
from service import TravelService,RedisService,TravelWeatherService
import datetime,json
from util import EmailUtil,PDFUtil,TongjiUtil,WeatherUtil

def init():
    configFilePath = os.path.join(os.getcwd(), "config/application.config")
    logging.warning("读取配置文件地址：%s" % configFilePath)
    if not os.path.exists(configFilePath):
        logging.warning("配置文件不存在，请检查")
        exit(0)
    conf = configparser.ConfigParser()
    conf.read(configFilePath, encoding="UTF-8")
    gloVar.chatDirPath = conf.get('ChatConfig', 'dirPath')
    gloVar.travelIndexImgPath = conf.get('TravelConfig', 'indexImgPath')
    gloVar.galleryImgPath = conf.get('GalleryConfig', 'galleryImgPath')
    gloVar.galleryOriginImgPath = conf.get('GalleryConfig', 'galleryOriginImgPath')
    gloVar.dbHost = conf.get('MysqlConfig', 'host')
    gloVar.dbUser = conf.get('MysqlConfig', 'user')
    gloVar.dbPwd = conf.get('MysqlConfig', 'password')
    gloVar.dbName = conf.get('MysqlConfig', 'db')
    gloVar.wordCloudFontPath = conf.get('wordCloudConfig', 'wordCloudFontPath')
    gloVar.staticPath = conf.get('staticConfig', 'staticPath')
    gloVar.systemTongjiPath = conf.get('systemConfig', 'systemTongjiPath')
    gloVar.locationPath = conf.get('locationConfig', 'locationPath')
    gloVar.loggingFilePath = conf.get('loggingConfig', 'loggingFilePath')
    gloVar.isSendPageVisitMsg = conf.get('commonConfig', 'isSendPageVisitMsg')
    gloVar.isCheckRefer = conf.get('commonConfig', 'isCheckRefer')
    #更新最XX的位置信息
    #TravelService.updateMostDirection()
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
    #初始化setting
    if not RedisService.isSettingExist(redisKey.isNeedFenceInOutNotify):
        RedisService.setSetting(redisKey.isNeedFenceInOutNotify, "1")
    if not RedisService.isSettingExist(redisKey.isNeedLocationNotUpdateForSmsNotify):
        RedisService.setSetting(redisKey.isNeedLocationNotUpdateForSmsNotify, "1")
    if not RedisService.isSettingExist(redisKey.isNeedLocationNotUpdateForAppNotify):
        RedisService.setSetting(redisKey.isNeedLocationNotUpdateForAppNotify, "1")
    if not RedisService.isSettingExist(redisKey.isNeedAutoRestartForApp):
        RedisService.setSetting(redisKey.isNeedAutoRestartForApp, "1")
    #记录服务启动时间到redis中
    serverStartTime = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
    RedisService.set(redisKey.serverStartTime, serverStartTime)
    #更新travel表中的movieType类型
    #TravelService.updateMovieType()
    #TongjiUtil.getTravelTongji()
    #TravelService.updateCountryToDistrict()
    #TravelService.updateTrack("2019-03-31")
    #服务启动时发送邮件
    try:
        #EmailUtil.sendEmail("服务启动通知", "服务在{}启动".format(serverStartTime))
        #PDFUtil.makePdfForTravel()
        #更新travel表中所有weekDay字段为空的记录
        #TravelService.updateWeekDay()
        #更新travel表中所有holiday字段为null的记录
        #TravelService.updateHoliday()
        pass
    except Exception as e:
        logging.warning("发送邮件失败",e)