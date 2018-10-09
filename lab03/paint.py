import io
import random
from copy import copy
from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk, ImageDraw
from tkcolorpicker import askcolor


class Paint:
    DEFAULT_PEN_SIZE = 4
    DEFAULT_WIDTH = 500
    DEFAULT_HEIGHT = 500
    DEFAULT_FILL_COLOR = (255, 0, 0)
    RANDOM_COLOR = (241, 128, 213)
    DEFAULT_BRUSH_COLOR = 'black'
    DEFAULT_BORDER_COLOR = (123, 156, 234)
    DEFAULT_HEX_VALUE = '#ff0000'
    DEFAULT_FILL_IMAGE = 'default_filler.jpg'

    def __init__(self):
        self.root = Tk()
        self.root.config(cursor='pencil')
        self.root.title("PainterPRO")
        self.root.resizable(False, False)

        self.brush_button = Button(self.root, text='Brush', command=self.use_brush)
        self.brush_button.grid(row=1, column=0)

        self.fill_color_button = Button(self.root, text='Color Filler', command=self.use_color_filler)
        self.fill_color_button.grid(row=1, column=1)

        self.fill_image_button = Button(self.root, text='Image Filler', command=self.use_image_filler)
        self.fill_image_button.grid(row=1, column=2)

        self.pick_color_button = Button(self.root, text='Pick color', command=self.pick_color)
        self.pick_color_button.grid(row=1, column=3)

        self.eraser_button = Button(self.root, text='Clear', command=self.use_eraser)
        self.eraser_button.grid(row=1, column=4)
        self.to_fill_points = set({})

        self.current_mode = 'draw'
        self.canvas = Canvas(self.root, bg='white', width=self.DEFAULT_WIDTH, height=self.DEFAULT_WIDTH)
        self.canvas.grid(row=0, columnspan=10)
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.old_x = None
        self.old_y = None
        self.fill_image = Image.open(self.DEFAULT_FILL_IMAGE)
        self.picked_hex_value = self.DEFAULT_HEX_VALUE
        self.picked_color = self.DEFAULT_FILL_COLOR
        self.line_width = self.DEFAULT_PEN_SIZE
        self.use_eraser()

        self.bind_draw()
        self.root.mainloop()

    def use_brush(self):
        self.current_mode = 'draw'
        self.root.config(cursor='pencil')
        self.canvas.unbind('<Button-1>')
        self.bind_draw()

    def bind_draw(self):
        self.canvas.bind('<B1-Motion>', self.draw_line)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def use_image_filler(self):
        self.current_mode = 'fill_image'
        self.root.config(cursor='box_spiral')
        self.canvas.bind('<Button-1>', self.fill_area)
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')

    def use_color_filler(self):
        self.current_mode = 'fill'
        cursor_str = 'coffee_mug' + ' ' + self.picked_hex_value
        self.root.config(cursor=cursor_str)
        self.canvas.bind('<Button-1>', self.fill_area)
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')

    def pick_color(self):
        color = askcolor(title='Choose color')
        self.picked_color = color[0]
        self.picked_hex_value = color[1]
        if self.current_mode == 'fill':
            cursor_str = 'coffee_mug' + ' ' + self.picked_hex_value
            self.root.config(cursor=cursor_str)

    def use_eraser(self):
        self.canvas.delete("all")
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_WIDTH), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.draw.rectangle([0, 0, self.DEFAULT_WIDTH - 1, self.DEFAULT_HEIGHT - 1], outline=self.DEFAULT_BORDER_COLOR)
        self.image.save('out.png', 'PNG')

    def fill_alg(self, point, start_pix_color):
        pix = self.image.load()
        current_x = point[0]
        current_y = point[1]
        if pix[current_x, current_y] != start_pix_color:
            return

        while pix[current_x, current_y] == start_pix_color:
            current_x -= 1
        left_bound = current_x

        current_x = point[0]
        while pix[current_x, current_y] == start_pix_color:
            current_x += 1
        right_bound = current_x

        self.draw_fill_line(left_bound, right_bound, point[1])

        for x in range(left_bound, right_bound + 1):
            if pix[x, point[1] + 1] == start_pix_color:
                self.fill_alg((x, point[1] + 1), start_pix_color)

        for x in range(left_bound, right_bound + 1):
            if pix[x, point[1] - 1] == start_pix_color:
                self.fill_alg((x, point[1] - 1), start_pix_color)

    def draw_fill_line(self, left_bound, right_bound, y):
        if self.current_mode == 'fill':
            self.draw.line([left_bound + 1, y, right_bound - 1, y], width=1, fill=self.picked_color)
        elif self.current_mode == 'fill_image':
            # pix = self.fill_image.load()
            for i in range(left_bound + 1, right_bound):
                self.to_fill_points.add((i, y))
                self.draw.line([left_bound + 1, y, right_bound - 1, y], width=1, fill=self.RANDOM_COLOR)
                # self.draw.point((i, y), pix[i % self.fill_image.width, y % self.fill_image.height])

    def draw_image(self):
        pix = self.fill_image.load()
        for (x, y) in self.to_fill_points:
            self.draw.point((x, y), pix[x % self.fill_image.width, y % self.fill_image.height])

    def fill_area(self, event):
        if event.x <= 1 or event.x >= self.DEFAULT_WIDTH - 1 or event.y <= 1 or event.y >= self.DEFAULT_HEIGHT - 1:
            return

        pix = self.image.load()
        start_x = event.x - 1
        start_y = event.y - 1

        if self.current_mode == 'fill_image' or pix[start_x, start_y] != self.picked_color:
            self.fill_alg((start_x, start_y), pix[start_x, start_y])

        # self.image.save('out.png', 'PNG')
        if self.current_mode == 'fill_image':
            self.draw_image()
        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
        self.draw.rectangle([1, 1, self.DEFAULT_WIDTH - 1, self.DEFAULT_HEIGHT - 1], outline=self.DEFAULT_BORDER_COLOR)

        self.to_fill_points = set({})

    def draw_line(self, event):
        self.line_width = self.DEFAULT_PEN_SIZE
        if self.old_x and self.old_y:
            self.draw.line([self.old_x, self.old_y, event.x - 1, event.y - 1],
                           fill=self.DEFAULT_BRUSH_COLOR, width=self.line_width)
            self.canvas.image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

        self.old_x = event.x - 1
        self.old_y = event.y - 1
        self.draw.rectangle([1, 1, self.DEFAULT_WIDTH - 1, self.DEFAULT_HEIGHT - 1], outline=self.DEFAULT_BORDER_COLOR)

    def reset(self, event):
        self.old_x, self.old_y = None, None


gui = Paint()