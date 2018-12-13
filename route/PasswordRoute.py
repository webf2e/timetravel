from flask import Blueprint
from flask import session,request,Response
from service import PasswordService
import json,logging
from util import TimeUtil
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
    if(uuidInRequest == uuidInServer):
        currentPwd = PasswordService.getCurrentPassword()
        logging.warning("currentPwd:"+str(currentPwd))
        isReset = False
        if(len(currentPwd) == 0):
            isReset = True
        elif TimeUtil.getIntervalSecond(currentPwd[0][2],datetime.datetime.now()) > 3 * 86400:
            isReset = True
            PasswordService.resetAllPassword()
            logging.warning("重置所有密码")
        if isReset:
            PasswordService.updateRandomPassword()
            logging.warning("更新随机密码")
            currentPwd = PasswordService.getCurrentPassword()
            logging.warning("当前密码为：" + str(currentPwd))
        result["password"] = currentPwd[0][1]
    logging.warning(result)
    return Response(json.dumps(result, ensure_ascii=False), mimetype='application/json')

@passwordRoute.route('/login',methods=["POST"])
def login():
    password = str(request.form.get("password"))
    currentPwdInDb = PasswordService.getCurrentPassword()
    logging.warning("currentPwd:" + str(currentPwdInDb))
    if(len(currentPwdInDb) == 0):
        return Response("password_overtime")
    currentPwdInDb = currentPwdInDb[0]
    if(password != currentPwdInDb[1]):
        return Response("password_error")
    if(TimeUtil.getIntervalSecond(currentPwdInDb[2],datetime.datetime.now()) > 3 * 86400):
        return Response("password_overtime")
    res = Response("success")
    if request.cookies.get('isLogin') == None:
        logging.warning("设置cookie")
        outdate = datetime.datetime.now() + datetime.timedelta(days=3)
        res.set_cookie("isLogin","OK",expires=outdate)
    return res