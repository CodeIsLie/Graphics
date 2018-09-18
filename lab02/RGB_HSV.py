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

# import tkFileDialog


def RGB2HSV(img):
    return img

def HSV2RGB(img):
    return img

def imgWork():
    filename = "img1.png"
    img = imread(filename)

    # change scrollbars -> change channel by modify original channel, assembly img, HSV2RGB
    # redraw imagebox
    # imgcopy
    # if click on button, save img to file

    hsv_img = RGB2HSV(img)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.grid()
        self.master.title("Channels changes")

        filename = "img1.png"
        img = imread(filename)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img)
        image = ImageTk.PhotoImage(image)

        #global panelA
        # panelA = None
        panelA = Label(image=image)
        panelA.image = image
        panelA.grid(row=0, column=0, rowspan=5, columnspan=2, sticky=W + E + N + S)

        for r in range(6):
            self.master.rowconfigure(r, weight=1)
        for c in range(5):
            self.master.columnconfigure(c, weight=1)

        def choose_img():
            path = filedialog.askopenfilename()
            if len(path) < 1:
                return
            img = imread(path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(img)
            image = ImageTk.PhotoImage(image)

            panelA.configure(image=image)
            panelA.image = image

        self.choose_button = tk.Button(root)
        self.choose_button["text"] = "Choose an image"
        self.choose_button["command"] = choose_img
        self.choose_button.grid(row=5, column=0, rowspan=1, columnspan=2, sticky=W + E)

        self.save_button = tk.Button(root)
        self.save_button["text"] = "Save img to file"
        self.save_button["command"] = root.destroy
        self.save_button.grid(row=5, column=3, rowspan=1, columnspan=4, sticky=W + E)

        def changeHue(hue):
            pass

        def changeSaturation(sat):
            pass

        def changeValue(value):
            pass

        varH = DoubleVar(value=120)
        scaleH = Scale(root, variable=varH, from_=0, to=255, command=changeHue)
        scaleH.grid(row = 0, column = 3, rowspan=5, columnspan = 1, sticky = N+S)

        varS = DoubleVar(value=120)
        scaleS = Scale(root, variable=varS, from_=0, to=255, command=changeSaturation)
        scaleS.grid(row=0, column=4, rowspan=5, columnspan=1, sticky=N + S)

        varV = DoubleVar(value=120)
        scaleV = Scale(root, variable=varV, from_=0, to=255, command=changeValue)
        scaleV.grid(row=0, column=5, rowspan=5, columnspan=4, sticky=N + S)



root = tk.Tk()
app = Application(master=root)
app.mainloop()