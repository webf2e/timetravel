from flask import Blueprint
from flask import session,request,Response
import os
from util.Global import gloVar
import json
from service import TravelService

travelRoute = Blueprint('travelRoute', __name__)

@travelRoute.route('/getAllPoint',methods=["POST"])
def getAllPoint():
    return Response(TravelService.getAllPoint(), mimetype='application/json')

@travelRoute.route('/getTravelTimeGroup',methods=["POST"])
def getTravelTimeGroup():
    return Response(TravelService.getTravelTimeGroup(), mimetype='application/json')

@travelRoute.route('/getNew4',methods=["POST"])
def getNew4():
    return Response(TravelService.getNew4(), mimetype='application/json')

@travelRoute.route('/getByLonLat',methods=["POST"])
def getByLonLat():
    lon = request.form.get("lon");
    lat = request.form.get("lat");
    return Response(TravelService.getByLonLat(lon,lat), mimetype='application/json')

@travelRoute.route('/getByDate',methods=["POST"])
def getByDate():
    date = request.form.get("date");
    print(date)
    return Response(TravelService.getByDate(date), mimetype='application/json')