from Object3D import *
from tkinter import *
from PIL import Image, ImageTk, ImageDraw

class WorkArea:
    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 600
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.figure = Chair()
        # self.figure_list[0].scale(150, 150, 150)
        self.projection = Projection.ISOMETRIC

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
        self.z1_input_box = Entry(self.root)
        self.z1_input_box.insert(0, "120")

        self.z1_input_box.grid(row=10, column=3)

        Label(self.root, text="x1: ").grid(row=8, column=2)
        Label(self.root, text="y1: ").grid(row=9, column=2)
        Label(self.root, text="z1: ").grid(row=10, column=2)

        Label(self.root, text="angle: ").grid(row=8, column=4)
        self.angle_input_box = Entry(self.root)
        self.angle_input_box.insert(0, "45")
        self.angle_input_box.grid(row=9, column=4)

        self.root.mainloop()

    def translate(self):
        figure = self.figure
        dx = float(self.x_input_box.get())
        dy = float(self.y_input_box.get())
        dz = float(self.z_input_box.get())
        figure.translate(dx, dy, dz)
        print("success translate dx={} dy={} dz={}".format(dx, dy, dz))
        self.redraw_all()

    def center_scale(self):
        figure = self.figure
        mx = float(self.x_input_box.get())
        my = float(self.y_input_box.get())
        mz = float(self.z_input_box.get())
        figure.center_scale(mx, my, mz)
        print("success center scale mx={} my={} mz={}".format(mx, my, mz))
        self.redraw_all()

    def scale(self):
        figure = self.figure
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

    def redraw_all(self):
        self.use_eraser()
        # self.figure.draw(self.draw, self.projection)
        figure_projection = self.figure.project(self.projection)
        # TODO: code for drawing all lines between points

        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def use_eraser(self):
        self.canvas.delete("all")
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_WIDTH), 'white')
        self.draw = ImageDraw.Draw(self.image)


gui = WorkArea()
