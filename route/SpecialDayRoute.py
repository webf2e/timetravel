from flask import Blueprint
from flask import abort,request,Response
from service import RedisService,SpecialDayService
import datetime,json

specialDayRoute = Blueprint('specialDayRoute', __name__)

@specialDayRoute.route('/getSpecialDay',methods=["POST"])
def getSpecialDay():
    now = datetime.datetime.now()
    dateStr = datetime.datetime.strftime(now,"%Y-%m-%d")
    redisKey = "special_{}".format(dateStr)
    specialStr = RedisService.get(redisKey)
    specialJson = json.loads(specialStr)
    word = "{} {}|{}".format(specialJson["specialHead"], specialJson["message"], specialJson["color"])
    return word