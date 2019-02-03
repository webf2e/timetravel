import requests,json,logging,datetime
# 获取当天的详细信息
appkey = "cd2606361b6637b355cc797820c37285"
def getLunar(date):
    try:
        url = "http://v.juhe.cn/calendar/day"
        params = {
            "key": appkey,  # 您申请的appKey
            "date": date,  # 指定日期,格式为YYYY-MM-DD,如月份和日期小于10,则取个位,如:2012-1-1
        }
        r = requests.post(url, data=params)
        return json.loads(r.text)["result"]["data"]["lunar"]
    except Exception as e:
        logging.warning("获取农历失败:{}",e)
        return None