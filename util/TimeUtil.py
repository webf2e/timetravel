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

def getTimestrampNow():
    return int(datetime.datetime.now().timestamp() * 1000)