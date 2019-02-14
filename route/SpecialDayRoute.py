from flask import Blueprint
from flask import abort,request,Response
from service import RedisService,SpecialWordService
import datetime,json

specialDayRoute = Blueprint('specialDayRoute', __name__)

@specialDayRoute.route('/getSpecialDay',methods=["POST"])
def getSpecialDay():
    now = datetime.datetime.now()
    dateStr = datetime.datetime.strftime(now,"%Y年%m月%d日")
    redisKey = "special_{}".format(dateStr)
    if RedisService.isExist(redisKey):
        return Response(RedisService.get(redisKey), mimetype='application/json')
    else:
        result = SpecialWordService.getByDate(dateStr)
        print(result)
        if len(result) == 0:
            result = "{}"
        RedisService.setWithTtl(redisKey, result, 60 * 60 * 24)
        return Response(result, mimetype='application/json')

@specialDayRoute.route('/getAllSpecialDay',methods=["POST"])
def getAllSpecialDay():
    now = datetime.datetime.now()
    dateStr = datetime.datetime.strftime(now,"%Y-%m-%d")
    return Response(SpecialWordService.getAllByBelowDate(dateStr), mimetype='application/json')