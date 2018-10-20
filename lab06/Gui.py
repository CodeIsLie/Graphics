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
        self.figure_list[0].scale(150, 150, 150)
        self.cur_figure_ind = 0

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

        self.shift_button = Button(self.root, text='Translate', command=self.translate)
        self.shift_button.grid(row=6, column=1)

        self.scale_button = Button(self.root, text='Scale', command=self.scale)
        self.scale_button.grid(row=6, column=2)

        self.rotate_button = Button(self.root, text='Rotate', command=self.rotate_all_axis)
        self.rotate_button.grid(row=6, column=3)

        self.rotate_x_button = Button(self.root, text='Rotate about x', command=self.rotate_x_axis)
        self.rotate_x_button.grid(row=6, column=4)

        self.rotate_y_button = Button(self.root, text='Rotate about y', command=self.rotate_y_axis)
        self.rotate_y_button.grid(row=6, column=5)

        self.rotate_z_button = Button(self.root, text='Rotate about z', command=self.rotate_z_axis)
        self.rotate_z_button.grid(row=6, column=6)

        self.root.mainloop()

    def translate(self):
        figure = self.figure_list[self.cur_figure_ind]
        dx = float(self.x_input_box.get())
        dy = float(self.y_input_box.get())
        dz = float(self.z_input_box.get())
        figure.translate(dx, dy, dz)
        print("success translate dx={} dy={} dz={}".format(dx, dy, dz))
        self.redraw_all()

    def scale(self):
        figure = self.figure_list[self.cur_figure_ind]
        mx = float(self.x_input_box.get())
        my = float(self.y_input_box.get())
        mz = float(self.z_input_box.get())
        figure.scale(mx, my, mz)
        print("success scale mx={} my={} mz={}".format(mx, my, mz))
        self.redraw_all()

    def rotate_x_axis(self):
        figure = self.figure_list[self.cur_figure_ind]
        angle_value = self.x_angle_input_box.get()
        if len(angle_value) == 0:
            return
        figure.rotate_all(float(angle_value), 0, 0)
        self.redraw_all()

    def rotate_y_axis(self):
        figure = self.figure_list[self.cur_figure_ind]
        angle_value = self.y_angle_input_box.get()
        if len(angle_value) == 0:
            return
        figure.rotate_all(0, float(angle_value), 0)
        self.redraw_all()

    def rotate_z_axis(self):
        figure = self.figure_list[self.cur_figure_ind]
        angle_value = self.z_angle_input_box.get()
        if len(angle_value) == 0:
            return
        figure.rotate_all(0, 0, float(angle_value))
        self.redraw_all()

    def rotate_all_axis(self):
        figure = self.figure_list[self.cur_figure_ind]
        x_angle = self.x_angle_input_box.get()
        y_angle = self.y_angle_input_box.get()
        z_angle = self.z_angle_input_box.get()
        figure.rotate_all(x_angle, y_angle, z_angle)
        self.redraw_all()

    def redraw_all(self):
        self.use_eraser()
        for figure in self.figure_list:
            figure.draw(self.draw)

        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def use_eraser(self):
        self.canvas.delete("all")
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_WIDTH), 'white')
        self.draw = ImageDraw.Draw(self.image)


gui = WorkArea()
