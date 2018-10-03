from tkinter import *
from enum import Enum
from paint_with_border import *

from PIL import Image, ImageTk, ImageDraw

DEFAULT_WIDTH = 500
DEFAULT_HEIGHT = 500


class Direction(Enum):
    Down = 0
    DownLeft = 1
    Left = 2
    UpLeft = 3
    Up = 4
    UpRight = 5
    Right = 6
    DownRight = 7


def shift_r_by_n(arr, n=0):
    return arr[len(arr) - n:] + arr[0:len(arr) - n]


def get_neighbours(direction, point):
    current_x = point[0]
    current_y = point[1]

    res = [((current_x - 1, current_y), Direction.Left),\
            ((current_x - 1, current_y + 1), Direction.DownLeft),\
            ((current_x, current_y + 1), Direction.Down),\
            ((current_x + 1, current_y + 1), Direction.DownRight),\
            ((current_x + 1, current_y), Direction.Right),\
            ((current_x + 1, current_y - 1), Direction.UpRight),\
            ((current_x, current_y - 1), Direction.Up),\
            ((current_x - 1, current_y - 1), Direction.UpLeft)]

    return shift_r_by_n(res, direction.value)


def calc_points(point, border_color):
    pix = image.load()
    current_x = point[0]
    current_y = point[1]

    while pix[current_x + 1, current_y] != border_color and current_x <= DEFAULT_WIDTH - 1:
        current_x += 1
    current_x += 1

    if current_x == DEFAULT_WIDTH:
        return {()}

    start_x = current_x
    start_y = current_y

    res_points_set = [(current_x, current_y)]
    current_direction = Direction.Down

    for x in get_neighbours(current_direction, (current_x, current_y)):
        if pix[x[0][0], x[0][1]] == border_color:
            res_points_set.append(x[0])
            current_x = x[0][0]
            current_y = x[0][1]
            current_direction = x[1]
            break
    while current_x != start_x or current_y != start_y:
        # print((current_x, current_y))
        neighbours = get_neighbours(current_direction, (current_x, current_y))
        for x in neighbours:
            # print('  ', x)
            if pix[x[0][0], x[0][1]] == border_color:
                # print('    ', x)
                res_points_set.append(x[0])
                current_x = x[0][0]
                current_y = x[0][1]
                current_direction = x[1]
                break

    return res_points_set


def paint(event):
    if event.x <= 1 or event.x >= DEFAULT_WIDTH - 1 or event.y <= 1 or event.y >= DEFAULT_HEIGHT - 1:
        return

    start_x = event.x - 1
    start_y = event.y - 1

    border_points = calc_points((start_x, start_y), (0, 0, 0, 255))
    border_points = get_borders(border_points)
    paint_figure(border_points, image)

    # draw.rectangle([1, 1, DEFAULT_WIDTH - 1, DEFAULT_HEIGHT - 1], outline='black')
    canvas.image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=canvas.image, anchor='nw')

def select_borders(event):
    if event.x <= 1 or event.x >= DEFAULT_WIDTH - 1 or event.y <= 1 or event.y >= DEFAULT_HEIGHT - 1:
        return

    pix = image.load()
    start_x = event.x - 1
    start_y = event.y - 1

    border_points = calc_points((start_x, start_y), (0, 0, 0, 255))

    for x, y in border_points:
        pix[x, y] = (0, 255, 0, 255)

    # draw.rectangle([1, 1, DEFAULT_WIDTH - 1, DEFAULT_HEIGHT - 1], outline='black')
    canvas.image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=canvas.image, anchor='nw')

root = Tk()
root.title("Border Picker")
root.resizable(False, False)

canvas = Canvas(root, bg='white', width=DEFAULT_WIDTH, height=DEFAULT_WIDTH)
canvas.grid(row=0, columnspan=10)

image = Image.open("in.png")
draw = ImageDraw.Draw(image)

canvas.image = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, image=canvas.image, anchor='nw')

canvas.bind('<Button-1>', paint)

root.mainloop()