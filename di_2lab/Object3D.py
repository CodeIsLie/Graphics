import numpy as np
import copy
from enum import Enum

class Projection(Enum):
    ORTHO_X = 1
    ORTHO_Y = 2
    ORTHO_Z = 3

    ISOMETRIC = 4
    DIMETRIC = 5

    PERSPECTIVE_1 = 6
    PERSPECTIVE_2 = 7
    PERSPECTIVE_3 = 8


def point_transfrom(point, matrix):
    point = np.append(point, [1])
    return np.dot(point, matrix)[:3]

def make_clone(figure):
    points_copy = copy.deepcopy(figure.point_list)
    return Figure(points_copy)

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
    def __init__(self, point_list, edges = None):
        self.point_list = point_list
        self.edges = []

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
            [0, 0, 1, -1/d],
            [0, 0, 0,    0]
        ])
        return self.get_projection(perspective_mat)

    # TODO: fix matrix
    def perspective_two_point(self, d=100):
        perspective_mat = np.array([
            [0, 0, 0,    0],
            [0, 1, 0,    0],
            [0, 0, 1, -1/d],
            [0, 0, 0,    0]
        ])
        return self.get_projection(perspective_mat)

    # TODO: fix matrix
    def perspective_three_point(self, d=100):
        perspective_mat = np.array([
            [0, 0, 0,    0],
            [0, 1, 0,    0],
            [0, 0, 1, -1/d],
            [0, 0, 0,    0]
        ])
        return self.get_projection(perspective_mat)

    def project(self, projection_type):
        # TODO: fix ortho names
        if projection_type == Projection.ORTHO_X:
            return self.orthographic_XOY()
        elif projection_type == Projection.ORTHO_Y:
            return self.orthographic_XOZ()
        elif projection_type == Projection.ORTHO_Z:
            return self.orthographic_YOZ()
        elif projection_type == Projection.ISOMETRIC:
            return self.isometric()
        elif projection_type == Projection.DIMETRIC:
            return self.dimetric()
        elif projection_type == Projection.PERSPECTIVE_1:
            return self.perspective_one_point()
        elif projection_type == Projection.PERSPECTIVE_2:
            return self.perspective_two_point()
        elif projection_type == Projection.PERSPECTIVE_3:
            return self.perspective_three_point()

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
