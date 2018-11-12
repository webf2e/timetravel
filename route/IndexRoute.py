from flask import Blueprint
from flask import session,request,Response
from service import PasswordService
import json
from util import TimeUtil
from util.Global import gloVar
import datetime

indexRoute = Blueprint('indexRoute', __name__)

@indexRoute.route('/getMeetingDays',methods=["POST"])
def getMeetingDays():
    return str(TimeUtil.subDay())