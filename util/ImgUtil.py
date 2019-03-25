from PIL import Image, ImageFilter

#"/home/liuwenbin/Desktop/1.png"
'''
旋转图片
imgPath，图片绝对路径
degree，旋转角度
'''
def rotate(img, degree):
    img = img.convert('RGBA')
    img = img.rotate(degree)
    return img

'''
透明化图片
imgPath，图片绝对路径
alpha，透明度（0.0-1.0）
'''
def alpha(img,alpha):
    img = img.convert('RGBA')
    L, H = img.size
    for h in range(H):
        for l in range(L):
            dot = (l,h)
            color_1 = img.getpixel(dot)
            color_1 = color_1[:-1] + (int(255 * alpha),)
            img.putpixel(dot,color_1)
    return img

'''
画图片阴影和边框(把图像放在一个作了高斯模糊的背景上)
imgPath，图片绝对路径
offset，阴影相对图像的偏移，用(x,y)表示，可以为正数或者负数
background，背景色
shadow，阴影色
border，图像边框，必须足够用来制作阴影模糊
iterations，过滤器处理次数，次数越多越模糊，当然处理过程也越慢
'''
def dropShadow(image, offset=(5,5),
        shadow=0x444444, border=8, iterations=3):
    # 创建背景块
    originWidth = image.size[0]
    originHeight = image.size[1]
    totalWidth = originWidth + abs(offset[0]) + 2*border
    totalHeight = originHeight + abs(offset[1]) + 2*border
    image = image.convert('RGB')
    back = Image.new(image.mode, (totalWidth, totalHeight), 0xffffff)

    # 放置阴影块，考虑图像偏移
    shadowLeft = border + max(offset[0], 0)
    shadowTop = border + max(offset[1], 0)
    back.paste(shadow, [shadowLeft, shadowTop, shadowLeft + image.size[0],
        shadowTop + image.size[1]] )

    # 处理阴影的边缘模糊
    n = 0
    while n < iterations:
        back = back.filter(ImageFilter.BLUR)
        n += 1

    back = back.convert('RGBA')
    L, H = back.size
    base = 255 * 255 * 255
    for h in range(H):
        for l in range(L):
            dot = (l, h)
            color_1 = back.getpixel(dot)
            alpha = int((base - color_1[0] * color_1[1] * color_1[2]) / base * 255)
            color_1 = color_1[:-1] + ((255 - alpha),)
            back.putpixel(dot, color_1)

    # 把图像粘贴到背景上
    imageLeft = border - min(offset[0], 0)
    imageTop = border - min(offset[1], 0)
    back.paste(image, (imageLeft, imageTop))
    back = back.resize((originWidth,originHeight),Image.ANTIALIAS)
    return back

'''
模糊图片
imgPath，图片绝对路径
'''
def blur(im):
    im3 = im.filter(ImageFilter.BLUR)
    return im3

'''
裁剪图片
imgPath，图片绝对路径
top，距离顶部距离
left，距离左侧距离
width，宽度
height，高度
'''
def cut(imgPath,top,left,width,height):
    img = Image.open(imgPath)
    region = (left, top, left + width, top + height)
    cropImg = img.crop(region)
    return cropImg

'''
缩放图片，根据宽高
imgPath，图片绝对路径
width，宽
height，高
'''
def resize(img,width,height):
    img = img.resize((width, height), Image.ANTIALIAS)
    return img

'''
缩放图片，根据百分比
imgPath，图片绝对路径
percent，百分比
'''
def resizeByPercent(img, percent):
    img = img.resize((int(img.size[0] * percent), int(img.size[1] * percent)), Image.ANTIALIAS)
    return img

def getWHPercent(imgPath):
    image = Image.open(imgPath)
    return round(image.size[0] / image.size[1], 2)

'''
压缩图片质量
'''
def compress(inImgName,outImgName):
    image = Image.open(inImgName)
    image.save(outImgName, quality=20)