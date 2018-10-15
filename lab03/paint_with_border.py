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
    for i in range(1, len(points)):
        _, y_prev = points[i - 1]
        x, y = points[i]
        _, y_next = points[i+1-points_len]
        ordered_all[y].append(x)
        if y_prev<y>y_next or y_prev>y<y_next:
            ordered_all[y].append(x)
        left_dir = 1 if y > y_prev else 2 if y < y_prev else 0
        right_dir = 1 if y > y_next else 2 if y < y_next else 0
        direction[(x, y)] = right_dir, left_dir

    for y in range(minY, maxY+1, 1):
        pair_complete = True
        points = sorted(ordered_all[y])
        length = len(points)

        # 1 - down, 2 - up, 0 - stay at on line
        i = 0
        left_pix = -1
        right_pix = -1
        while i < length:
            if pair_complete:
                complex_line = False
                if left_pix == -1:
                    left_pix = points[i]
                else:
                    complex_line = True
                x_next = points[i + 1 - length]
                while points[i] == x_next - 1:
                    i += 1
                    x_next = points[i + 1 - length]

                right_pix = points[i]
                left_dir = direction[(left_pix, y)]
                left_dir = left_dir[0] if left_dir[0] != 0 else left_dir[1]
                right_dir = direction[(right_pix, y)]
                right_dir = right_dir[1] if right_dir[1] != 0 else right_dir[0]
                if complex_line:
                    if (left_dir, right_dir) in {(2, 2), (1, 1)}:
                        ordered_points[y].append(right_pix)
                        pair_complete = False
                else:
                    if (left_dir, right_dir) in {(1, 2), (2, 1)}:
                        ordered_points[y].append(right_pix)
                        pair_complete = False

                left_pix = -1
                i += 1
            else:
                ordered_points[y].append(points[i])
                if points[i+1-length] == points[i]+1 or points[i+1-length] == points[i]:
                    left_pix = points[i]
                pair_complete = True
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
                    borders[y].add(x)

    return borders


def paint_figure(borders, image):
    draw = ImageDraw.Draw(image)
    for y in borders:
        points = list(sorted(borders[y]))
        for i in range(0, len(points)-len(points)%2, 2):
            x_l = points[i]
            x_r = points[i+1]

            draw.line((x_l+1, y, x_r-1, y), fill=(255, 0, 0, 255))