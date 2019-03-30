import io
import random
from copy import copy
from math import cos, sin, sqrt, acos
from tkinter import *
from tkinter import filedialog
from enum import Enum

import numpy as np
from PIL import Image, ImageTk, ImageDraw


def get_Bezier_point(points, t):
    # if len(points) != 4:
    #     return None
    t_ = 1-t
    points_tensor = np.array(points)
    points_tensor[1] *= 3
    points_tensor[2] *= 3
    points_tensor.transpose()
    t_tenzor = np.array([t_ * t_ * t_,
                         t_ * t_ * t,
                         t_ * t * t,
                         t * t * t])
    t_tenzor.transpose()
    res = np.dot(t_tenzor, points_tensor)
    # print(res)
    return res

def get_Bezie_curve(main_points):
    t = 0
    points = []
    while t < 1+0.005:
        points.append(get_Bezier_point(main_points, t))
        t += 0.01

    return points

def get_middle_point(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x1 + x2)/2, (y1 + y2)/2

class WorkArea:

    DEFAULT_WIDTH = 500
    DEFAULT_HEIGHT = 500
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.point_list = []
        self.current_primitive_ind = -1

        self.root = Tk()
        self.root.title("BezierPro")
        self.root.resizable(False, False)

        self.draw_button = Button(self.root, text='add point', command=self.use_drawer)
        self.draw_button.grid(row=3, column=0)

        self.del_button = Button(self.root, text='delete point', command=self.remove_point)
        self.del_button.grid(row=3, column=1)

        self.move_button = Button(self.root, text='move point', command=self.use_mover)
        self.move_button.grid(row=3, column=2)

        self.eraser_button = Button(self.root, text='Clear', command=self.clear_all)
        self.eraser_button.grid(row=3, column=3)

        Label(self.root, text="Draw points here: ").grid(row=0, column=3)

        self.canvas = Canvas(self.root, bg='white', width=self.DEFAULT_WIDTH, height=self.DEFAULT_WIDTH)
        self.canvas.grid(row=1, columnspan=10)
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.point_location_label = Label(self.root, text='')
        self.point_location_label.grid(row=5, column=4)

        self.additional_points = []
        self.movable_point_ind = None

        self.root.mainloop()

    def use_drawer(self):
        self.canvas.bind('<Button-1>', self.add_point)
        self.canvas.bind('<Button-3>', self.stop_drawing)

    def add_point(self, event):
        self.point_list.append((event.x, event.y))
        self.draw.ellipse([event.x-1, event.y-1, event.x+1, event.y+1], fill='red')
        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def remove_point(self):
        self.canvas.bind('<Button-1>', self.remove)
        self.canvas.bind('<Button-3>', self.stop_removing)

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
        # self.canvas.unbind('<Button-1>')
        # self.canvas.unbind('<Button-3>')
        # self.draw_current_primitive()

    def draw_curve(self, curve_points, image_draw, color='black'):
        first_point = curve_points[0]
        if len(curve_points) > 1:
            for point in curve_points[1:]:
                image_draw.line([first_point[0], first_point[1], point[0], point[1]], width=1, fill=color)
                first_point = point
        else:
            print("sorry, your line contains only 0 or 1 point")

    def draw_curves(self):
        if len(self.point_list) < 4:
            return
        self.additional_points = []

        main_points = []
        fictive_point = None
        if len(self.point_list) % 2 == 1:
            x1, y1 = self.point_list[-1]
            x2, y2 = self.point_list[-2]
            fictive_point = (x1 + x2) / 2, (y1 + y2) / 2
            self.point_list.insert(-1, fictive_point)

        first_point = self.point_list[0]
        for i in range(1, len(self.point_list)-2, 2):
            snd_point = self.point_list[i]
            trd_point = self.point_list[i+1]
            add_point = get_middle_point(trd_point, self.point_list[i+2])

            last_point = self.point_list[-1] if i+3 == len(self.point_list) else add_point
            main_points.append([first_point, snd_point, trd_point, last_point])
            if i + 3 == len(self.point_list):
                break

            first_point = add_point
            self.additional_points.append(add_point)

        # main_points = [self.point_list[:4]]
        for points in main_points:
            bezier_curve = get_Bezie_curve(points)
            self.draw_curve(bezier_curve, self.draw)
            self.canvas.image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

        if fictive_point is not None:
            self.point_list.remove(fictive_point)

    def draw_points(self):
        for x, y in self.point_list:
            self.draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill='red')
            self.canvas.image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def draw_add_points(self):
        for x, y in self.additional_points:
            self.draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill='green')
            self.canvas.image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def redraw_all(self):
        self.use_eraser()
        self.draw_curves()
        self.draw_points()

    def use_eraser(self):
        self.canvas.delete("all")
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_WIDTH), 'white')
        self.draw = ImageDraw.Draw(self.image)

    def use_mover(self):
        self.canvas.bind('<Button-1>', self.select_point)

    def select_point(self, event):
        p_list = self.point_list
        for i in range(len(p_list)):
            if abs(event.x - p_list[i][0]) < 3 and abs(event.y - p_list[i][1]) < 3:
                self.movable_point_ind = i
                self.canvas.bind('<Button-1>', self.move_point)
                return

    def move_point(self, event):
        self.canvas.unbind('<Button-1>')
        if self.movable_point_ind is None:
            return
        self.point_list[self.movable_point_ind] = event.x, event.y
        self.movable_point_ind = None
        self.redraw_all()

gui = WorkArea()
