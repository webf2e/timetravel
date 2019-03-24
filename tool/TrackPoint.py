import os,json
from util import ImgUtil
from PIL import Image, ImageFilter

def resizeMapPointImg():
    path = "/home/liuwenbin/PycharmProjects/timetravel/static/images/points"

    files = os.listdir(path)
    for file in files:
        p = os.path.join(path, file)
        print(p)
        ImgUtil.resizeByPercent(Image.open(p), 1 / 5).save(p)

def getLineColor():
    fileName = "trackLineColor"
    lines = open(fileName,"r+")
    colors = {}
    for line in lines:
        line = line.strip()
        if "" == line:
            continue
        ls = line.split("\t")
        colors[ls[0]] = ls[1]
    print(json.dumps(colors))

#resizeMapPointImg()

getLineColor()