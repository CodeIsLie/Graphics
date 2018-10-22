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

        Label(self.root, text="choose your figure: ").grid(row=2, column=7)
        self.current_figure_var = StringVar(self.root)
        self.current_figure_var.set("cube")  # default value
        self.choose_figure_list = OptionMenu(self.root, self.current_figure_var, "cube", "tetraedr", "octaedr")
        self.choose_figure_list.grid(row=3, column=7)

        Label(self.root, text="x: ").grid(row=2, column=2)
        Label(self.root, text="y: ").grid(row=3, column=2)
        Label(self.root, text="z: ").grid(row=4, column=2)
        Label(self.root, text="x_angle: ").grid(row=2, column=4)
        Label(self.root, text="y_angle: ").grid(row=3, column=4)
        Label(self.root, text="z_angle: ").grid(row=4, column=4)

        self.x_input_box = Entry(self.root)
        self.y_input_box = Entry(self.root)
        self.z_input_box = Entry(self.root)

        self.x_input_box.insert(0, "100")
        self.y_input_box.insert(0, "100")
        self.z_input_box.insert(0, "100")

        self.x_input_box.grid(row=2, column=3)
        self.y_input_box.grid(row=3, column=3)
        self.z_input_box.grid(row=4, column=3)

        self.x_angle_input_box = Entry(self.root)
        self.y_angle_input_box = Entry(self.root)
        self.z_angle_input_box = Entry(self.root)

        self.x_angle_input_box.insert(0, "15")
        self.y_angle_input_box.insert(0, "15")
        self.z_angle_input_box.insert(0, "15")

        self.x_angle_input_box.grid(row=2, column=5)
        self.y_angle_input_box.grid(row=3, column=5)
        self.z_angle_input_box.grid(row=4, column=5)

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

        self.rotate_button = Button(self.root, text='Rotate about vector', command=self.rotate_about_vector)
        self.rotate_button.grid(row=7, column=3)

        self.center_scale_button = Button(self.root, text='Center Scale', command=self.center_scale)
        self.center_scale_button.grid(row=7, column=2)

        self.x1_input_box = Entry(self.root)
        self.y1_input_box = Entry(self.root)
        self.z1_input_box = Entry(self.root)

        self.x1_input_box.insert(0, "120")
        self.y1_input_box.insert(0, "120")
        self.z1_input_box.insert(0, "120")

        self.x1_input_box.grid(row=8, column=3)
        self.y1_input_box.grid(row=9, column=3)
        self.z1_input_box.grid(row=10, column=3)

        Label(self.root, text="x1: ").grid(row=8, column=2)
        Label(self.root, text="y1: ").grid(row=9, column=2)
        Label(self.root, text="z1: ").grid(row=10, column=2)

        Label(self.root, text="angle: ").grid(row=8, column=4)
        self.angle_input_box = Entry(self.root)
        self.angle_input_box.insert(0, "45")
        self.angle_input_box.grid(row=9, column=4)

        self.mirror_button = Button(self.root, text='Mirror', command=self.mirror)
        self.mirror_button.grid(row=7, column=7)

        self.xoy_check_box = IntVar()
        Checkbutton(self.root, text="XOY", variable=self.xoy_check_box).grid(row=8, column=7)
        self.yoz_check_box = IntVar()
        Checkbutton(self.root, text="YOZ", variable=self.yoz_check_box).grid(row=9, column=7)
        self.zox_check_box = IntVar()
        Checkbutton(self.root, text="ZOX", variable=self.zox_check_box).grid(row=10, column=7)

        self.rotate_x_center_button = Button(self.root, text='Rotate about center x', command=self.rotate_x_center)
        self.rotate_x_center_button.grid(row=7, column=4)

        self.rotate_y_center_button = Button(self.root, text='Rotate about center y', command=self.rotate_y_center)
        self.rotate_y_center_button.grid(row=7, column=5)

        self.rotate_z_center_button = Button(self.root, text='Rotate about center z', command=self.rotate_z_center)
        self.rotate_z_center_button.grid(row=7, column=6)

        self.root.mainloop()

    def mirror(self):
        figure = self.figure_list[self.cur_figure_ind]
        xoy = self.xoy_check_box.get()
        yoz = self.yoz_check_box.get()
        zox = self.zox_check_box.get()
        figure.mirror(xoy, yoz, zox)
        self.redraw_all()

    def translate(self):
        figure = self.figure_list[self.cur_figure_ind]
        dx = float(self.x_input_box.get())
        dy = float(self.y_input_box.get())
        dz = float(self.z_input_box.get())
        figure.translate(dx, dy, dz)
        print("success translate dx={} dy={} dz={}".format(dx, dy, dz))
        self.redraw_all()

    def center_scale(self):
        figure = self.figure_list[self.cur_figure_ind]
        mx = float(self.x_input_box.get())
        my = float(self.y_input_box.get())
        mz = float(self.z_input_box.get())
        figure.center_scale(mx, my, mz)
        print("success center scale mx={} my={} mz={}".format(mx, my, mz))
        self.redraw_all()

    def scale(self):
        figure = self.figure_list[self.cur_figure_ind]
        mx = float(self.x_input_box.get())
        my = float(self.y_input_box.get())
        mz = float(self.z_input_box.get())
        figure.scale(mx, my, mz)
        print("success scale mx={} my={} mz={}".format(mx, my, mz))
        self.redraw_all()

    def rotate_x_center(self):
        figure = self.figure_list[self.cur_figure_ind]
        angle_value = self.angle_input_box.get()
        if len(angle_value) == 0:
            return
        x = figure.center_point[0]
        y = figure.center_point[1]
        z = figure.center_point[2]
        figure.rotate_about_vector(float(angle_value), x, y, z, x + 10, y, z)
        self.redraw_all()

    def rotate_y_center(self):
        figure = self.figure_list[self.cur_figure_ind]
        angle_value = self.angle_input_box.get()
        if len(angle_value) == 0:
            return
        x = figure.center_point[0]
        y = figure.center_point[1]
        z = figure.center_point[2]
        figure.rotate_about_vector(float(angle_value), x, y, z, x, y + 10, z)
        self.redraw_all()

    def rotate_z_center(self):
        figure = self.figure_list[self.cur_figure_ind]
        angle_value = self.angle_input_box.get()
        if len(angle_value) == 0:
            return
        x = figure.center_point[0]
        y = figure.center_point[1]
        z = figure.center_point[2]
        figure.rotate_about_vector(float(angle_value), x, y, z, x, y, z + 10)
        self.redraw_all()

    def rotate_about_vector(self):
        figure = self.figure_list[self.cur_figure_ind]
        x = float(self.x_input_box.get())
        y = float(self.y_input_box.get())
        z = float(self.z_input_box.get())

        x1 = float(self.x1_input_box.get())
        y1 = float(self.y1_input_box.get())
        z1 = float(self.z1_input_box.get())

        angle_value = self.angle_input_box.get()

        figure.rotate_about_vector(float(angle_value), x, y, z, x1, y1, z1)
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
        x_angle = float(self.x_angle_input_box.get())
        y_angle = float(self.y_angle_input_box.get())
        z_angle = float(self.z_angle_input_box.get())
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
