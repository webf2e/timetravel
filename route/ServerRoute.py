from flask import Blueprint
from flask import session,request
from util import PushUtil
import logging,datetime

serverRoute = Blueprint('serverRoute', __name__)

@serverRoute.route('/ssh/login',methods=["GET"])
def sshLogin():
    content = request.args.get("content")
    contents = content.split(",")
    user = contents[0]
    clientIp = contents[1]
    time = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
    PushUtil.pushToSingle("服务器登录", "{}_{}".format(user, clientIp), "")
    logging.warning("服务器通过ssh登录，登录用户：{}，登录客户端IP：{}，登录时间：{}".format(user, clientIp, time))
    return "OK"

#该接口供server项目调用，重启后，调用该接口判断是否重启成功
@serverRoute.route('/restart/check',methods=["GET"])
def restartCheck():
    return "OK"