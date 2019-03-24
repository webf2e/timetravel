from flask import Blueprint
from flask import abort,request,Response
from service import RedisService,MessageService
import datetime,json

messageRoute = Blueprint('messageRoute', __name__)

@messageRoute.route('/getAllMessage',methods=["POST"])
def getAllMessage():
    return Response(MessageService.getAll(), mimetype='application/json')