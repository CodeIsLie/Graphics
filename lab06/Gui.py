from Affine3D import *
from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk, ImageDraw


class WorkArea:

    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 600
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.figure_list = [Polyhedron.get_cube()]
        # self.current_primitive_ind = -1

        self.root = Tk()
        self.root.title("3DPRO")
        self.root.resizable(False, False)

        self.eraser_button = Button(self.root, text='Clear', command=self.use_eraser)
        self.eraser_button.grid(row=3, column=1)

        self.redraw_button = Button(self.root, text='Redraw', command=self.redraw_all)
        self.redraw_button.grid(row=2, column=1)

        self.canvas = Canvas(self.root, bg='white', width=self.DEFAULT_WIDTH, height=self.DEFAULT_WIDTH)
        self.canvas.grid(row=1, columnspan=10)
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.image)

        # Label(self.root, text="Your primitives list: ").grid(row=0, column=12)

        Label(self.root, text="x: ").grid(row=2, column=2)
        Label(self.root, text="y: ").grid(row=3, column=2)
        Label(self.root, text="z: ").grid(row=4, column=2)
        Label(self.root, text="x_angle: ").grid(row=2, column=5)
        Label(self.root, text="y_angle: ").grid(row=3, column=5)
        Label(self.root, text="z_angle: ").grid(row=4, column=5)

        self.x_input_box = Entry(self.root)
        self.y_input_box = Entry(self.root)
        self.z_input_box = Entry(self.root)

        self.x_input_box.grid(row=2, column=3)
        self.y_input_box.grid(row=3, column=3)
        self.z_input_box.grid(row=4, column=3)

        self.x_angle_input_box = Entry(self.root)
        self.y_angle_input_box = Entry(self.root)
        self.z_angle_input_box = Entry(self.root)

        self.x_angle_input_box.grid(row=2, column=6)
        self.y_angle_input_box.grid(row=3, column=6)
        self.z_angle_input_box.grid(row=4, column=6)

        self.shift_button = Button(self.root, text='Shift') #, command=self.shift_primitive)
        self.shift_button.grid(row=6, column=1)

        self.scale_button = Button(self.root, text='Scale')
        self.scale_button.grid(row=6, column=2)

        self.rotate_button = Button(self.root, text='Rotate')
        self.rotate_button.grid(row=6, column=3)

        self.rotate_button = Button(self.root, text='Rotate about x')
        self.rotate_button.grid(row=6, column=4)

        self.rotate_button = Button(self.root, text='Rotate about y')
        self.rotate_button.grid(row=6, column=5)

        self.rotate_button = Button(self.root, text='Rotate about z')
        self.rotate_button.grid(row=6, column=6)

        self.root.mainloop()

    def redraw_all(self):
        for figure in self.figure_list:
            figure.draw(self.draw)

        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def use_eraser(self):
        self.canvas.delete("all")
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_WIDTH), 'white')
        self.draw = ImageDraw.Draw(self.image)


gui = WorkArea()
