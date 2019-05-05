import cv2
from PIL import Image,ImageDraw,ImageFont
import numpy as np
def addTextToVideo(fromVideoPath, toVideoPath, x, y, text):
    # 读取视频
    cap = cv2.VideoCapture(fromVideoPath)
    # 获取视频帧率
    fps_video = cap.get(cv2.CAP_PROP_FPS)
    # 设置写入视频的编码格式
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    # 获取视频宽度
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # 获取视频高度
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    videoWriter = cv2.VideoWriter(toVideoPath, fourcc, fps_video, (frame_width, frame_height))
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            # 文字坐标
            cv2img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            pilimg = Image.fromarray(cv2img)
            # PIL图片上打印汉字
            draw = ImageDraw.Draw(pilimg)  # 图片上打印
            font = ImageFont.truetype("/home/liuwenbin/PycharmProjects/timetravel/static/fonts/YaHei.Consolas.1.12.ttf",
                                      20, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
            draw.text((x, y), text, (255, 0, 0), font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
            # PIL图片转cv2 图片
            cv2charimg = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
            videoWriter.write(cv2charimg)
        else:
            videoWriter.release()
            break

addTextToVideo("/home/liuwenbin/Videos/movie/比我还要聪明.mp4", "/home/liuwenbin/Videos/movie/比我还要聪明1.mp4",0,50,"你好啊")