from flask import Blueprint
from flask import session,request,Response
import os
from util.Global import gloVar
import json
from service import TravelService

adminRoute = Blueprint('adminRoute', __name__)

@adminRoute.route('/admin/upFile',methods=["POST"])
def upFile():
    #先判断文件夹下有没有文件，如果有就等一下
    for f in os.listdir(gloVar.chatDirPath):
        if(os.path.isfile(os.path.join(gloVar.chatDirPath,f))):
            return "稍等一下，暂时有文件没有转移"
    files = str(request.files)
    date = str(request.form.get("date"))
    dates = date.split("_")
    index = 0;
    #先判断文件夹是否存在
    filePath = os.path.join(gloVar.chatDirPath,dates[0],dates[1],dates[2])
    if os.path.exists(filePath):
        index = str(max(os.listdir(filePath)))
        index = int(index[index.rfind("_")+1:index.rfind(".")])
    else:
        os.makedirs(filePath)
    count = 0
    for i in range(0,100):
        typeName = "file{}".format(i)
        if files.rfind("'{}'".format(typeName)) == -1:
            continue
        file = request.files[typeName]
        fn = str(file.filename)
        if not fn.lower().endswith("png"):
            continue
        index += 1
        file.save(os.path.join(gloVar.chatDirPath, "{}_{}.png".format(date,index)))
        count += 1
    return '上传成功{}个文件'.format(count)
