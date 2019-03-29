import os

path = "../"

fileContentMap = {}
imgs = {}
def getContent(path):
    if os.path.isfile(path):
        if path.endswith("html") or path.endswith("js") or path.endswith("css") or path.endswith("py"):
            content = ""
            lines = open(path,"r+")
            for line in lines:
                content += line
            fileContentMap[path] = content
        elif path.lower().endswith("gif") or path.lower().endswith("png") or path.lower().endswith("jpg") or path.lower().endswith("jpeg"):
            imgs[path] = path[path.rfind("/") + 1:]

    else:
        files = os.listdir(path)
        for file in files:
            getContent(os.path.join(path,file))

getContent(path)
for imgPath,imgName in imgs.items():
    isUse = False
    for filePath,content in fileContentMap.items():
        if content.find(imgName) != -1:
            isUse = True
            break
    if isUse:
        #print("图片{}在{}文件中使用".format(imgPath,filePath))
        pass
    else:
        print("图片{}没有被使用".format(imgPath))
