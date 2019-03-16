from Object3D import *
from Intersection import *
from tkinter import *
from PIL import Image, ImageTk, ImageDraw

f_points = [(60, 300), (100, 250), (140, 225), (180, 200), (220, 184), (260, 167), (300, 156), (340, 144), (380, 138),
            (420, 135), (460, 135), (500, 138), (540, 144), (580, 156), (620, 167), (660, 184), (700, 200), (740, 225),
            (780, 250), (820, 300)]
g_points = [(60, 130), (140, 132), (220, 133), (300, 135), (340, 136), (380, 140), (400, 150), (420, 164), (427, 195),
            (434, 232), (440, 250), (460, 270), (480, 277), (500, 280), (540, 285), (580, 286), (620, 287), (660, 290),
            (740, 291), (820, 293)]


class WorkArea:
    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 600
    DEFAULT_COLOR = 'black'
    INTERSECTION_COLOR = (139, 0, 255)

    def __init__(self):
        self.surface = LinedSurface(f_points, g_points)
        self.cylinder = Cylinder(30)
        self.cylinder_rad = 120
        # print(self.figure.point_list)
        # print(self.figure.edges)
        self.surface.scale(0.4, 0.4, 350.0)
        self.surface.shift(-180, -100, -180)
        self.surface.rotate_x_axis_center(np.pi / 2)

        self.cylinder.scale_center(self.cylinder_rad, self.cylinder_rad, 250)

        self.projection_type = Projection.ORTHO_XOY

        self.iso_mode = "iso_1"
        self.root = Tk()
        self.root.title("3DPRO")
        self.root.resizable(False, False)

        self.canvas = Canvas(self.root, bg='white', width=self.DEFAULT_WIDTH, height=self.DEFAULT_WIDTH)
        self.canvas.grid(row=1, columnspan=10)
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.image)

        # Label(self.root, text="Тип проекции:             ").grid(row=2, column=1)
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

        self.redraw_all()

        self.root.mainloop()

    def project(self, figure):
        projection_type = self.projection_type
        # Orthographic projections
        shifted_copy = make_clone(figure)
        shifted_copy.shift(300, 300, 200)
        if projection_type == Projection.ORTHO_XOY:
            return shifted_copy.orthographic_XOY().take_xy_coords()
        elif projection_type == Projection.ORTHO_XOZ:
            return shifted_copy.orthographic_XOZ().take_xz_coords()
        elif projection_type == Projection.ORTHO_YOZ:
            return shifted_copy.orthographic_YOZ().take_yz_coords()
        # Axonometric projections
        elif projection_type == Projection.ISOMETRIC:
            return shifted_copy.isometric().take_xy_coords()
        elif projection_type == Projection.DIMETRIC:
            return shifted_copy.dimetric().take_xy_coords()
        # Perspective projections
        elif projection_type == Projection.PERSPECTIVE_1:
            return shifted_copy.perspective_one_point().take_xy_coords()
        elif projection_type == Projection.PERSPECTIVE_2:
            return shifted_copy.perspective_two_point().take_xy_coords()
        elif projection_type == Projection.PERSPECTIVE_3:
            return shifted_copy.perspective_three_point().take_xy_coords()

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
        figure = self.surface
        dx = float(self.x_input_box.get())
        dy = float(self.y_input_box.get())
        dz = float(self.z_input_box.get())
        figure.shift(dx, dy, dz)
        print("success translate dx={} dy={} dz={}".format(dx, dy, dz))
        self.redraw_all()

    def center_transform(func):
        def magic(self):
            mid_x, mid_y, mid_z = self.surface.center_point
            self.surface.shift(-mid_x, -mid_y, -mid_z)
            func(self)
            self.surface.shift(mid_x, mid_y, mid_z)
            self.redraw_all()
        return magic

    @center_transform
    def scale(self):
        figure = self.surface
        mx = float(self.kx_input_box.get())
        my = float(self.ky_input_box.get())
        mz = float(self.kz_input_box.get())
        figure.scale(mx, my, mz)
        print("success scale mx={} my={} mz={}".format(mx, my, mz))

    @center_transform
    def x_rotate(self):
        angle = float(self.angle_input_box.get()) * np.pi/ 180
        self.surface.rotate_x_axis(angle)
        self.cylinder.rotate_x_axis(angle)

    @center_transform
    def y_rotate(self):
        angle = float(self.angle_input_box.get()) * np.pi/ 180
        self.surface.rotate_y_axis(angle)
        self.cylinder.rotate_y_axis(angle)

    @center_transform
    def z_rotate(self):
        angle = float(self.angle_input_box.get()) * np.pi/ 180
        self.surface.rotate_z_axis(angle)
        self.cylinder.rotate_z_axis(angle)

    def draw_figure(self, figure):
        figure_projection = self.project(figure)
        for point_ind1, point_ind2 in figure_projection.edges:
            x1, y1 = figure_projection.point_list[point_ind1]
            x2, y2 = figure_projection.point_list[point_ind2]
            self.draw.line([x1, y1, x2, y2], width=1, fill=WorkArea.DEFAULT_COLOR)

    def draw_intersection_points(self):
        surface = self.surface
        line_cnt_points = len(self.surface.point_list) // 2
        for surf_a, surf_b, surf_c, surf_d in zip(surface.point_list[:line_cnt_points],
                                                  surface.point_list[1:line_cnt_points],
                                                  surface.point_list[line_cnt_points:],
                                                  surface.point_list[line_cnt_points + 1:]
                                                  ):
            points = find_point_intersections((surf_a, surf_b), (surf_c, surf_d), 100, self.cylinder_rad)
            points = np.array([p for p in points])
            projected_points = self.project(Figure(points))
            # for x, y in projected_points:
            if len(projected_points.point_list) > 0:
                for x, y in projected_points.point_list:
                    self.draw.point([x, y], fill=WorkArea.INTERSECTION_COLOR)

    def redraw_all(self):
        self.erase()
        # self.figure.draw(self.draw, self.projection)
        self.draw_figure(self.surface)
        self.draw_figure(self.cylinder)
        self.draw_intersection_points()

        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def erase(self):
        self.canvas.delete("all")
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_WIDTH), 'white')
        self.draw = ImageDraw.Draw(self.image)

gui = WorkArea()

