from flask import Flask,request,abort
from route.QuestionRoute import questionRoute
from route.PasswordRoute import passwordRoute
from route.IndexRoute import indexRoute
from route.MemoryRoute import memoryRoute
from route.TravelRoute import travelRoute
from route.AdminRoute import adminRoute
from route.GalleryRoute import galleryRoute
from route.LocationRoute import locationRoute
from route.SettingRoute import settingRoute
from route.AppRoute import appRoute
from route.SpecialDayRoute import specialDayRoute
from route.AnniversaryRoute import anniversaryRoute
from route.MessageRoute import messageRoute
from route.ServerRoute import serverRoute
from service import InitService
from datetime import timedelta
from flask_apscheduler import APScheduler
from sche.config import Config
from util import Log
import logging

app = Flask(__name__)

app.register_blueprint(questionRoute)
app.register_blueprint(passwordRoute)
app.register_blueprint(indexRoute)
app.register_blueprint(memoryRoute)
app.register_blueprint(travelRoute)
app.register_blueprint(adminRoute)
app.register_blueprint(galleryRoute)
app.register_blueprint(locationRoute)
app.register_blueprint(appRoute)
app.register_blueprint(settingRoute)
app.register_blueprint(specialDayRoute)
app.register_blueprint(anniversaryRoute)
app.register_blueprint(messageRoute)
app.register_blueprint(serverRoute)

@app.route('/')
def login():
    isLogin = request.cookies.get('isLogin')
    ua = str(request.headers.get("user-agent"))
    ipad = ua.find("iPad") != -1
    isIphone = not ipad and ua.find("iPhone") != -1
    isAndroid = ua.find("Android") != -1
    isMobile = isIphone or isAndroid;
    logging.warning("isMobile:{}".format(isMobile))
    if isLogin == None:
        if isMobile:
            return app.send_static_file("mobile/login.html")
        else:
            return app.send_static_file("login.html")
    else:
        if isMobile:
            return app.send_static_file("mobile/index.html")
        else:
            return app.send_static_file("index.html")

InitService.init()
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = 'lovejing'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config['MAX_CONTENT_LENGTH'] = 50*1024*1024
scheduler = APScheduler()
app.config.from_object(Config())
scheduler.init_app(app)
scheduler.start()
Log.init()
logging.warning("timeTravel服务启动")

#防盗链
@app.before_request
def before_request():
    try:
        url = request.url
        url = url.lower()
        if (url.endswith(".jpg") or url.endswith(".png") or
            url.endswith(".gif") or url.endswith(".jpeg") or
            url.endswith(".css") or url.endswith(".js") or
            url.endswith(".ico")):

            referer = request.headers.get("Referer")
            print("before_request,url:{}".format(url))
            print("before_request,referer:{}".format(referer))
        # if not (url in [
        #     "/static/upload/cdn/jetbrains/jetbrains-license-server-activating.png",
        #     "/static/upload/cdn/jetbrains/jetbrains-license-server-activated.png"
        # ] and referer == "http://jetbrains.license.laucyun.com/"):
        #     raise Exception("forbidden")
    except Exception as e:
        if str(e) == "forbidden":
            abort(403)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8010)

