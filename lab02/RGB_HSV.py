# Преобразовать изображение из RGB в HSV. Добавить возможность изменять значения оттенка, насыщенности и яркости.
# Результат сохранять в файл, предварительно преобразовав обратно.

from cv2 import imread, imwrite
import cv2
import PIL
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image
from PIL import ImageTk

from numpy import dstack
from numpy import array
import numpy as np


def RGB2HSV(img):
    float_img = cv2.normalize(img.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)
    R = float_img[:, :, 0].tolist()
    G = float_img[:, :, 1].tolist()
    B = float_img[:, :, 2].tolist()

    MAX = [[max(r, g, b) for r, g, b in zip(rs, gs, bs)] for rs, gs, bs in zip(R, G, B)]
    MIN = [[min(r, g, b) for r, g, b in zip(rs, gs, bs)] for rs, gs, bs in zip(R, G, B)]

    H = [[0 if max1 == min1 else
         60 * (g - b) // (max1 - min1) + 0 if max == r and g >= b else
         60 * (g - b) // (max1 - min1) + 360 if max == r else
         60 * (b - r) // (max1 - min1) + 120 if max == g else
         60 * (r - g) // (max1 - min1) + 240
         for max1, min1, r, g, b in zip(maxes, mines, rs, gs, bs)]
          for maxes, mines, rs, gs, bs in zip(MAX, MIN, R, G, B)]
    S = [[0 if max1 == 0 else 1 - min1/max1 for min1, max1 in zip(mins, maxes)] for mins, maxes in zip(MIN, MAX)]
    V = MAX

    H = (array(H) // 2).astype(int)
    S = (array(S) * 255).astype(int)
    V = (array(V) * 255).astype(int)

    HSV_img = dstack((H, S, V))
    return HSV_img
    # , cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

def HSV2RGB(img):
    H = img[:, :, 0]
    S = img[:, :, 1]
    V = img[:, :, 2]

    img = img.astype(np.uint8)
    RGB_img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)

    return RGB_img

def getImg(path):
    img = imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(img)
    image = ImageTk.PhotoImage(image)
    return image


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.RGB_img = None
        self.HSV_img = None

        # panelA = None
        self.createGui()

    def createGui(self):
        self.grid()
        self.master.title("Channels changes")

        for r in range(6):
            self.master.rowconfigure(r, weight=1)
        for c in range(5):
            self.master.columnconfigure(c, weight=1)

        filename = "img1.png"
        img = imread(filename)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.RGB_img = img
        self.HSV_img = RGB2HSV(img)
        # image = RGB2HSV(img)

        image = Image.fromarray(img)
        image = ImageTk.PhotoImage(image)

        self.panelA = Label(image=image)
        self.panelA.image = image
        self.panelA.grid(row=0, column=0, rowspan=5, columnspan=2, sticky=W + E + N + S)

        self.createScales()
        self.createButtons()

    def createButtons(self):
        def choose_img():
            path = filedialog.askopenfilename()
            if len(path) < 1:
                return

            img = imread(path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            self.RGB_img = img
            self.HSV_img = RGB2HSV(img)

            image = Image.fromarray(img)
            image = ImageTk.PhotoImage(image)
            self.panelA.configure(image=image)
            self.panelA.image = image

        self.choose_button = tk.Button(root)
        self.choose_button["text"] = "Choose an image"
        self.choose_button["command"] = choose_img
        self.choose_button.grid(row=5, column=0, rowspan=1, columnspan=2, sticky=W + E)

        def test_convertations():
            hsv_img = RGB2HSV(self.RGB_img)
            rgb_img = HSV2RGB(hsv_img)

            image = Image.fromarray(rgb_img)
            image = ImageTk.PhotoImage(image)
            self.panelA.configure(image=image)
            self.panelA.image = image

        self.save_button = tk.Button(root)
        self.save_button["text"] = "Save img to file"
        self.save_button["command"] = test_convertations
        self.save_button.grid(row=5, column=3, rowspan=1, columnspan=4, sticky=W + E)

    def createScales(self):
        def changeHue(hue):
            pass

        def changeSaturation(sat):
            pass

        def changeValue(value):
            pass

        varH = DoubleVar(value=120)
        scaleH = Scale(root, variable=varH, from_=0, to=255, command=changeHue)
        scaleH.grid(row=0, column=3, rowspan=5, columnspan=1, sticky=N + S)

        varS = DoubleVar(value=120)
        scaleS = Scale(root, variable=varS, from_=0, to=255, command=changeSaturation)
        scaleS.grid(row=0, column=4, rowspan=5, columnspan=1, sticky=N + S)

        varV = DoubleVar(value=120)
        scaleV = Scale(root, variable=varV, from_=0, to=255, command=changeValue)
        scaleV.grid(row=0, column=5, rowspan=5, columnspan=4, sticky=N + S)

root = tk.Tk()
app = Application(master=root)
app.mainloop()