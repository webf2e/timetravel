import requests
import logging
import hashlib
import json
from util import TimeUtil
from service import RedisService
from util.RedisKey import redisKey
#coding=utf-8

appId = "5J6x0OXyjQ76886EHpixH6"
appKey = "j1zfq7NGar5UTyZOc02PB5"
masterSecret = "WbkzEe9bJ68xZOc46MuCl2"


def getAuthCode():
    headers = {"Content-Type": "application/json"}
    url = "https://restapi.getui.com/v1/{}/auth_sign".format(appId)
    timestramp = str(TimeUtil.getTimestrampNow())
    originStr = "{}{}{}".format(appKey,timestramp,masterSecret)
    sha256 = hashlib.sha256()
    sha256.update(originStr.encode('utf-8'))
    sign = sha256.hexdigest()
    data = "{\"sign\":\""+sign+"\",\"timestamp\":\""+timestramp+"\",\"appkey\":\""+appKey+"\"}"
    res = requests.post(url=url,data=data,headers=headers)
    return json.loads(res.text)["auth_token"]

def pushToSingle(title,content,touchuan,clientId=RedisService.getSetting(redisKey.cid)):
    headers = {"Content-Type": "application/json","authtoken":getAuthCode()}
    title = "【爱的小窝】 {}".format(title)
    data = """
        {
           "message": {
           "appkey": "%s",
           "is_offline": true,
           "offline_expire_time":10000000,
           "msgtype": "notification"
        },
        "notification": {
            "style": {
                "type": 0,
                "text": "%s",
                "title": "%s"
            },
            "transmission_type": true,
            "transmission_content": "%s"
        },
        "cid": "%s",
        "requestid": "%s"
    }
    """ %(appKey,content.encode("utf-8").decode("latin1"),
          title.encode("utf-8").decode("latin1"),
          touchuan.encode("utf-8").decode("latin1"),
          clientId,str(TimeUtil.getTimestrampNow()))
    logging.warning("推送的请求参数：{}".format(data))
    pushUrl = "https://restapi.getui.com/v1/{}/push_single".format(appId)
    r = requests.post(url=pushUrl,data=data,headers=headers)
    logging.warning("推送的相应结果：{}".format(r.text))


def getUserStatus(clientId=RedisService.getSetting(redisKey.cid)):
    headers = {"Content-Type": "application/json","authtoken":getAuthCode()}
    pushUrl = "https://restapi.getui.com/v1/{}/user_status/{}".format(appId,clientId)
    r = requests.get(url=pushUrl,headers=headers)
    logging.warning("获取用户状态结果：{}".format(r.text))