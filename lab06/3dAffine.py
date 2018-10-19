import numpy as np

'''
В программе должны присутствовать следующие классы: точка, прямая (ребро), многоугольник (грань), многогранник.

Программа должна содержать следующие возможности:

Отображение одного из правильных многогранников: тетраэдр, гексаэдр, октаэдр, икосаэдр*, додекаэдр*.
Применение аффинных преобразований: смещение, поворот, масштаб, с указанием параметров преобразования. 
Преобразования должны быть реализованы матрицами!
'''


class Edge:
    def __init__(self, points=[]):
        self.points = points

    def add_point(self, point):
        self.points.append(point)

    def point_count(self):
        return len(self.points)

    def transform(self, matrix):
        new_points = []
        for x, y, z in self.points:
            point_tensor = np.array([x, y, z, 1])
            new_point = np.dot(point_tensor, matrix)[:3]
            new_points.append(new_point)
        self.points = new_points

    def translate(self, tx, ty, tz):
        translation_matrix = np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
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
        self.transform(rotation_matrix)

    def rotate_y_axis(self, theta):
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        rotation_matrix = np.array([
            [cos_theta, 0, sin_theta, 0],
            [0, 1, 0, 0],
            [-sin_theta, 0, cos_theta, 0],
            [0, 0, 0, 1]
        ])
        self.transform(rotation_matrix)

    def rotate_z_axis(self, theta):
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        rotation_matrix = np.array([
            [cos_theta, -sin_theta, 0, 0],
            [sin_theta, cos_theta, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.transform(rotation_matrix)

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


