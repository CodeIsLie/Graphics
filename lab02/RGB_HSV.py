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
    float_img = img.astype('float') / 255
    R = float_img[:, :, 0].tolist()
    G = float_img[:, :, 1].tolist()
    B = float_img[:, :, 2].tolist()

    MAX = [[max(r, g, b) for r, g, b in zip(rs, gs, bs)] for rs, gs, bs in zip(R, G, B)]
    MIN = [[min(r, g, b) for r, g, b in zip(rs, gs, bs)] for rs, gs, bs in zip(R, G, B)]

    H = [[0 if max1 == min1 else
         60 * ( (6 + (g - b) / (max1 - min1)) % 6) if max1 == r else
         60 * (b - r) / (max1 - min1) + 120 if max1 == g else
         60 * (r - g) / (max1 - min1) + 240
         for max1, min1, r, g, b in zip(maxes, mines, rs, gs, bs)]
          for maxes, mines, rs, gs, bs in zip(MAX, MIN, R, G, B)]

    S = [[0 if max1 == 0 else 1 - min1/max1 for min1, max1 in zip(mins, maxes)] for mins, maxes in zip(MIN, MAX)]
    V = MAX

    H = ( (array(H))).astype(int)
    S = (array(S) * 100).astype(int)
    V = (array(V) * 100).astype(int)

    HSV_img = dstack((H, S, V))
    return HSV_img

def HSV2RGB(img):
    H = (img[:, :, 0])
    S = (img[:, :, 1]).astype(int)
    V = (img[:, :, 2]).astype(int)

    Hi = [[ h//60 % 6 for h in hs] for hs in H]
    Vmin = [[ (100-s)*v/100 for s, v in zip(ss, vs)] for ss, vs in zip(S, V)]
    a = [[ (v-vmin)* (h%60)/60 for v, vmin, h in zip(vs, vmins, hs)] for vs, vmins, hs in zip(V, Vmin, H)]
    Vinc = [[vmin + a for vmin, a in zip(vmins, As)] for vmins, As in zip(Vmin, a)]
    Vdec = [[v - a for v, a in zip(vs, As)] for vs, As in zip(V, a)]

    RGB = [ [(v, vi, vm) if h == 0 else
             (vd, v, vm) if h == 1 else
             (vm, v, vi) if h == 2 else
             (vm, vd, v) if h == 3 else
             (vi, vm, v) if h == 4 else
             (v, vm, vd)
             for v, vd, vi, vm, h in zip(vs, vds, vis, vms, hs)]
            for vs, vds, vis, vms, hs in zip(V, Vdec, Vinc, Vmin, Hi)]

    RGB = array(RGB)
    RGB = RGB * 255/100
    RGB = RGB.astype(np.uint8)

    return RGB

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