from PIL import Image
import matplotlib.pyplot as plt
import tkinter
import turtle

lines = open("/home/liuwenbin/Desktop/location","r")
im = Image.open("/home/liuwenbin/Desktop/w.jpg")
for line in lines:
    line = line.strip()
    if line == "":
        continue
    line = line.replace("\t",",")
    vals = line.split(",")
    t = (int(vals[0]),int(vals[1]),int(vals[2]) + int(vals[0]),int(vals[3]) + int(vals[1]))
    print(t)
    im.paste("red", t)  ##或者“blue”
im.show()


