import os
import traceback
from PIL import Image

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