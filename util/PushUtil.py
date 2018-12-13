import requests
import logging
import hashlib
import json
from util import TimeUtil
#coding=utf-8


def getAuthCode():
    headers = {"Content-Type": "application/json"}
    url = "https://restapi.getui.com/v1/{}/auth_sign".format("5J6x0OXyjQ76886EHpixH6")
    timestramp = str(TimeUtil.getTimestrampNow())
    originStr = "{}{}{}".format("j1zfq7NGar5UTyZOc02PB5",timestramp,"WbkzEe9bJ68xZOc46MuCl2")
    sha256 = hashlib.sha256()
    sha256.update(originStr.encode('utf-8'))
    sign = sha256.hexdigest()
    data = "{\"sign\":\""+sign+"\",\"timestamp\":\""+timestramp+"\",\"appkey\":\"j1zfq7NGar5UTyZOc02PB5\"}"
    res = requests.post(url=url,data=data,headers=headers)
    return json.loads(res.text)["auth_token"]

def pushToSingle(title,content,touchuan,clientId="90d5c0eeddef90dab99583952d289f52"):
    headers = {"Content-Type": "application/json","authtoken":getAuthCode()}
    data = """
        {
           "message": {
           "appkey": "j1zfq7NGar5UTyZOc02PB5",
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
    """ %(content.encode("utf-8").decode("latin1"),
          title.encode("utf-8").decode("latin1"),
          touchuan.encode("utf-8").decode("latin1"),
          clientId,str(TimeUtil.getTimestrampNow()))
    logging.warning("推送的请求参数：{}".format(data))
    pushUrl = "https://restapi.getui.com/v1/{}/push_single".format("5J6x0OXyjQ76886EHpixH6")
    r = requests.post(url=pushUrl,data=data,headers=headers)
    logging.warning("推送的相应结果：{}".format(r.text))