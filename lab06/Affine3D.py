import numpy as np

'''
В программе должны присутствовать следующие классы: точка, прямая (ребро), многоугольник (грань), многогранник.

Программа должна содержать следующие возможности:

Отображение одного из правильных многогранников: тетраэдр, гексаэдр, октаэдр, икосаэдр*, додекаэдр*.
Применение аффинных преобразований: смещение, поворот, масштаб, с указанием параметров преобразования. 
Преобразования должны быть реализованы матрицами!
'''

DEFAULT_COLOR = 'black'

class Edge:
    def __init__(self, points=None):
        self.points = [] if points is None else points

    def add_point(self, point):
        self.points.append(point)

    def point_count(self):
        return len(self.points)

    def get_transformed_points(self, matrix):
        new_points = []
        for x, y, z in self.points:
            point_tensor = np.array([x, y, z, 1])
            new_point = np.dot(point_tensor, matrix)[:3]
            new_points.append(new_point)
        return new_points

    def transform(self, matrix):
        self.points = self.get_transformed_points(matrix)

    def translate(self, tx, ty, tz):
        translation_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [tx, ty, tz, 1]
        ])
        self.transform(translation_matrix)

    def scale(self, mx, my, mz):
        scale_matrix = np.array([
            [mx, 0, 0, 0],
            [0, my, 0, 0],
            [0, 0, mz, 0],
            [0, 0, 0, 1]
        ])
        self.transform(scale_matrix)

    def rotate_x_axis(self, theta):
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        rotation_matrix = np.array([
            [1, 0, 0, 0],
            [0, cos_theta, -sin_theta, 0],
            [0, sin_theta, cos_theta, 0],
            [0, 0, 0, 1]
        ])
        self.transform(rotation_matrix.transpose())

    def rotate_y_axis(self, theta):
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        rotation_matrix = np.array([
            [cos_theta, 0, sin_theta, 0],
            [0, 1, 0, 0],
            [-sin_theta, 0, cos_theta, 0],
            [0, 0, 0, 1]
        ])
        self.transform(rotation_matrix.transpose())

    def rotate_z_axis(self, theta):
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        rotation_matrix = np.array([
            [cos_theta, -sin_theta, 0, 0],
            [sin_theta, cos_theta, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.transform(rotation_matrix.transpose())

    def to_2D(self, fov_h, fov_w, z_n, z_f):
        w = 1 / np.tan(fov_w / 2)
        h = 1 / np.tan(fov_h / 2)
        q = z_f / (z_f - z_n)
        matrix = np.array([
            [w, 0, 0, 0],
            [0, h, 0, 0],
            [0, 0, q, 1],
            [0, 0, -q * z_n, 0]
        ])
        points = self.get_transformed_points(matrix)
        points = [x[:2] for x in points]
        lines = list(zip(points, [points[-1]]+points[0:-1]))
        return lines

    def __str__(self):
        s = ""
        for x, y, z in self.points:
            s += "({}, {}, {}) ".format(x, y, z)
        s += "\n"
        return s


# многогранник
class Polyhedron:
    def __init__(self, edges=None):
        self.edges = [] if edges is None else edges

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_draw_lines(self):
        res = []
        for edge in self.edges:
            res += edge.to_2D(90, 90, 300, 1000)
        return res

    def translate(self, dx, dy, dz):
        for edge in self.edges:
            edge.translate(dx, dy, dz)

    def scale(self, dx, dy, dz):
        for edge in self.edges:
            edge.scale(dx, dy, dz)

    def rotate_all(self, angle_x, angle_y, angle_z):
        for edge in self.edges:
            edge.rotate_x_axis(angle_x * np.pi/180)
            edge.rotate_y_axis(angle_y * np.pi/180)
            edge.rotate_z_axis(angle_z * np.pi/180)

    def draw(self, image_draw):
        # TODO: remove this from draw
        self.scale(100, 100, 100)
        self.rotate_all(30, 30, 30)
        self.translate(160, 160, 160)

        lines = self.get_draw_lines()
        # for edge in self.edges:

        for i in range(len(lines)):
            x1, y1 = lines[i][0]
            x2, y2 = lines[i][1]
            image_draw.line([x1, y1, x2, y2], width=1, fill=DEFAULT_COLOR)

    @staticmethod
    def get_cube():
        p1 = np.array([0, 0, 0])
        p2 = np.array([1, 0, 0])
        p3 = np.array([0, 1, 0])
        p4 = np.array([0, 0, 1])
        p5 = np.array([1, 1, 0])
        p6 = np.array([1, 0, 1])
        p7 = np.array([0, 1, 1])
        p8 = np.array([1, 1, 1])

        edge_points = [
            [p1, p2, p5, p3],
            [p1, p2, p6, p4],
            [p1, p3, p7, p4],
            [p8, p7, p4, p6],
            [p8, p7, p3, p5],
            [p8, p6, p2, p5]
        ]
        edges = [Edge(points) for points in edge_points]

        return Polyhedron(edges)

