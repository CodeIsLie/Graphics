import math

import numpy as np
from AffineMatrices import *

'''
В программе должны присутствовать следующие классы: точка, прямая (ребро), многоугольник (грань), многогранник.
Программа должна содержать следующие возможности:
Отображение одного из правильных многогранников: тетраэдр, гексаэдр, октаэдр, икосаэдр*, додекаэдр*.
Применение аффинных преобразований: смещение, поворот, масштаб, с указанием параметров преобразования. 
Преобразования должны быть реализованы матрицами!
'''

DEFAULT_COLOR = 'black'


def point_transform(point, matrix):
    x, y, z = point
    point_tensor = np.array([x, y, z, 1])
    return np.dot(point_tensor, matrix)[:3]


class Polygon:
    def __init__(self, points=None):
        self.points = [] if points is None else points

    def add_point(self, point):
        self.points.append(point)

    def point_count(self):
        return len(self.points)

    def get_transformed_points(self, matrix):
        new_points = []
        for point in self.points:
            new_points.append(point_transform(point, matrix))
        return new_points

    def get_transformed_points1(self, matrix, points):
        new_points = []
        for point in points:
            new_points.append(point_transform(point, matrix))
        return new_points

    def transform(self, matrix):
        self.points = self.get_transformed_points(matrix)

    def translate(self, tx, ty, tz):
        translation_matrix = get_translation_mat(tx, ty, tz)
        self.transform(translation_matrix)

    def scale(self, mx, my, mz):
        scale_matrix = get_scale_mat(mx, my, mz)
        self.transform(scale_matrix)

    def rotate_about_vector(self, theta, l, m, n):
        rotation_matrix = get_rotation_mat(theta, l, m, n)
        self.transform(rotation_matrix.transpose())

    def rotate_x_axis(self, theta):
        rotation_matrix = get_x_rotation_mat(theta)
        self.transform(rotation_matrix)

    def get_x_rotation(self, theta, points):
        rotation_matrix = get_x_rotation_mat(theta)
        return self.get_transformed_points1(rotation_matrix, points)

    def rotate_y_axis(self, theta):
        rotation_matrix = get_y_rotation_mat(theta)
        self.transform(rotation_matrix)

    def get_y_rotation(self, theta, points):
        rotation_matrix = get_y_rotation_mat(theta)
        return self.get_transformed_points1(rotation_matrix, points)

    def rotate_z_axis(self, theta):
        rotation_matrix = get_z_rotation_mat(theta)
        self.transform(rotation_matrix)

    def get_z_rotation(self, theta, points):
        rotation_matrix = get_z_rotation_mat(theta)
        return self.get_transformed_points1(rotation_matrix, points)

    def mirror(self, xoy, yoz, zox):
        if xoy:
            xoy_matrix = np.array([
                [1, 0,  0, 0],
                [0, 1,  0, 0],
                [0, 0, -1, 0],
                [0, 0,  0, 1]
            ])
            self.transform(xoy_matrix)

        if yoz:
            yoz_matrix = np.array([
                [-1, 0,  0, 0],
                [ 0, 1,  0, 0],
                [ 0, 0,  1, 0],
                [ 0, 0,  0, 1]
            ])
            self.transform(yoz_matrix)

        if zox:
            zox_matrix = np.array([
                [1,  0,  0, 0],
                [0, -1,  0, 0],
                [0,  0,  1, 0],
                [0,  0,  0, 1]
            ])
            self.transform(zox_matrix)

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

    def to_2D_isometry(self, center):
        translation_matrix = get_translation_mat(*[-x for x in center])
        points = self.get_transformed_points1(translation_matrix, self.points)

        theta = 45 * np.pi / 180
        l = 0
        m = 1
        n = 0
        rotation_matrix = get_rotation_mat(theta, l, m, n)
        points = self.get_transformed_points1(rotation_matrix, points)

        theta = 35.264 * np.pi / 180
        l = 1
        m = 0
        n = 0
        rotation_matrix = get_rotation_mat(theta, l, m, n)
        points = self.get_transformed_points1(rotation_matrix, points)

        translation_matrix = get_translation_mat(*center)
        points = self.get_transformed_points1(translation_matrix, points)
        points = [x[:2] for x in points]
        lines = list(zip(points, [points[-1]] + points[0:-1]))
        return lines

    def __str__(self):
        s = ""
        for x, y, z in self.points:
            s += "({}, {}, {}) ".format(x, y, z)
        s += "\n"
        return s


# многогранник
class Polyhedron:
    def __init__(self, edges=None, center_point=None):
        self.edges = [] if edges is None else edges
        self.center_point = (0.5, 0.5, 0.5) if center_point is None else center_point

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_draw_lines(self):
        res = []
        for edge in self.edges:
            # res += edge.to_2D(90, 90, 300, 1000)
            res += edge.to_2D_isometry(self.center_point)
        return res

    def transform(self, matrix):
        pass

    def translate(self, dx, dy, dz):
        for edge in self.edges:
            edge.translate(dx, dy, dz)

        translation_matrix = get_translation_mat(dx, dy, dz)
        self.center_point = point_transform(self.center_point, translation_matrix)

    def center_scale(self, mx, my, mz):
        print(self.center_point)
        old_center = self.center_point
        self.scale(mx, my, mz)
        self.translate(
            -(self.center_point[0] - old_center[0]),
            -(self.center_point[1] - old_center[1]),
            -(self.center_point[2] - old_center[2]))
        print(self.center_point)

    def scale(self, mx, my, mz):
        for edge in self.edges:
            edge.scale(mx, my, mz)

        scale_matrix = get_scale_mat(mx, my, mz)
        self.center_point = point_transform(self.center_point, scale_matrix)

    def rotate_about_vector(self, theta, x, y, z, x1, y1, z1):
        print("rotating about vector: center = ", self.center_point)
        l = x1 - x
        m = y1 - y
        n = z1 - z
        length = math.sqrt(l**2 + m**2 + n**2)
        l = l/length
        m = m/length
        n = n/length

        self.translate(-x, -y, -z)

        theta *= np.pi / 180
        for edge in self.edges:
            edge.rotate_about_vector(theta, l, m, n)

        rotation_matrix = get_rotation_mat(theta, l, m, n)
        self.center_point = point_transform(self.center_point, rotation_matrix.transpose())

        self.translate(x, y, z)

        print("success: center = ", self.center_point)

    def rotate_all(self, angle_x, angle_y, angle_z):
        angle_x *= np.pi / 180
        angle_y *= np.pi / 180
        angle_z *= np.pi / 180
        for edge in self.edges:
            edge.rotate_x_axis(angle_x)
            edge.rotate_y_axis(angle_y)
            edge.rotate_z_axis(angle_z)

        rotation_matrix_x = get_x_rotation_mat(angle_x)
        self.center_point = point_transform(self.center_point, rotation_matrix_x)

        rotation_matrix_y = get_y_rotation_mat(angle_y)
        self.center_point = point_transform(self.center_point, rotation_matrix_y)

        rotation_matrix_z = get_z_rotation_mat(angle_z)
        self.center_point = point_transform(self.center_point, rotation_matrix_z)

    def draw(self, image_draw):
        lines = self.get_draw_lines()

        for i in range(len(lines)):
            x1, y1 = lines[i][0]
            x2, y2 = lines[i][1]
            image_draw.line([x1, y1, x2, y2], width=1, fill=DEFAULT_COLOR)

    def mirror(self, xoy, yoz, zox):
        for edge in self.edges:
            edge.mirror(xoy, yoz, zox)
        print("mirroring: center = ", self.center_point)
        if xoy:
            xoy_matrix = np.array([
                [1, 0,  0, 0],
                [0, 1,  0, 0],
                [0, 0, -1, 0],
                [0, 0,  0, 1]
            ])
            self.center_point = point_transform(self.center_point, xoy_matrix)

        if yoz:
            yoz_matrix = np.array([
                [-1, 0,  0, 0],
                [ 0, 1,  0, 0],
                [ 0, 0,  1, 0],
                [ 0, 0,  0, 1]
            ])
            self.center_point = point_transform(self.center_point, yoz_matrix)

        if zox:
            zox_matrix = np.array([
                [1,  0,  0, 0],
                [0, -1,  0, 0],
                [0,  0,  1, 0],
                [0,  0,  0, 1]
            ])
            self.center_point = point_transform(self.center_point, zox_matrix)
        print("success: center = ", self.center_point)

    @staticmethod
    def get_ikosaeder():
        p0 = np.array([0, 1, 0])
        p1 = np.array([.951, .5, -.309])
        p2 = np.array([.587, .5, .809])
        p3 = np.array([-.587, .5, .809])
        p4 = np.array([-.951, .5, -.309])
        p5 = np.array([0, .5, -1])
        p6 = np.array([.951, -.5, .309])
        p7 = np.array([0, -.5, 1])
        p8 = np.array([-.951, -.5 ,.309])
        p9 = np.array([-.587, -.5 ,-.809])
        p10 = np.array([.587 ,-.5 ,-.809])
        p11= np.array([0 ,-1 ,0])

        edge_points = [
            [p0, p2, p1],
            [p0, p3 , p2],
            [p0, p4 , p3],
            [p0, p5 , p4],
            [p0 , p1 , p5],
            [p1 , p2 , p6],
            [p2 , p7 , p6],
            [p2 , p3 , p7],
            [p3 , p8 , p7],
            [p3 , p4 , p8],
            [p4 , p9 , p8],
            [p4 , p5 , p9],
            [p5 , p10 , p9],
            [p5 , p1 , p10],
            [p1 , p6 , p10],
            [p7 , p11 , p6],
            [p7 , p8 , p11],
            [p9 , p11 , p8],
            [p9 , p10 , p11],
            [p10 , p6 , p11]
        ]
        edges = [Polygon(points) for points in edge_points]

        return Polyhedron(edges, (0,0,0))

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
        edges = [Polygon(points) for points in edge_points]

        return Polyhedron(edges)