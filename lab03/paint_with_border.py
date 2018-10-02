from tkinter import *
from enum import Enum
from PIL import ImageDraw
# from main import *

def get_borders(points):
    points = list(points)
    points_len = len(points)
    for i in range(len(points)):
        x, y = points[i]
        _, y_prev = points[i-1]
        _, y_next = points[i+1-points_len]
        if not(y_prev < y > y_next or y_prev > y < y_next or y_prev == y == y_next):
            ordered_points[y].add(x)

    return ordered_points

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
                    borders[y].add(x)

    return borders

def paint_figure(borders, image):
    draw = ImageDraw.Draw(image)
    for y in borders:
        points = list(borders[y])
        for i in range(0, len(points)-1, 2):
            x_l = points[i]
            x_r = points[i+1]

            draw.line((x_l, y, x_r, y), fill=(255, 0, 0, 255))
