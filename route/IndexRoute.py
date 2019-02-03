from flask import Blueprint,Response
import json,datetime
from util import TimeUtil,LunarUtil
from util.Global import gloVar

indexRoute = Blueprint('indexRoute', __name__)

@indexRoute.route('/getMeetingDays',methods=["POST"])
def getMeetingDays():
    timeList = []
    timeList.append("我们已经相遇{}天！".format(TimeUtil.subDay("2018-10-05 00:00:00")))
    timeList.append("我成为你的男朋友第{}天！".format(TimeUtil.subDay("2018-12-09 00:00:00")))
    return Response(json.dumps(timeList), mimetype='application/json')


@indexRoute.route('/isSpecialDay',methods=["POST"])
def isSpecialDay():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    date = "{}-{}-{}".format(year, month, day)
    md = "{}-{}".format(month, day)
    if md in gloVar.specialDay:
        return Response(gloVar.specialDay[md], mimetype='application/json')
    else:
        md = LunarUtil.getLunar(date)
        if md in gloVar.specialDay:
            return Response(gloVar.specialDay[md], mimetype='application/json')
        else:
            return Response("None", mimetype='application/json')
