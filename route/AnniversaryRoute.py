from flask import Blueprint
from flask import abort,request,Response
from service import AnniversaryService
from util import TimeUtil
import json,datetime

anniversaryRoute = Blueprint('anniversaryRoute', __name__)


@anniversaryRoute.route('/getAllAnniversary',methods=["POST"])
def getAllAnniversary():
    jsonStr = AnniversaryService.getAllAnniversary()
    jsonObj = json.loads(jsonStr)
    for jo in jsonObj:
        jo["delay"] = TimeUtil.subDay(jo["time"].replace("年","-")
                        .replace("月","-").replace("日"," ") + "00:00:00")
    return Response(json.dumps(jsonObj), mimetype='application/json')