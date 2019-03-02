import numpy as np
import copy
from enum import Enum

class Projection(Enum):
    ORTHO_XOY = 1
    ORTHO_XOZ = 2
    ORTHO_YOZ = 3

    ISOMETRIC = 4
    DIMETRIC = 5

    PERSPECTIVE_1 = 6
    PERSPECTIVE_2 = 7
    PERSPECTIVE_3 = 8


def point_transfrom(point, matrix):
    point = np.append(point, [1])
    row_transforamtion = np.dot(point, matrix)
    homogenious_coords = row_transforamtion / row_transforamtion[3]
    return homogenious_coords[:3]

def make_clone(figure):
    points_copy = copy.deepcopy(figure.point_list)
    return Figure(points_copy, figure.edges)

def get_x_rot_matrix(angle):
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    rotation_matrix = np.array([
        [1,     0,      0, 0],
        [0, cos_a,  sin_a, 0],
        [0, -sin_a, cos_a, 0],
        [0,      0,     0, 1]
    ])
    return rotation_matrix

def get_y_rot_matrix(angle):
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    rotation_matrix = np.array([
        [cos_a, 0, -sin_a, 0],
        [0,     1,      0, 0],
        [sin_a, 0,  cos_a, 0],
        [0,     0,      0, 1]
    ])
    return rotation_matrix

def get_z_rot_matrix(angle):
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    rotation_matrix = np.array([
        [cos_a,  sin_a, 0, 0],
        [-sin_a, cos_a, 0, 0],
        [0,          0, 1, 0],
        [0,          0, 0, 1]
    ])
    return rotation_matrix


class Figure:
    def __init__(self, point_list, edges=None):
        self.point_list = np.array(point_list)
        self.center_point = None
        self.calc_center()
        self.edges = edges

    def calc_center(self):
        mid_x = (max(self.point_list[:, 0]) + min(self.point_list[:, 0])) / 2
        mid_y = (max(self.point_list[:, 1]) + min(self.point_list[:, 1])) / 2
        mid_z = (max(self.point_list[:, 2]) + min(self.point_list[:, 2])) / 2
        self.center_point = np.array([mid_x, mid_y, mid_z])

    def take_xy_coords(self):
        self.point_list = [np.take(x, [0, 1]) for x in self.point_list]
        return self

    def take_xz_coords(self):
        self.point_list = [np.take(x, [0, 2]) for x in self.point_list]
        return self

    def take_yz_coords(self):
        self.point_list = [np.take(x, [1, 2]) for x in self.point_list]
        return self

    def transform(self, matrix):
        self.point_list = [point_transfrom(p, matrix) for p in self.point_list]

    def scale(self, kx, ky, kz):
        scale_matrix = np.array([
            [kx, 0, 0, 0],
            [0, ky, 0, 0],
            [0, 0, kz, 0],
            [0, 0, 0,  1]
        ])
        self.transform(scale_matrix)

    def shift(self, dx, dy, dz):
        shift_matrix = np.array([
            [1,  0,  0,  0],
            [0,  1,  0,  0],
            [0,  0,  1,  0],
            [dx, dy, dz, 1]
        ])
        self.transform(shift_matrix)

    def rotate_x_axis(self, angle):
        rotation_matrix = get_x_rot_matrix(angle)
        self.transform(rotation_matrix)

    def rotate_y_axis(self, angle):
        rotation_matrix = get_y_rot_matrix(angle)
        self.transform(rotation_matrix)

    def rotate_z_axis(self, angle):
        rotation_matrix = get_z_rot_matrix(angle)
        self.transform(rotation_matrix)

    def get_projection(self, matrix):
        clone = make_clone(self)
        clone.transform(matrix)
        return clone

    def orthographic_XOY(self):
        ortho_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1]
        ])
        return self.get_projection(ortho_matrix)

    def orthographic_XOZ(self):
        ortho_matrix = np.array([
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        return self.get_projection(ortho_matrix)

    def orthographic_YOZ(self):
        ortho_matrix = np.array([
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        return self.get_projection(ortho_matrix)

    def isometric(self):
        isometric_mat = np.dot(get_x_rot_matrix(np.pi*2/3),
                               get_y_rot_matrix(np.pi*2/3))
        return self.get_projection(isometric_mat)

    def dimetric(self):
        dimetric_mat = np.dot(get_x_rot_matrix(np.pi * 2 / 3),
                               get_y_rot_matrix(np.pi * 2 / 3))
        return self.get_projection(dimetric_mat)

    def perspective_one_point(self, d=100):
        perspective_mat = np.array([
            [0, 0, 0,    0],
            [0, 1, 0,    0],
            [0, 0, 1, 1/d],
            [0, 0, 0,    0]
        ])
        return self.get_projection(perspective_mat)

    def perspective_two_point(self, dy=100, dz=100):
        perspective_mat = np.array([
            [0, 0, 0,     0],
            [0, 1, 0, 1/dy],
            [0, 0, 1, 1/dz],
            [0, 0, 0,     0]
        ])
        return self.get_projection(perspective_mat)

    def perspective_three_point(self, dx=100, dy=100, dz=100):
        perspective_mat = np.array([
            [0, 0, 0, 1/dx],
            [0, 1, 0, 1/dy],
            [0, 0, 1, 1/dz],
            [0, 0, 0,     0]
        ])
        return self.get_projection(perspective_mat)


class Cube(Figure):
    def __init__(self):
        point_list = [
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
            [1, 0, 0],
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0],
            [1, 1, 1]
        ]
        edges = [
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 4),
            (1, 5),
            (2, 4),
            (2, 6),
            (3, 5),
            (3, 6),
            (7, 4),
            (7, 5),
            (7, 6)
        ]
        Figure.__init__(self, point_list, edges)


class Chair(Figure):
    def __init__(self):
        seat = []
        leg_1 = []
        leg_2 = []
        leg_3 = []
        leg_4 = []

        backrest_leg_left = []
        backrest_leg_right = []
        backrest = []

        hole = []

        point_list = seat + leg_1 + leg_2 + leg_3 + leg_4 \
                     + backrest_leg_left + backrest_leg_right + backrest + hole

        edges = []
        Figure.__init__(self, point_list, edges)
