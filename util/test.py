from PIL import Image

lines = open("/home/liuwenbin/Desktop/location","r")
im = Image.open("/home/liuwenbin/Desktop/w.jpg")
img1 = Image.open("/home/liuwenbin/Desktop/gallery-img1.jpg")
im.resize((2000,1500)).save('/home/liuwenbin/Desktop/w.jpg')
im = Image.open("/home/liuwenbin/Desktop/w.jpg")
for line in lines:
    line = line.strip()
    if line == "":
        continue
    line = line.replace("\t",",")
    vals = line.split(",")
    t = (int(vals[0])*2, int(vals[1])*2, int(vals[2])*2 + int(vals[0])*2, int(vals[3])*2 + int(vals[1])*2)
    print(t)
    img1 = img1.resize((int(vals[2])*2, int(vals[3])*2))
    im.paste(img1, t)
im.show()


