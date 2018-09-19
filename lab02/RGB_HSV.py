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

    def maxF(r, g, b):
        return max(r, g, b)
    def minF(r, g, b):
        return min(r, g, b)
    maxF = np.vectorize(maxF)
    MAX = maxF(R, G, B)
    MIN = minF(R, G, B)

    H = np.vectorize(lambda max1, min1, r, g, b:
                     0 if max1 == min1 else
                     60 * ((6 + (g - b) / (max1 - min1)) % 6) if max1 == r else
                     60 * (b - r) / (max1 - min1) + 120 if max1 == g else
                     60 * (r - g) / (max1 - min1) + 240
                     )(MAX, MIN, R, G, B)

    S = np.vectorize(lambda min1, max1: 0 if max1 == 0 else 1 - min1/max1)(MIN, MAX)
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

    Hi  = np.vectorize(lambda h: h//60 % 6)(H)
    Vmin = np.vectorize(lambda s, v: (100-s)*v/100)(S, V)
    a = np.vectorize(lambda v, vmin, h: (v-vmin)* (h%60)/60)(V, Vmin, H)
    Vinc = Vmin + a
    Vdec = V - a
    R, G, B = np.vectorize(lambda v, vd, vi, vm, h:
             (v, vi, vm) if h == 0 else
             (vd, v, vm) if h == 1 else
             (vm, v, vi) if h == 2 else
             (vm, vd, v) if h == 3 else
             (vi, vm, v) if h == 4 else
             (v, vm, vd))(V, Vdec, Vinc, Vmin, Hi)

    RGB = dstack((R, G, B))
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
        self.H = self.HSV_img[:, :, 0]
        self.S = self.HSV_img[:, :, 1]
        self.V = self.HSV_img[:, :, 2]
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
            self.H = self.HSV_img[:, :, 0]
            self.S = self.HSV_img[:, :, 1]
            self.V = self.HSV_img[:, :, 2]

            image = Image.fromarray(img)
            image = ImageTk.PhotoImage(image)
            self.panelA.configure(image=image)
            self.panelA.image = image

        self.choose_button = tk.Button(root)
        self.choose_button["text"] = "Choose an image"
        self.choose_button["command"] = choose_img
        self.choose_button.grid(row=5, column=0, rowspan=1, columnspan=2, sticky=W + E)

        def save_img():
            path = filedialog.asksaveasfile(mode='w', filetypes=(("Image files", "*.png"),("Jpeg files", "*.jpg")))
            if path is None:
                return
            path = path.name
            imwrite(path, cv2.cvtColor(self.RGB_img, cv2.COLOR_RGB2BGR))

        self.save_button = tk.Button(root)
        self.save_button["text"] = "Save img to file"
        self.save_button["command"] = save_img
        self.save_button.grid(row=5, column=3, rowspan=1, columnspan=4, sticky=W + E)

    def setImage(self, image):
        self.RGB_img = image
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.panelA.configure(image=image)
        self.panelA.image = image

    def createScales(self):
        def changeHue(hue):
            H = self.HSV_img[:, :, 0]
            H = (H + (int(hue) - 120)) % 360
            self.H = H
            S = self.S
            V = self.V
            self.setImage(HSV2RGB(dstack((H, S, V))))

        def changeSaturation(sat):
            sat = int(sat)
            def modifySat(s):
                return min(100, s + sat - 100) if sat >= 100 else max(0, s + sat - 100)
            modifySat = np.vectorize(modifySat)

            H = self.H
            S = self.HSV_img[:, :, 1]
            S = modifySat(S)
            self.S = S
            V = self.V
            self.setImage(HSV2RGB(dstack((H, S, V))))

        def changeValue(value):
            value = int(value)
            def modifyValue(v):
                return min(100, v + value - 100) if value >= 100 else max(0, v + value - 100)
            modifyValue = np.vectorize(modifyValue)

            H = self.H
            S = self.S
            V = self.HSV_img[:, :, 2]
            V = modifyValue(V)
            self.V = V
            self.setImage(HSV2RGB(dstack((H, S, V))))

        varH = DoubleVar(value=120)
        scaleH = Scale(root, variable=varH, from_=0, to=360, command=changeHue)
        scaleH.grid(row=0, column=3, rowspan=5, columnspan=1, sticky=N + S)

        varS = DoubleVar(value=100)
        scaleS = Scale(root, variable=varS, from_=0, to=200, command=changeSaturation)
        scaleS.grid(row=0, column=4, rowspan=5, columnspan=1, sticky=N + S)

        varV = DoubleVar(value=100)
        scaleV = Scale(root, variable=varV, from_=0, to=200, command=changeValue)
        scaleV.grid(row=0, column=5, rowspan=5, columnspan=4, sticky=N + S)

root = tk.Tk()
app = Application(master=root)
app.mainloop()