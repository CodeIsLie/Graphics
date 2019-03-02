from Object3D import *
from tkinter import *
from PIL import Image, ImageTk, ImageDraw

class WorkArea:
    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 600
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.figure = Chair()
        print(self.figure.point_list)
        print(self.figure.edges)
        self.figure.scale(0.7, 0.7, 0.7)
        self.figure.rotate_x_axis_center(np.pi)
        self.figure.shift(100, 100, 130)
        self.projection_type = Projection.ORTHO_XOY

        self.iso_mode = "iso_1"
        self.root = Tk()
        self.root.title("3DPRO")
        self.root.resizable(False, False)

        self.canvas = Canvas(self.root, bg='white', width=self.DEFAULT_WIDTH, height=self.DEFAULT_WIDTH)
        self.canvas.grid(row=1, columnspan=10)
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.image)

        Label(self.root, text="Тип проекции:             ").grid(row=2, column=1)
        self.projection_var = StringVar(self.root)
        self.projection_var.set("orthographic_xoy")  # default value
        possible_projections = ["orthographic_xoy",
                                "orthographic_xoz",
                                "orthographic_yoz",
                                "isometric",
                                "dimetric",
                                "perspective_one",
                                "perspective_two",
                                "perspective_three"]
        self.choose_projection = OptionMenu(self.root, self.projection_var, *possible_projections)
        self.choose_projection.grid(row=3, column=1)

        self.projection_button = Button(self.root, text='Apply', command=self.select_projection)
        self.projection_button.grid(row=4, column=1)

        Label(self.root, text="x: ").grid(row=2, column=2)
        Label(self.root, text="y: ").grid(row=3, column=2)
        Label(self.root, text="z: ").grid(row=4, column=2)

        self.x_input_box = Entry(self.root)
        self.y_input_box = Entry(self.root)
        self.z_input_box = Entry(self.root)
        self.x_input_box.insert(0, "100")
        self.y_input_box.insert(0, "100")
        self.z_input_box.insert(0, "100")
        self.x_input_box.grid(row=2, column=3)
        self.y_input_box.grid(row=3, column=3)
        self.z_input_box.grid(row=4, column=3)
        self.shift_button = Button(self.root, text='Shift', command=self.shift).grid(row=5, column=3)

        Label(self.root, text="angle: ").grid(row=2, column=6)
        self.angle_input_box = Entry(self.root)
        self.angle_input_box.insert(0, "45")
        self.angle_input_box.grid(row=3, column=6)

        self.x_rotate_button = Button(self.root, text='rotate about x', command=self.x_rotate).grid(row=4, column=6)
        self.y_rotate_button = Button(self.root, text='rotate about y', command=self.y_rotate).grid(row=5, column=6)
        self.z_rotate_button = Button(self.root, text='rotate about z', command=self.z_rotate).grid(row=6, column=6)

        Label(self.root, text="kx: ").grid(row=2, column=4)
        Label(self.root, text="ky: ").grid(row=3, column=4)
        Label(self.root, text="kz: ").grid(row=4, column=4)

        self.kx_input_box = Entry(self.root)
        self.ky_input_box = Entry(self.root)
        self.kz_input_box = Entry(self.root)
        self.kx_input_box.insert(0, "1")
        self.ky_input_box.insert(0, "1")
        self.kz_input_box.insert(0, "1")
        self.kx_input_box.grid(row=2, column=5)
        self.ky_input_box.grid(row=3, column=5)
        self.kz_input_box.grid(row=4, column=5)
        self.scale_button = Button(self.root, text='Scale', command=self.scale).grid(row=5, column=5)

        self.eraser_button = Button(self.root, text='Clear', command=self.erase)
        self.eraser_button.grid(row=3, column=8)

        self.redraw_button = Button(self.root, text='Redraw', command=self.redraw_all)
        self.redraw_button.grid(row=2, column=8)

        self.redraw_button = Button(self.root, text='Next', command=self.next_perspective)
        self.redraw_button.grid(row=4, column=8)

        self.redraw_all()

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

    def select_projection(self):
        projection_dict = {
            "orthographic_xoy": Projection.ORTHO_XOY,
            "orthographic_xoz": Projection.ORTHO_XOZ,
            "orthographic_yoz": Projection.ORTHO_YOZ,
            "isometric": Projection.ISOMETRIC,
            "dimetric": Projection.DIMETRIC,
            "perspective_one": Projection.PERSPECTIVE_1,
            "perspective_two": Projection.PERSPECTIVE_2,
            "perspective_three": Projection.PERSPECTIVE_3,
        }
        self.projection_type = projection_dict[self.projection_var.get()]
        self.redraw_all()

    def shift(self):
        figure = self.figure
        dx = float(self.x_input_box.get())
        dy = float(self.y_input_box.get())
        dz = float(self.z_input_box.get())
        figure.shift(dx, dy, dz)
        print("success translate dx={} dy={} dz={}".format(dx, dy, dz))
        self.redraw_all()

    def center_transform(func):
        def magic(self):
            mid_x, mid_y, mid_z = self.figure.center_point
            self.figure.shift(-mid_x, -mid_y, -mid_z)
            func(self)
            self.figure.shift(mid_x, mid_y, mid_z)
            self.redraw_all()
        return magic

    @center_transform
    def scale(self):
        figure = self.figure
        mx = float(self.kx_input_box.get())
        my = float(self.ky_input_box.get())
        mz = float(self.kz_input_box.get())
        figure.scale(mx, my, mz)
        print("success scale mx={} my={} mz={}".format(mx, my, mz))

    @center_transform
    def x_rotate(self):
        angle = float(self.angle_input_box.get()) * np.pi/ 180
        self.figure.rotate_x_axis(angle)

    @center_transform
    def y_rotate(self):
        angle = float(self.angle_input_box.get()) * np.pi/ 180
        self.figure.rotate_y_axis(angle)

    @center_transform
    def z_rotate(self):
        angle = float(self.angle_input_box.get()) * np.pi/ 180
        self.figure.rotate_z_axis(angle)

    def next_perspective(self):
        if self.projection_var.get() == "orthographic_xoy":
            self.projection_var.set("orthographic_xoz")
        elif self.projection_var.get() == "orthographic_xoz":
            self.x_rotate()
            self.x_rotate()
            self.projection_var.set("orthographic_yoz")
        elif self.projection_var.get() == "orthographic_yoz":
            for _ in range(6):
                self.x_rotate()
            self.projection_var.set("isometric")
        elif self.projection_var.get() == "isometric" and self.iso_mode == "iso_1":
            self.kx_input_box.delete(0, END)
            self.kx_input_box.insert(0, "0.5")
            self.scale()
            self.iso_mode = "iso_2"
        elif self.projection_var.get() == "isometric" and self.iso_mode == "iso_2":
            self.kx_input_box.delete(0, END)
            self.kx_input_box.insert(0, "2.0")
            self.ky_input_box.delete(0, END)
            self.ky_input_box.insert(0, "0.5")
            self.scale()
            self.iso_mode = "iso_3"
        elif self.projection_var.get() == "isometric" and self.iso_mode == "iso_3":
            self.kx_input_box.delete(0, END)
            self.kx_input_box.insert(0, "1.0")
            self.ky_input_box.delete(0, END)
            self.ky_input_box.insert(0, "2.0")
            self.scale()
            self.projection_var.set("dimetric")
        elif self.projection_var.get() == "dimetric":
            self.kx_input_box.delete(0, END)
            self.ky_input_box.delete(0, END)
            self.kz_input_box.delete(0, END)

            self.kx_input_box.insert(0, "1.4")
            self.ky_input_box.insert(0, "1.4")
            self.kz_input_box.insert(0, "1.4")
            self.scale()

            self.angle_input_box.delete(0, END)
            self.angle_input_box.insert(0, "70")
            self.y_rotate()

            self.projection_var.set("perspective_one")
        elif self.projection_var.get() == "perspective_one":
            self.figure = Chair()
            self.figure.rotate_x_axis_center(115 * np.pi/180)
            self.figure.scale_center(1.2, 1.2, 1.2)
            self.figure.shift(200, 200, 20)
            self.projection_var.set("perspective_two")
        elif self.projection_var.get() == "perspective_two":
            # self.figure = Chair()
            self.figure.scale_center(1.5, 1.5, 1.5)
            self.figure.rotate_x_axis_center(15 * np.pi/180)
            self.projection_var.set("perspective_three")

        self.select_projection()

    def redraw_all(self):
        self.erase()
        # self.figure.draw(self.draw, self.projection)
        figure_projection = self.project()
        for point_ind1, point_ind2 in figure_projection.edges:
            x1, y1 = figure_projection.point_list[point_ind1]
            x2, y2 = figure_projection.point_list[point_ind2]
            self.draw.line([x1, y1, x2, y2], width=1, fill=WorkArea.DEFAULT_COLOR)

        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def erase(self):
        self.canvas.delete("all")
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_WIDTH), 'white')
        self.draw = ImageDraw.Draw(self.image)


gui = WorkArea()
