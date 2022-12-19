from cv2 import cv2
import random
import pandas as pd
from PIL import Image as Imagee
from tkinter import *
from tkinter.colorchooser import askcolor

img_path = 'colorpic.jpg'
img = cv2.imread(img_path)
clicked = False
root = Tk()
r = g = b = xpos = ypos = 0
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)


def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if (d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)
        print("-----------------------------------------------------------")
        print("Color U have Picked From the Image :", b, g, r)


cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while (1):

    cv2.imshow("image", img)

    if (clicked):
        colors = askcolor(title="Color Chooser")[0]
        print("Color You have Chosen to change:", colors)
        pass
        img_pil = Imagee.open("colorpic.jpg")
        img_pil = img_pil.convert("RGB")
        d = img_pil.getdata()
        new_image = []
        root.geometry("300x300")
        # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text string to display( Color name and RGB values )
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if (r + g + b >= 600):
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        width, height = img_pil.size
        for i in range(width):
            for j in range(height):
                gg = img_pil.getpixel((i, j))
                if gg[0] in list(range(r - 70, r + 70, 1)):
                    if gg[1] in list(range(g - 70, g + 70, 1)):
                        if gg[2] in list(range(b - 70, b + 70, 1)):
                            img_pil.putpixel((i, j), (colors[0], colors[1], colors[2]))
        img_pil.putdata(new_image)
        img_pil.show("image", img_pil)
        file_name = "Chandru" + str(random.randint(100, 999)) + ".jpg"
        img_pil.save(file_name)
        print("File Has Been Successfully. Named:", file_name)
        print("-----------------------------------------------------------")
        clicked = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()