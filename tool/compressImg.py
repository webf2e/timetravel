from PIL import Image
import os

def compress(inImgName,outImgName):
    image = Image.open(inImgName)
    image.save(outImgName, quality=20)

path = "/home/liuwenbin/PycharmProjects/timetravel/static/gallery"
fs = os.listdir(path)
for f in fs:
    tdir = os.path.join(path,f)
    files = os.listdir(tdir)
    for file in files:
        imgName = os.path.join(tdir,file)
        print(imgName)
        #compress(imgName,imgName)
