from flask import Flask,request
from route.QuestionRoute import questionRoute
from route.PasswordRoute import passwordRoute
from route.IndexRoute import indexRoute
from route.MemoryRoute import memoryRoute
from route.TravelRoute import travelRoute
from route.AdminRoute import adminRoute
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

@app.route('/')
def login():
    isLogin = request.cookies.get('isLogin')
    print("isLogin:{}".format(isLogin))
    if isLogin == None:
        return app.send_static_file("login.html")
    else:
        return app.send_static_file("index.html")

InitService.init()
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = 'lovejing'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
scheduler = APScheduler()
app.config.from_object(Config())
scheduler.init_app(app)
scheduler.start()
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8010)

