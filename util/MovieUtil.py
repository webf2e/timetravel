import cv2
from PIL import Image,ImageDraw,ImageFont, ImageFilter
import os,shutil
import skvideo.io
#sudo pip3 install sk-video

headSecond = 4

def getImgWidthAndHeight(imgPath):
    image = Image.open(imgPath)
    return (image.size[0], image.size[1])

def resizeImg(img,width,height):
    img = img.resize((width, height), Image.ANTIALIAS)
    return img

def resizeImgByPercent(img, percent):
    img = img.resize((int(img.size[0] * percent), int(img.size[1] * percent)), Image.ANTIALIAS)
    return img

def getVideoInfo(videoPath):
    # 读取视频
    cap = cv2.VideoCapture(videoPath)
    # 获取视频帧率
    fps_video = int(cap.get(cv2.CAP_PROP_FPS))
    # 获取视频宽度
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # 获取视频高度
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return (frame_width, frame_height, fps_video)

def getImgName(current):
    if current < 10:
        return "000000{}".format(current)
    elif current < 100:
        return "00000{}".format(current)
    elif current < 1000:
        return "0000{}".format(current)
    elif current < 10000:
        return "000{}".format(current)
    elif current < 100000:
        return "00{}".format(current)
    elif current < 1000000:
        return "0{}".format(current)
    elif current < 10000000:
        return "{}".format(current)
    return "{}".format(current)

def changeVideoToImgs(videoPathAndName, savePath, prefix):
    videogen = skvideo.io.vreader(videoPathAndName)
    i = 1
    for frame in videogen:
        name = getImgName(i)
        skvideo.io.vwrite(os.path.join(savePath,"{}_{}.png").format(prefix,name), frame)
        i = i + 1
    print("{}的帧数：{}".format(videoPathAndName, i))
    return i

def changeImgSize(imgPathAndName,maxWidth,maxHeight):
    width,height = getImgWidthAndHeight(imgPathAndName)
    hPercent = maxHeight / height
    wPercent = maxWidth / width
    realImg = Image.open(imgPathAndName)
    bimg = Image.open(imgPathAndName)
    bimg = resizeImg(bimg, maxWidth, maxHeight)
    for i in range(0,15):
        bimg = bimg.filter(ImageFilter.BLUR)
    bimg = bimg.point(lambda p: p * 2.1)
    if hPercent <= wPercent:
        #左右
        realImg = resizeImgByPercent(realImg, hPercent)
        offset = (maxWidth - realImg.size[0]) // 2
        bimg.paste(realImg, [offset, 0, offset + realImg.size[0], realImg.size[1]])
        bimg.save(imgPathAndName)
    else:
        #上下
        realImg = resizeImgByPercent(realImg, wPercent)
        offset = (maxHeight - realImg.size[1]) // 2
        bimg.paste(realImg, [0, offset, realImg.size[0], offset + realImg.size[1]])
        bimg.save(imgPathAndName)

def addTextToImg(imgNameAndPath,text):
    image = Image.open(imgNameAndPath)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/home/liuwenbin/PycharmProjects/timetravel/static/fonts/YaHei.Consolas.1.12.ttf",
                              20, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
    textWidth = 24 * len(text)
    draw.text(((image.size[0] - textWidth) // 2, image.size[1] - 30), text, (255, 0, 0), font=font)
    image.save(imgNameAndPath)

def makeBegin(index, text, maxHeight, maxWidth, path):
    image = Image.open("/home/liuwenbin/PycharmProjects/timetravel/static/images/bak.png")
    image = resizeImg(image, maxWidth, maxHeight)
    imgName = getImgName(index)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/home/liuwenbin/PycharmProjects/timetravel/static/fonts/YaHei.Consolas.1.12.ttf",
                              20, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
    draw.text(((image.size[0] - 24 * len(text)) // 2, (image.size[1] - 30) // 2), text, (255, 255, 255), font=font)
    draw.text(((image.size[0] - 11 * 13) // 2, (image.size[1] - 30) // 2 + 30), "@CherryCoding", (255, 255, 255), font=font)
    image.save(os.path.join(path, "0_{}.png".format(imgName)))

#change all video to imgs
def getNewVideo(videoPath):
    dirName = videoPath[videoPath.rfind("/")+1:]
    videoImgPath = os.path.join(videoPath, "imgs")
    if not os.path.exists(videoImgPath):
        os.mkdir(videoImgPath)

    videos = sorted(os.listdir(videoPath))
    maxWidth = 0
    maxHeight = 0
    totalFps = 0
    videoCount = 0
    totalImgCount = 0
    for video in videos:
        if not video.endswith(".mp4"):
            continue
        videoPathAndName = os.path.join(videoPath, video)
        totalImgCount += changeVideoToImgs(videoPathAndName, videoImgPath, video.replace(".mp4", ""))
        width, height, fps = getVideoInfo(videoPathAndName)
        if width > maxWidth:
            maxWidth = width
        if height > maxHeight:
            maxHeight = height
        totalFps += fps
        videoCount += 1
    avgFps = totalFps // videoCount
    print("avgFps:{}".format(avgFps))
    print("一共有{}张图片".format(totalImgCount))
    print("最大高宽为：{}, {}".format(maxHeight, maxWidth))

    for i in range(0,avgFps * headSecond):
        makeBegin(i, dirName, maxHeight, maxWidth,videoImgPath)

    # modify images
    tongjiCount = 50
    images = sorted(os.listdir(videoImgPath))
    operateCount = 0
    for image in images:
        if not image.endswith(".png"):
            continue
        imgNameAndPath = os.path.join(videoImgPath, image)
        changeImgSize(imgNameAndPath, maxWidth, maxHeight)
        operateCount += 1
        if operateCount % tongjiCount == 0:
            print("修改图片大小已经处理了{}%".format(operateCount / totalImgCount * 100))

    # add text
    operateCount = 0
    for image in images:
        if not image.endswith(".png"):
            continue
        imgNameAndPath = os.path.join(videoImgPath, image)
        text = image.replace(".png", "")
        text = text[0:text.rfind("_")]
        addTextToImg(imgNameAndPath, text)
        operateCount += 1
        if operateCount % tongjiCount == 0:
            print("在图片上添加文字已经处理了{}%".format(operateCount / totalImgCount * 100))

    # change to avi
    operateCount = 0
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    videoWriter = cv2.VideoWriter(os.path.join(videoPath.replace(dirName,""), "{}.avi".format(dirName)), fourcc, avgFps,
                                  (maxWidth, maxHeight))  # 最后一个是保存图片的尺寸\
    for image in images:
        if not image.endswith(".png"):
            continue
        imgNameAndPath = os.path.join(videoImgPath, image)
        frame = cv2.imread(imgNameAndPath)
        videoWriter.write(frame)
        operateCount += 1
        if operateCount % tongjiCount == 0:
            print("转化为视频已经处理了{}%".format(operateCount / totalImgCount * 100))
    videoWriter.release()
    # del img
    shutil.rmtree(videoImgPath)


parentVideoPath = "/home/liuwenbin/Videos"
videoDirs = os.listdir(parentVideoPath)
for videoDir in videoDirs:
    try:
        getNewVideo(os.path.join(parentVideoPath, videoDir))
        pass
    except Exception as e:
        print(e)