from tkinter import filedialog
from tkinter import *
from PIL import Image
from PIL import ImageTk
# import tkFileDialog
import cv2

def RGB2HSV(img):
    return img

def HSV2RGB(img):
    return img

def select_image():
    # grab a reference to the image panels
    global panelA, panelB, panelScrolls

    # open a file chooser dialog and allow the user to select an input
    # image
    path = filedialog.askopenfilename()
    # ensure a file path was selected
    if len(path) > 0:
        image = cv2.imread(path)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hsv_img = RGB2HSV(image)

        # convert the images to PIL format...
        image = Image.fromarray(image)
        hsv_img = Image.fromarray(hsv_img)
        # ...and then to ImageTk format
        image = ImageTk.PhotoImage(image)
        hsv_img = ImageTk.PhotoImage(hsv_img)

        # if the panels are None, initialize them
        if panelA is None or panelB is None:
            # the first panel will store our original image
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)

            panelB = Label(image=hsv_img)
            panelB.image = hsv_img
            panelB.pack(side="right", padx=10, pady=10)

            panelScrolls = Label(root)
            var = DoubleVar()
            scaleH = Scale(panelScrolls, variable=var)
            scaleH.pack(anchor=TOP)

            scaleC = Scale(panelScrolls, variable=var)
            scaleC.pack(anchor=CENTER)

            scaleV = Scale(panelScrolls, variable=var)
            scaleV.pack(anchor=BOTTOM)
            panelScrolls.pack(side="right", padx=10, pady=10)

        # otherwise, update the image panels
        else:
            # update the pannels
            panelA.configure(image=image)
            panelA.image = image

            panelB.configure(image=hsv_img)
            panelB.image = hsv_img


root = Tk()
panelA = None
panelB = None
panelC = None

# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

# kick off the GUI
root.mainloop()