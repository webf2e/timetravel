import datetime

def subTime(start):
    dateDelta = (datetime.datetime.now()-start)
    days = dateDelta.days
    seconds = dateDelta.seconds
    secondStr = dealSeconds(seconds)
    if (0 == days):
        return secondStr
    return "{}天{}".format(days,secondStr)

def subTime():
    start = datetime.datetime.strptime("2018-10-05 00:00:00", "%Y-%m-%d %H:%M:%S")
    dateDelta = (datetime.datetime.now()-start)
    days = dateDelta.days
    seconds = dateDelta.seconds
    secondStr = dealSeconds(seconds)
    if (0 == days):
        return secondStr
    return "{}天{}".format(days,secondStr)

def subDay():
    start = datetime.datetime.strptime("2018-10-05 00:00:00", "%Y-%m-%d %H:%M:%S")
    dateDelta = (datetime.datetime.now()-start)
    days = dateDelta.days
    return days + 1

def subDay(timestr):
    start = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
    dateDelta = (datetime.datetime.now()-start)
    days = dateDelta.days
    return days + 1

#获取持续的时分秒
def dealSeconds(seconds):
    if seconds < 60:
        return "{}秒".format(seconds)
    min = seconds // 60
    if min < 60:
        seconds = seconds - min * 60
        return "{}分{}秒".format(min, seconds)
    hour = min // 60
    min = (seconds - hour * 3600) // 60
    seconds = (seconds - hour * 3600 - min * 60)
    return "{}时{}分{}秒".format(hour, min, seconds)

def getIntervalSecond(startTimeStr,endTimeStr):
    return float((datetime.datetime.strptime(endTimeStr, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(startTimeStr, "%Y-%m-%d %H:%M:%S")).total_seconds())

def getIntervalSecond(startTime,endTime):
    return float((endTime - startTime).total_seconds())


def getTimeStrFromTimestramp(timestramp,format):
    return datetime.datetime.strftime(datetime.datetime.fromtimestamp(timestramp / 1000),format)

#获取当前时间的时间戳
def getTimestrampNow():
    return int(datetime.datetime.now().timestamp() * 1000)

#传入日期获取星期几
def getWeekNumByDate(date):
    weekDay = -1
    try:
        weekDay = datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S").weekday()
    except:
        print("日期转化失败")
    if weekDay == 0:
        return "星期一"
    elif weekDay == 1:
        return "星期二"
    elif weekDay == 2:
        return "星期三"
    elif weekDay == 3:
        return "星期四"
    elif weekDay == 4:
        return "星期五"
    elif weekDay == 5:
        return "星期六"
    elif weekDay == 6:
        return "星期日"
    return "未知"

#获取去年今日
def getCurrentDateLastYear():
    from dateutil.relativedelta import relativedelta
    return (datetime.datetime.now().date() - relativedelta(years=1)).strftime('%Y-%m-%d')