import numpy as np
import copy


def point_transfrom(point, matrix):
    point = np.append(point, [1])
    row_transformation = np.dot(point, matrix)
    if abs(row_transformation[3]) < 1e-10:
        x = 5
    homogenious_coords = row_transformation / row_transformation[3]

    return homogenious_coords[:3]


def make_clone(figure):
    points_copy = copy.deepcopy(figure.point_list)
    center_copy = copy.deepcopy(figure.center_point)
    return Figure(points_copy, figure.edges, center_copy, False)


def get_shift_matrix(dx, dy, dz):
    shift_matrix = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [dx, dy, dz, 1]
    ])
    return shift_matrix

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
    def __init__(self, point_list, center_point=None):
        self.point_list = np.array(point_list)
        self.center_point = center_point
        self.calc_center()

    def calc_center(self):
        if len(self.point_list) == 0:
            self.center_point = np.array([0, 0, 0])
            return
        mid_x = (max(self.point_list[:, 0]) + min(self.point_list[:, 0])) / 2
        mid_y = (max(self.point_list[:, 1]) + min(self.point_list[:, 1])) / 2
        mid_z = (max(self.point_list[:, 2]) + min(self.point_list[:, 2])) / 2
        self.center_point = np.array([mid_x, mid_y, mid_z])

    def take_xy_coords(self):
        self.point_list = [np.take(x, [0, 1]) for x in self.point_list]
        return self

    def transform(self, matrix):
        self.center_point = point_transfrom(self.center_point, matrix)
        self.point_list = [point_transfrom(p, matrix) for p in self.point_list]

    def scale(self, kx, ky, kz):
        scale_matrix = np.array([
            [kx, 0, 0, 0],
            [0, ky, 0, 0],
            [0, 0, kz, 0],
            [0, 0, 0,  1]
        ])
        self.transform(scale_matrix)

    def scale_center(self, kx, ky, kz):
        mid_x, mid_y, mid_z = self.center_point
        self.shift(-mid_x, -mid_y, -mid_z)
        self.scale(kx, ky, kz)
        self.shift(mid_x, mid_y, mid_z)

    def shift(self, dx, dy, dz):
        shift_matrix = get_shift_matrix(dx, dy, dz)
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

    def rotate_x_axis_center(self, angle):
        mid_x, mid_y, mid_z = self.center_point
        self.shift(-mid_x, -mid_y, -mid_z)
        rotation_matrix = get_x_rot_matrix(angle)
        self.transform(rotation_matrix)
        self.shift(mid_x, mid_y, mid_z)

    def rotate_y_axis_center(self, angle):
        mid_x, mid_y, mid_z = self.center_point
        self.shift(-mid_x, -mid_y, -mid_z)
        rotation_matrix = get_y_rot_matrix(angle)
        self.transform(rotation_matrix)
        self.shift(mid_x, mid_y, mid_z)

    def rotate_z_axis_center(self, angle):
        mid_x, mid_y, mid_z = self.center_point
        self.shift(-mid_x, -mid_y, -mid_z)
        rotation_matrix = get_z_rot_matrix(angle)
        self.transform(rotation_matrix)
        self.shift(mid_x, mid_y, mid_z)

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

    def __str__(self):
        return str(self.point_list)


