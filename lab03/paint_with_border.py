from tkinter import *
from enum import Enum
from PIL import ImageDraw
# from main import *

def get_borders(points):
    _, y_coordinates = list(zip(*points))
    minY = min(y_coordinates)
    maxY = max(y_coordinates)

    ordered_points = dict()
    ordered_all = dict()
    for i in range(minY, maxY+1):
        ordered_points[i] = []
        ordered_all[i] = []

    points_len = len(points)
    direction = dict()
    for i in range(len(points)):
        _, y_prev = points[i - 1]
        x, y = points[i]
        _, y_next = points[i+1-points_len]
        ordered_all[y].append(x)
        if y_prev<y>y_next or y_prev>y<y_next:
            ordered_all[y].append(x)
        direction[(x,y)] = 1 if y > y_prev else 2 if y < y_prev else 0

    for y in range(minY, maxY+1, 1):
        pair_complete = True
        points = sorted(ordered_all[y])
        length = len(points)

        # 1 - down, 2 - up, 0 - stay at on line
        long_line = False
        start_direction = 0
        i = 0
        while i < length:
            if pair_complete:
                if start_direction == 0:
                    start_direction = direction[(points[i], y)]
                x_next = points[i + 1 - length]
                while points[i] == x_next - 1:
                    i += 1
                    x_next = points[i + 1 - length]
                    long_line = True

                cur_direction = direction[(x_next, y)]
                if long_line:
                    if (start_direction, cur_direction) in {(1, 2), (2, 1)}:
                        ordered_points[y].append(points[i])
                        pair_complete = False
                else:
                    ordered_points[y].append(points[i])
                    pair_complete = False

                long_line = False
                i += 1
            else:
                ordered_points[y].append(points[i])
                pair_complete = True
                start_direction = direction[(points[i], y)]
                long_line = points[i + 1 - length] == points[i] + 1
                i += 1

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
                    borders[y].add(x) #


    return borders


def paint_figure(borders, image):
    draw = ImageDraw.Draw(image)
    for y in borders:
        points = list(sorted(borders[y]))
        for i in range(0, len(points)-len(points)%2, 2):
            x_l = points[i]
            x_r = points[i+1]

            draw.line((x_l+1, y, x_r-1, y), fill=(255, 0, 0, 255))
