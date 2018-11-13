"""
3. Построение графика двух переменных
Сегмент поверхности задаётся функцией f(x, y) = z, диапазонами отсечения [x0, x1], [y0, y1]
и количеством разбиений по осям (шагом).
Программа должна позволять строить сегмент поверхности, заданный выбранной функцией на
заданном диапазоне с заданным количеством разбиений. Формат модели должен содержать данные о гранях.
Диапазоны и разбиения можно задавать идентичными для X и Y.
Необходимо отобразить полученную модель, позволить применять к ней аффинные преобразования.

Сохранить полученную модель в файл.*
"""

from Affine3D import *
from tkinter import *
from tkinter import filedialog
import numpy as np
from Camera import *

from PIL import Image, ImageTk, ImageDraw


def sin3d(x, y):
    return np.sin(x + y)


def flower_rose(x, y):
    return 100 - 3/np.sqrt(x*x + y*y) + np.sin(np.sqrt(x*x + y*y)) + \
           np.sqrt(200 - x*x + y*y + 10*np.sin(x) + 10*np.sin(y))/1000


class WorkArea:

    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 600
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.figure_list = [Polyhedron.get_cube()
                            #Polyhedron.get_ikosaeder()
             ]
        self.figure_list[0].scale(150, 150, 150)
        self.cur_figure_ind = 0

        self.root = Tk()
        self.root.title("3DPRO")
        self.root.resizable(False, False)

        self.eraser_button = Button(self.root, text='Clear', command=self.use_eraser)
        self.eraser_button.grid(row=3, column=1)

        self.redraw_button = Button(self.root, text='Redraw', command=self.redraw_all)
        self.redraw_button.grid(row=2, column=1)

        self.canvas = Canvas(self.root, bg='white', width=self.DEFAULT_WIDTH, height=self.DEFAULT_HEIGHT)
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

        self.rotate_button = Button(self.root, text='Rotate', command=self.rotate_all_axis)
        self.rotate_button.grid(row=6, column=3)

        self.center_scale_button = Button(self.root, text='Center Scale', command=self.center_scale)
        self.center_scale_button.grid(row=6, column=2)

        self.rotate_x_center_button = Button(self.root, text='Rotate about center x', command=self.rotate_x_center)
        self.rotate_x_center_button.grid(row=6, column=4)

        self.rotate_y_center_button = Button(self.root, text='Rotate about center y', command=self.rotate_y_center)
        self.rotate_y_center_button.grid(row=6, column=5)

        self.rotate_z_center_button = Button(self.root, text='Rotate about center z', command=self.rotate_z_center)
        self.rotate_z_center_button.grid(row=6, column=6)

        self.rotate_z_center_button = Button(self.root, text='Draw Graphic', command=self.graph_draw)
        self.rotate_z_center_button.grid(row=6, column=7)

        Label(self.root, text="count graph segments:").grid(row=7, column=2)
        self.segments_box = Entry(self.root)
        self.segments_box.insert(0, "40")
        self.segments_box.grid(row=8, column=2)

        Label(self.root, text="start x:").grid(row=7, column=3)
        self.x_start_box = Entry(self.root)
        self.x_start_box.insert(0, "-10")
        self.x_start_box.grid(row=8, column=3)

        Label(self.root, text="end x:").grid(row=7, column=4)
        self.x_end_box = Entry(self.root)
        self.x_end_box.insert(0, "10")
        self.x_end_box.grid(row=8, column=4)

        Label(self.root, text="start y:").grid(row=9, column=3)
        self.y_start_box = Entry(self.root)
        self.y_start_box.insert(0, "-10")
        self.y_start_box.grid(row=10, column=3)

        Label(self.root, text="end y:").grid(row=9, column=4)
        self.y_end_box = Entry(self.root)
        self.y_end_box.insert(0, "10")
        self.y_end_box.grid(row=10, column=4)

        self.save_button = Button(self.root, text='Save', command=self.save)
        self.save_button.grid(row=10, column=5)

        self.open_button = Button(self.root, text='Open', command=self.open_figure)
        self.open_button.grid(row=10, column=6)

        self.solid_revolution_button = Button(self.root, text='Solid of revolution', command=self.solid_of_revolution)
        self.solid_revolution_button.grid(row=11, column=2)

        self.x_check_box = IntVar()
        Checkbutton(self.root, text="X", variable=self.x_check_box).grid(row=11, column=5)
        self.y_check_box = IntVar()
        Checkbutton(self.root, text="Y", variable=self.y_check_box).grid(row=11, column=6)
        self.z_check_box = IntVar()
        Checkbutton(self.root, text="Z", variable=self.z_check_box).grid(row=11, column=7)

        self.splits_count_box = Entry(self.root)
        self.splits_count_box.insert(0, "10")
        self.splits_count_box.grid(row=11, column=4)
        Label(self.root, text="splits count: ").grid(row=11, column=3)

        self.open_button = Button(self.root, text='Create camera', command=self.create_camera)
        self.open_button.grid(row=8, column=5)

        self.root.mainloop()

    def create_camera(self):
        r = -1/10
        matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, r],
            [0, 0, 0, 1]
        ])
        camera = Camera((0, 0, 0), None, self.figure_list[self.cur_figure_ind], matrix)

        self.use_eraser()
        camera.switch_to_camera_view(self.draw)
        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')


    def solid_of_revolution(self):
        self.canvas.bind('<Button-1>', self.add_generatrix_point)
        self.canvas.bind('<Button-3>', self.stop_adding_generatrix_point)
        self.generatrix_points = []

    def add_generatrix_point(self, event):
        self.generatrix_points.append((event.x, event.y))
        points_len = len(self.generatrix_points)
        if points_len > 1:
            self.canvas.create_line(
                self.generatrix_points[points_len - 2][0], self.generatrix_points[points_len - 2][1],
                self.generatrix_points[points_len - 1][0], self.generatrix_points[points_len - 1][1])

    def stop_adding_generatrix_point(self, event):
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Button-3>')
        split_count = int(self.splits_count_box.get())
        theta = 360 / split_count
        theta = theta * np.pi / 180
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        x_matrix = np.array([
            [1, 0, 0, 0],
            [0, cos_theta, -sin_theta, 0],
            [0, sin_theta, cos_theta, 0],
            [0, 0, 0, 1]
        ])

        y_matrix = np.array([
            [cos_theta, 0, sin_theta, 0],
            [0, 1, 0, 0],
            [-sin_theta, 0, cos_theta, 0],
            [0, 0, 0, 1]
        ])

        z_matrix = np.array([
            [cos_theta, -sin_theta, 0, 0],
            [sin_theta, cos_theta, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        x_checked = self.x_check_box.get()
        z_checked = self.x_check_box.get()

        rotation_matrix = y_matrix

        if x_checked:
            rotation_matrix = x_matrix
        if z_checked:
            rotation_matrix = z_matrix

        points = []
        for (x, y) in self.generatrix_points:
            points.append((x, y, 0))
            print(x, y)

        all_points = [points]
        for i in range(1, split_count):
            new_points = []
            for point in all_points[len(all_points) - 1]:
                new_point = point_transform(point, rotation_matrix.transpose())
                new_points.append(new_point)
            all_points.append(new_points)

        edges = []
        for i in range(0, split_count):
            for j in range(0, len(all_points[i]) - 1):
                edges.append(Polygon([all_points[i][j], all_points[i][j+1], all_points[(i+1) % split_count][j+1], all_points[(i+1) % split_count][j]]))
        p = Polyhedron(edges, (0, 0, 0))
        self.figure_list = [p]
        self.cur_figure_ind = 0
        self.redraw_all()

    def create_func_figure(self, f):
        # matrix of all points of functions
        func_points = []
        cnt_segments = int(self.segments_box.get())
        x_start = float(self.x_start_box.get())
        x_end = float(self.x_end_box.get())
        y_start = float(self.y_start_box.get())
        y_end = float(self.y_end_box.get())
        for x in np.linspace(x_start, x_end, cnt_segments):
            line = []
            for y in np.linspace(y_start, y_end, cnt_segments):
                line.append((x, y, f(x, y)))
            func_points.append(line)

        polygons = []
        for i in range(0, cnt_segments-1):
            for j in range(0, cnt_segments-1):
                polygons.append(Polygon([
                    func_points[i][j],
                    func_points[i+1][j],
                    func_points[i+1][j+1],
                    func_points[i][j+1]
                ]))

        print("start point is {}".format(func_points[0][0]))
        return Polyhedron(polygons)

    def graph_draw(self):
        # self.figure_list = [self.create_func_figure(sin3d)]
        # self.figure_list = [self.create_func_figure(lambda x, y: x*y)]
        self.figure_list = [self.create_func_figure(lambda x, y: np.sin(x) * np.cos(y))]
        self.figure_list[0].translate(300, 300, 300)
        self.figure_list[0].center_scale(25, 25, 25)
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

    def rotate_x_center(self):
        figure = self.figure_list[self.cur_figure_ind]
        angle_value = self.x_angle_input_box.get()
        if len(angle_value) == 0:
            return
        x, y, z = figure.center_point
        figure.rotate_about_vector(float(angle_value), x, y, z, x + 10, y, z)
        self.redraw_all()

    def rotate_y_center(self):
        figure = self.figure_list[self.cur_figure_ind]
        angle_value = self.y_angle_input_box.get()
        if len(angle_value) == 0:
            return
        x, y, z = figure.center_point
        figure.rotate_about_vector(float(angle_value), x, y, z, x, y + 10, z)
        self.redraw_all()

    def rotate_z_center(self):
        figure = self.figure_list[self.cur_figure_ind]
        angle_value = self.z_angle_input_box.get()
        if len(angle_value) == 0:
            return
        x, y, z = figure.center_point
        figure.rotate_about_vector(float(angle_value), x, y, z, x, y, z + 10)
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
        self.rotate_x_axis()
        self.rotate_y_axis()
        self.rotate_z_axis()

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

    def save(self):
        self.figure_list[0].save_in_file()

    def open_figure(self):
        self.figure_list[0] = Polyhedron.open_from_file()
        self.redraw_all()


gui = WorkArea()
