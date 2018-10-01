from tkinter import *
from enum import Enum
# from main import *

def get_borders(point, border_color):
    points = calc_points(point, border_color)
    _, y_coordinates = list(zip(*points))
    minY = min(y_coordinates)
    maxY = max(y_coordinates)

    ordered_points = dict()
    for i in range(minY, maxY+1):
        ordered_points[i] = {}

    points_len = len(points)
    for i in range(len(points)):
        x, y = points[i]
        _, y_prev = point[i-1]
        _, y_next = points[i+1-points_len]
        if not(y_prev < y > y_next or y_prev > y < y_next or y_prev == y == y_next):
            ordered_points[y].add(x)

def find_holes(borders, image, border_color):
    # UPD borders with respect to holes inside figure
    pix = image.load()
    for y in borders:
        points = list(borders[y].copy())
        for i in range(0, len(points), 2):
            x_l = points[i]
            x_r = points[i+1]
            for x in range(x_l+1, x_r, 1):
                if pix[x, y] != border_color:
                    borders[y].add(x) #


    return borders

def paint(borders, image):
    for ys in borders:
        y = ys
        points = borders[y]
        for i in range(0, len(points), 2):
            x_l = points[i]
            x_r = points[i+1]
            print(x_l, x_r)
            # paint all points on image from xl+1 to xr-1 by paint_color

borders = {1:[2,3], 2:[3,4]}
paint(borders, 1)