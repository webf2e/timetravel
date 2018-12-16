from flask import Blueprint,Response
import json
from util import TimeUtil

indexRoute = Blueprint('indexRoute', __name__)

@indexRoute.route('/getMeetingDays',methods=["POST"])
def getMeetingDays():
    timeList = []
    timeList.append("我们已经相遇{}天！".format(TimeUtil.subDay("2018-10-05 00:00:00")))
    timeList.append("我成为你的男朋友第{}天！".format(TimeUtil.subDay("2018-12-09 00:00:00")))
    return Response(json.dumps(timeList), mimetype='application/json')