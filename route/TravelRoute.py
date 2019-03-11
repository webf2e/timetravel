from flask import Blueprint
from flask import request,Response
from service import TravelService,RedisService
from util import TimeUtil
import json


travelRoute = Blueprint('travelRoute', __name__)

@travelRoute.route('/getAllPoint',methods=["POST"])
def getAllPoint():
    return Response(TravelService.getAllPoint(), mimetype='application/json')

@travelRoute.route('/getTravelTimeGroup',methods=["POST"])
def getTravelTimeGroup():
    return Response(TravelService.getTravelTimeGroup(), mimetype='application/json')

@travelRoute.route('/getNew5',methods=["POST"])
def getNew5():
    travels = json.loads(TravelService.getNew5())
    for travel in travels:
        travel["delay"] = TimeUtil.subDay(travel["travelTime"]) - 1
        travel["travelTime"] = travel["travelTime"][:-3]
        del travel["travelId"]
        del travel["weatherId"]
    return Response(json.dumps(travels), mimetype='application/json')

@travelRoute.route('/getTravelInfoById',methods=["POST"])
def getTravelInfoById():
    id = request.form.get("id")
    if id == None or id == "":
        return Response("{}", mimetype='application/json')
    travels = json.loads(TravelService.getTravelInfoById(id))
    for travel in travels:
        travel["delay"] = TimeUtil.subDay(travel["travelTime"]) - 1
        travel["travelTime"] = travel["travelTime"][:-3]
        del travel["travelId"]
        del travel["weatherId"]
    return Response(json.dumps(travels), mimetype='application/json')

@travelRoute.route('/getByLonLat',methods=["POST"])
def getByLonLat():
    lon = request.form.get("lon")
    lat = request.form.get("lat")
    travels = json.loads(TravelService.getByLonLat(lon,lat))
    for travel in travels:
        travel["delay"] = TimeUtil.subDay(travel["travelTime"]) - 1
        travel["travelTime"] = travel["travelTime"][:-3]
        del travel["travelId"]
        del travel["weatherId"]
    return Response(json.dumps(travels), mimetype='application/json')

@travelRoute.route('/getByDate',methods=["POST"])
def getByDate():
    date = request.form.get("date")
    print(date)
    travels = json.loads(TravelService.getByDate(date))
    for travel in travels:
        travel["delay"] = TimeUtil.subDay(travel["travelTime"]) - 1
        travel["travelTime"] = travel["travelTime"][:-3]
        del travel["travelId"]
        del travel["weatherId"]
    return Response(json.dumps(travels), mimetype='application/json')

@travelRoute.route('/getTravelTongji',methods=["POST"])
def getTravelTongji():
    return Response(RedisService.getTongji("travel"), mimetype='application/json')