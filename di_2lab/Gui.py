from Object3D import *
from tkinter import *
from PIL import Image, ImageTk, ImageDraw

class WorkArea:
    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 600
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.figure = Cube()
        self.figure.scale(100, 100, 100)
        self.figure.shift(100, 100, 100)
        # self.figure_list[0].scale(150, 150, 150)
        self.projection_type = Projection.ORTHO_XOY

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

    def project(self):
        projection_type = self.projection_type
        figure = self.figure
        # Orthographic projections
        if projection_type == Projection.ORTHO_XOY:
            return figure.orthographic_XOY().take_xy_coords()
        elif projection_type == Projection.ORTHO_XOZ:
            return figure.orthographic_XOZ().take_xz_coords()
        elif projection_type == Projection.ORTHO_YOZ:
            return figure.orthographic_YOZ().take_yz_coords()
        # Axonometric projections
        elif projection_type == Projection.ISOMETRIC:
            return figure.isometric().take_xy_coords()
        elif projection_type == Projection.DIMETRIC:
            return figure.dimetric().take_xy_coords()
        # Perspective projections
        elif projection_type == Projection.PERSPECTIVE_1:
            return figure.perspective_one_point().take_xy_coords()
        elif projection_type == Projection.PERSPECTIVE_2:
            return figure.perspective_two_point().take_xy_coords()
        elif projection_type == Projection.PERSPECTIVE_3:
            return figure.perspective_three_point().take_xy_coords()

    def translate(self):
        figure = self.figure
        dx = float(self.x_input_box.get())
        dy = float(self.y_input_box.get())
        dz = float(self.z_input_box.get())
        figure.shift(dx, dy, dz)
        print("success translate dx={} dy={} dz={}".format(dx, dy, dz))
        self.redraw_all()

    def scale(self):
        figure = self.figure
        mx = float(self.x_input_box.get())
        my = float(self.y_input_box.get())
        mz = float(self.z_input_box.get())
        figure.scale(mx, my, mz)
        print("success scale mx={} my={} mz={}".format(mx, my, mz))
        self.redraw_all()

    def center_scale(self):
        figure = self.figure
        mx = float(self.x_input_box.get())
        my = float(self.y_input_box.get())
        mz = float(self.z_input_box.get())
        figure.center_scale(mx, my, mz)
        print("success center scale mx={} my={} mz={}".format(mx, my, mz))
        self.redraw_all()

    def redraw_all(self):
        self.use_eraser()
        # self.figure.draw(self.draw, self.projection)
        figure_projection = self.project()
        for point_ind1, point_ind2 in figure_projection.edges:
            x1, y1 = figure_projection.point_list[point_ind1]
            x2, y2 = figure_projection.point_list[point_ind2]
            self.draw.line([x1, y1, x2, y2], width=1, fill=WorkArea.DEFAULT_COLOR)

        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def use_eraser(self):
        self.canvas.delete("all")
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_WIDTH), 'white')
        self.draw = ImageDraw.Draw(self.image)


gui = WorkArea()
