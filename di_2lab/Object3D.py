import numpy as np
import copy

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
    def __init__(self, point_list):
        self.point_list = point_list

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

    def perspective_one_point(self, d):
        perspective_mat = np.array([
            [0, 0, 0,    0],
            [0, 1, 0,    0],
            [0, 0, 1, -1/d],
            [0, 0, 0,    0]
        ])
        return self.get_projection(perspective_mat)

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
        Figure.__init__(self, point_list)
