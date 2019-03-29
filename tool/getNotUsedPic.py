import os

path = "../"

fileContentMap = {}
imgs = []
def getContent(path):
    if os.path.isfile(path):
        if path.endswith("html") or path.endswith("js") or path.endswith("css") or path.endswith("py"):
            content = ""
            lines = open(path,"r+")
            for line in lines:
                content += line
            fileContentMap[path] = content
        elif path.lower().endswith("gif") or path.lower().endswith("png") or path.lower().endswith("jpg") or path.lower().endswith("jpeg"):
            imgs.append(path[path.rfind("/") + 1:])

    else:
        files = os.listdir(path)
        for file in files:
            getContent(os.path.join(path,file))

getContent(path)
print(imgs)