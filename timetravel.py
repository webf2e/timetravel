from flask import Flask,request
from route.QuestionRoute import questionRoute
from route.PasswordRoute import passwordRoute
from route.IndexRoute import indexRoute
from route.MemoryRoute import memoryRoute
from route.TravelRoute import travelRoute
from route.AdminRoute import adminRoute
from route.GalleryRoute import galleryRoute
from service import InitService
from datetime import timedelta
from flask_apscheduler import APScheduler
from sche.config import Config

app = Flask(__name__)

app.register_blueprint(questionRoute)
app.register_blueprint(passwordRoute)
app.register_blueprint(indexRoute)
app.register_blueprint(memoryRoute)
app.register_blueprint(travelRoute)
app.register_blueprint(adminRoute)
app.register_blueprint(galleryRoute)

# var ua = navigator.userAgent;
# var ipad = ua.match(/(iPad).*OS\s([\d_]+)/),
# isIphone =!ipad && ua.match(/(iPhone\sOS)\s([\d_]+)/),
# isAndroid = ua.match(/(Android)\s+([\d.]+)/),
# isMobile = isIphone || isAndroid;
@app.route('/')
def login():
    isLogin = request.cookies.get('isLogin')
    ua = str(request.headers.get("user-agent"))
    ipad = ua.find("iPad") != -1
    isIphone = not ipad and ua.find("iPhone") != -1
    isAndroid = ua.find("Android") != -1
    isMobile = isIphone or isAndroid;
    print("isMobile:{}".format(isMobile))
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
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8010)

