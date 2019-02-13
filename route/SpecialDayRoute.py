from flask import Blueprint
from flask import abort,request,Response
from service import RedisService,SpecialWordService
import datetime,json

specialDayRoute = Blueprint('specialDayRoute', __name__)

@specialDayRoute.route('/getSpecialDay',methods=["POST"])
def getSpecialDay():
    now = datetime.datetime.now()
    dateStr = datetime.datetime.strftime(now,"%Y年%m月%d日")
    # result= """{
    #     "time": "2019年02月04日",
    #     "word": "亲爱哒，我的一生有你相随，对你的牵挂成为一种幸福，我的人生旅途有你陪伴，是我前世修来的福气，执子之手，陪你到永久。宝贝，除夕快乐！",
    #     "themeColor": "#b65555",
    #     "festival": "2019年除夕"
    # }"""
    # result = "{}"
    # return Response(result, mimetype='application/json')
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