from Affine3D import *
from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk, ImageDraw

class WorkArea:

    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 600
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.primitive_list = []
        self.current_primitive_ind = -1

        self.root = Tk()
        self.root.title("3DPRO")
        self.root.resizable(False, False)

        self.eraser_button = Button(self.root, text='Clear', command=self.use_eraser)
        self.eraser_button.grid(row=3, column=1)

        self.canvas = Canvas(self.root, bg='white', width=self.DEFAULT_WIDTH, height=self.DEFAULT_WIDTH)
        self.canvas.grid(row=1, columnspan=10)
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.image)

        # Label(self.root, text="Your primitives list: ").grid(row=0, column=12)

        Label(self.root, text="x: ").grid(row=2, column=5)
        Label(self.root, text="y: ").grid(row=3, column=5)
        Label(self.root, text="z: ").grid(row=4, column=5)
        Label(self.root, text="angle: ").grid(row=5, column=5)

        self.x_input_box = Entry(self.root)
        self.y_input_box = Entry(self.root)
        self.z_input_box = Entry(self.root)

        self.x_input_box.grid(row=2, column=6)
        self.y_input_box.grid(row=3, column=6)

        self.angle_input_box = Entry(self.root)
        self.angle_input_box.grid(row=4, column=6)

        self.shift_button = Button(self.root, text='Shift') #, command=self.shift_primitive)
        self.shift_button.grid(row=6, column=5)

        self.scale_button = Button(self.root, text='Scale') #, command=self.scale_primitive)
        self.scale_button.grid(row=6, column=6)

        self.rotate_button = Button(self.root, text='Rotate') #, command=self.rotate_primitive)
        self.rotate_button.grid(row=6, column=7)

        self.root.mainloop()

    def use_eraser(self):
        pass

gui = WorkArea()