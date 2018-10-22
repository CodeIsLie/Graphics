from triangulation import *
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw


class WorkArea:
    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 600
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.point_list = []

        self.root = Tk()
        self.root.title("Delone triangulation")
        self.root.resizable(False, False)

        self.eraser_button = Button(self.root, text='Clear', command=self.erase)
        self.eraser_button.grid(row=3, column=1)

        self.triangulation_button = Button(self.root, text='make triangulation') #, command=self.redraw_all)
        self.triangulation_button.grid(row=3, column=3)

        self.canvas = Canvas(self.root, bg='white', width=self.DEFAULT_WIDTH, height=self.DEFAULT_WIDTH)
        self.canvas.grid(row=1, columnspan=10)
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.bind('<Button-1>', self.draw_mod)

        self.root.mainloop()

    def add_point(self, x, y):
        self.point_list.append((x, y))

    def draw_mod(self, event):
        x = event.x
        y = event.y
        self.add_point(x, y)
        self.redraw_all()

    def erase(self):
        self.point_list = []
        self.use_eraser()

    def use_eraser(self):
        self.canvas.delete("all")
        self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_WIDTH), 'white')
        self.draw = ImageDraw.Draw(self.image)

    def redraw_all(self):
        self.use_eraser()
        for x, y in self.point_list:
            self.draw.ellipse([x-2, y-2, x+2, y+2], fill=(255, 0, 0))

        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')


gui = WorkArea()