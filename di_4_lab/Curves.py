import io
import random
from copy import copy
from math import cos, sin, sqrt, acos
from tkinter import *

import numpy as np
from PIL import Image, ImageTk, ImageDraw

from Object3D import *


def get_middle_point(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x1 + x2)/2, (y1 + y2)/2


def get_curve_matrices():
    return {
        'hermit': np.array([
            [2,  -2,  1,  1],
            [-3,  3, -2, -1],
            [0,   0,  1,  0],
            [1,   0,  0,  0]
        ]),
        'bezier': np.array([
            [-1,  3, -3,  1],
            [3,  -6,  3,  0],
            [-3,  3,  0,  0],
            [1,   0,  0,  0]
        ]),
        'b_spline': np.array([
            [-1,  3, -3,  1],
            [3,  -6,  3,  0],
            [-3,  0,  3,  0],
            [1,   4,  1,  0]
        ])
        }


def get_curve_part(curve_matrix, points, k=1.0):
    points = np.array(points)
    drawed_points = []
    for t in np.arange(0, 1, 0.001):
        t_tenzor = np.array([t*t*t, t*t, t, 1]).reshape((1, 4))
        point = t_tenzor @ curve_matrix @ points * k
        drawed_points.append(point.tolist()[0])

    return drawed_points


def get_curve(curve_type, point_list):
    if curve_type == 'hermit':
        p1, p2, p3, p4 = point_list
        r1 = p1 - p2
        r4 = p4 - p3
        point_tensor = np.array([p1, p4, r1, r4])
        return get_curve_part(get_curve_matrices()['hermit'], point_tensor)
    elif curve_type == 'bezier':
        return get_curve_part(get_curve_matrices()['bezier'], point_list)
    elif curve_type == 'b_spline':
        return get_curve_part(get_curve_matrices()['b_spline'], point_list, 0.15)


def get_char_raw_points():
    return [
        # C
        [(0, 0), (3, 0), (3, 2), (2, 2), (2, 1), (1, 1), (1, 4), (2, 4), (2, 3), (3, 3), (3, 5), (0, 5)],
        # П
        [(0, 0), (3, 0), (3, 5), (2, 5), (2, 1), (1, 1), (1, 5), (0, 5)],
        # Л
        [(0, 1), (1, 0), (3, 0), (3, 5), (2, 5), (2, 1), (1, 1), (1, 5), (0, 5)],
        # А
        [(0, 1), (1, 0), (3, 0), (3, 5), (2, 5), (2, 4), (1, 4), (1, 5), (0, 5)],
        [(1, 1), (2, 1), (2, 3), (1, 3)],
        # Й
        [(0, 0), (1, 0), (1, 3), (2, 1), (2, 0), (3, 0), (3, 5), (2, 5), (2, 2), (1, 4), (1, 5), (0, 5)],
        [(1, -2), (2, -2), (2, -1), (1, -1)],
        # Н
        [(0, 0), (1, 0), (1, 2), (2, 2), (2, 0), (3, 0), (3, 5), (2, 5), (2, 3), (1, 3), (1, 5), (0, 5)]
    ]


def get_char_figures():
    char_points = get_char_raw_points()
    scale_size = 20
    char_points = [[(x+x_shift*scale_size, y+2, 0) for x, y in points]
                   for points, x_shift in zip(char_points, [0, 5, 10, 15, 15, 20, 20, 25])]
    figures = [Figure(points) for points in char_points]
    for fig in figures:
        fig.scale_center(scale_size, scale_size, scale_size)
        fig.shift(scale_size*3, scale_size*5, 0)
    figures[4].shift(0, -scale_size/2, 0)
    figures[6].shift(0, -scale_size*3.5, 0)
    return figures


class WorkArea:

    DEFAULT_WIDTH = 700
    DEFAULT_HEIGHT = 500
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.point_list = []
        self.figures = get_char_figures()

        self.root = Tk()
        self.root.title("CurvePro")
        self.root.resizable(False, False)

        self.draw_button = Button(self.root, text='add point', command=self.use_drawer)
        self.draw_button.grid(row=3, column=0)

        self.eraser_button = Button(self.root, text='Clear', command=self.clear_all)
        self.eraser_button.grid(row=3, column=3)

        self.canvas = Canvas(self.root, bg='white', width=self.DEFAULT_WIDTH, height=self.DEFAULT_HEIGHT)
        self.canvas.grid(row=1, columnspan=10)
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.normal_form_button = Button(self.root, text='normal form', command=self.line_draw)
        self.normal_form_button.grid(row=3, column=2)

        self.hermit_button = Button(self.root, text='hermit form', command=self.hermit_draw)
        self.hermit_button.grid(row=3, column=3)

        self.bezier_button = Button(self.root, text='bezier', command=self.bezier_draw)
        self.bezier_button.grid(row=3, column=4)

        self.b_spline_button = Button(self.root, text='B spline', command=self.b_spline_draw)
        self.b_spline_button.grid(row=3, column=5)

        self.additional_points = []
        self.movable_point_ind = None

        self.redraw_all()
        self.root.mainloop()

    def use_drawer(self):
        self.canvas.bind('<Button-1>', self.add_point)
        self.canvas.bind('<Button-3>', self.stop_drawing)

    def add_point(self, event):
        self.point_list.append((event.x, event.y))
        self.draw.ellipse([event.x-1, event.y-1, event.x+1, event.y+1], fill='red')
        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def remove(self, event):
        p_list = self.point_list
        for i in range(len(p_list)):
            if abs(event.x - p_list[i][0]) < 3 and abs(event.y - p_list[i][1]) < 3:
                self.point_list.remove(self.point_list[i])
                self.redraw_all()
                return

    def stop_removing(self, event):
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Button-3>')

    def clear_all(self):
        self.point_list = []
        self.use_eraser()

    def stop_drawing(self, event):
        self.redraw_all()
        print("stop drawing")

    def draw_line_figure(self, figure_ind):
        figure = self.figures[figure_ind]
        points = figure.take_xy_coords().point_list
        lines = [(p1, p2) for p1, p2 in zip(points, points[1:] + [points[0]])]
        for p1, p2 in lines:
            self.draw.line((*p1, *p2), fill=WorkArea.DEFAULT_COLOR)

    def line_draw(self):
        self.use_eraser()
        for i in range(len(self.figures)):
            self.draw_line_figure(i)

        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def hermit_draw(self):
        self.use_eraser()
        for fig in self.figures:
            point_list = fig.take_xy_coords().point_list.copy()
            self.draw_curves_hermit(point_list)

        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def bezier_draw(self):
        self.use_eraser()
        for fig in self.figures:
            point_list = fig.take_xy_coords().point_list.copy()
            self.draw_curves_bezier(point_list)

        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def b_spline_draw(self):
        self.use_eraser()
        for fig in self.figures:
            point_list = fig.take_xy_coords().point_list.copy()
            self.draw_curves_bspline(point_list)

        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def draw_curve(self, curve_points, color='black'):
        first_point = curve_points[0]
        image_draw = self.draw
        if len(curve_points) > 1:
            for point in curve_points[1:]:
                image_draw.line([first_point[0], first_point[1], point[0], point[1]], width=1, fill=color)
                first_point = point
        else:
            print("sorry, your line contains only 0 or 1 point")

    def draw_curves_hermit(self, point_list):
        if len(point_list) < 4:
            return

        if len(point_list) % 2 == 0:
            x1, y1 = point_list[0]
            x2, y2 = point_list[-1]
            fictive_point = (x1 + x2) / 2, (y1 + y2) / 2
            point_list.insert(0, fictive_point)
        point_list.append(point_list[0])

        first_point = point_list[0]
        new_point_list = [first_point]
        for i in range(1, len(point_list) - 2, 2):
            snd_point = point_list[i]
            trd_point = point_list[i + 1]
            add_point = get_middle_point(trd_point, point_list[i + 2])

            last_point = point_list[-1] if i + 3 == len(point_list) else add_point
            new_point_list += [snd_point, trd_point, last_point]
            if i + 3 == len(point_list):
                break

        cnt = len(new_point_list)
        new_point_list = new_point_list + new_point_list[:4]

        for i in range(cnt):
            points = new_point_list[i:i+4]
            points_tenzor = np.array([points[1], points[0], points[3], points[2]])
            hermit_curve = get_curve('hermit', points_tenzor)
            self.draw_curve(hermit_curve)

    def draw_curves_bezier(self, point_list):
        if len(point_list) < 4:
            return
        main_points = []
        if len(point_list) % 2 == 0:
            x1, y1 = point_list[0]
            x2, y2 = point_list[-1]
            fictive_point = (x1 + x2) / 2, (y1 + y2) / 2
            point_list.insert(0, fictive_point)
        point_list.append(point_list[0])

        first_point = point_list[0]
        for i in range(1, len(point_list)-2, 2):
            snd_point = point_list[i]
            trd_point = point_list[i+1]
            add_point = get_middle_point(trd_point, point_list[i+2])

            last_point = point_list[-1] if i+3 == len(point_list) else add_point
            main_points.append([first_point, snd_point, trd_point, last_point])
            if i + 3 == len(point_list):
                break

            first_point = add_point

        for points in main_points:
            bezier_curve = get_curve('bezier', points)
            self.draw_curve(bezier_curve)

    def draw_curves_bspline(self, point_list):
        cnt = len(point_list)
        point_list = point_list + point_list[:4]

        for i in range(cnt):
            points = point_list[i:i + 4]
            b_spline_curve = get_curve('b_spline', points)
            self.draw_curve(b_spline_curve)

    def redraw_all(self):
        self.use_eraser()

    def use_eraser(self):
        self.canvas.delete("all")
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_WIDTH), 'white')
        self.draw = ImageDraw.Draw(self.image)


gui = WorkArea()
