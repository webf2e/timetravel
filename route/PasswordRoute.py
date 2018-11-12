from flask import Blueprint
from flask import session,request,Response
from service import PasswordService
import json
from util import TimeUtil
from util.Global import gloVar
import datetime

passwordRoute = Blueprint('passwordRoute', __name__)

@passwordRoute.route('/s',methods=["POST"])
def sessionTest():
    session["uuid"] = 1
    return "ok"

@passwordRoute.route('/getPassword',methods=["POST"])
def getPassword():
    result={}
    uuidInServer = str(session["uuid"])
    uuidInRequest = str(request.form.get("uuid"))
    print("uuidInRequest:{}".format(uuidInRequest))
    print("uuidInServer:{}".format(uuidInServer))
    print(uuidInRequest == uuidInServer)
    if(uuidInRequest == uuidInServer):
        currentPwd = PasswordService.getCurrentPassword()
        print(currentPwd)
        isReset = False
        if(len(currentPwd) == 0):
            isReset = True
        elif TimeUtil.getIntervalSecond(currentPwd[0][2],datetime.datetime.now()) > 3 * 86400:
            isReset = True
            PasswordService.resetAllPassword()
        if isReset:
            PasswordService.updateRandomPassword()
            currentPwd = PasswordService.getCurrentPassword()
        result["password"] = currentPwd[0][1]
        gloVar.password = str(currentPwd[0][1])
        gloVar.passwordTime = currentPwd[0][2]
    print(result)
    return Response(json.dumps(result, ensure_ascii=False), mimetype='application/json')

@passwordRoute.route('/login',methods=["POST"])
def login():
    password = str(request.form.get("password"))
    if(gloVar.password == "" or password != gloVar.password):
        return Response("password_error")
    if(TimeUtil.getIntervalSecond(gloVar.passwordTime,datetime.datetime.now()) > 3 * 86400):
        return Response("password_overtime")
    res = Response("success")
    if request.cookies.get('isLogin') == None:
        print("设置cookie")
        outdate = datetime.datetime.now() + datetime.timedelta(days=3)
        res.set_cookie("isLogin","OK",expires=outdate)
    return res