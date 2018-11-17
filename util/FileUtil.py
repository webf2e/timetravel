import os
import traceback
from PIL import Image
import pytesseract
from util.Global import gloVar

def renameAndMove(dirPath):
    try:
        files = os.listdir(dirPath)
        for file in files:
            fileName = str(file)
            if os.path.isdir(os.path.join(dirPath, fileName)):
                continue
            if not fileName.startswith("20"):
                continue;
            end = fileName[fileName.rfind("_"):]
            newFileName = fileName
            if len(end) == 6:
                afterEnd = end.replace("_", "_0")
                newFileName = fileName.replace(end, afterEnd)
                print("{} -> {}".format(fileName, newFileName))
                os.rename(os.path.join(dirPath, fileName), os.path.join(dirPath, newFileName))
            #转移文件夹
            fileNames = newFileName.split("_")
            dPath = os.path.join(dirPath, fileNames[0], fileNames[1], fileNames[2])
            print(dPath)
            if not os.path.exists(dPath):
                os.makedirs(dPath)
            os.rename(os.path.join(dirPath, newFileName), os.path.join(dPath, newFileName))
    except Exception as e:
        print("move chat fileError",traceback.format_exc())


def resizeImg(file,width,height):
    img = Image.open(file)
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save(file)

def getText(filePath):
    text=pytesseract.image_to_string(Image.open(filePath),lang='chi_sim')
    print(text)

def getGalleryImgByMonth(datas):
    month2Img = {}
    for data in datas:
        month = data[1]
        id = data[0]
        if month in month2Img:

            list = month2Img[month]
        else:
            list = []
        list = list + getGalleryImgPathById(id)
        month2Img[month] = list
    return month2Img

def getGalleryImgPathById(id):
    filePath = []
    dirPath = os.path.join(gloVar.galleryImgPath,str(id))
    if(not os.path.exists(dirPath)):
        return filePath
    files = os.listdir(dirPath)
    files.sort()
    for file in files:
        filePath.append(os.path.join("/static/gallery",str(id),file))
    return filePath

def compressImg(path):
    files = os.listdir(path)
    for file in files:
        if file.startswith("gallery-") and file.endswith(".jpg"):
            im = Image.open(os.path.join(path,file))
            im.save("/home/liuwenbin/Desktop/"+file, 'JPEG', quality=40)

compressImg("../static/images")