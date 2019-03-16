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
    row_transformation = np.dot(point, matrix)
    if abs(row_transformation[3]) < 1e-10:
        x = 5
    homogenious_coords = row_transformation / row_transformation[3]

    return homogenious_coords[:3]

def make_clone(figure):
    points_copy = copy.deepcopy(figure.point_list)
    return Figure(points_copy, figure.edges)

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
    def __init__(self, point_list, edges=None):
        self.point_list = np.array(point_list)
        self.center_point = None
        self.calc_center()
        self.edges = edges

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

    def take_xz_coords(self):
        self.point_list = [np.take(x, [0, 2]) for x in self.point_list]
        return self

    def take_yz_coords(self):
        self.point_list = [np.take(x, [1, 2]) for x in self.point_list]
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
        isometric_mat = np.dot(get_y_rot_matrix(np.pi*45/180),
                               get_x_rot_matrix(np.pi*35.264/180))
        dx, dy, dz = self.center_point
        matrix = np.dot(np.dot(get_shift_matrix(-dx, -dy, -dz), isometric_mat), get_shift_matrix(dx, dy, dz))
        projection = self.get_projection(matrix)
        return projection

    def dimetric(self):
        dimetric_mat = np.dot(get_y_rot_matrix(np.pi*45/180),
                              get_x_rot_matrix(np.pi*26.565/180))
        dx, dy, dz = self.center_point
        matrix = np.dot(np.dot(get_shift_matrix(-dx, -dy, -dz), dimetric_mat), get_shift_matrix(dx, dy, dz))
        projection = self.get_projection(matrix)
        return projection

    def perspective_one_point(self, d=200):
        perspective_mat = np.array([
            [1, 0, 0,   0],
            [0, 1, 0,   0],
            [0, 0, 1, 1/d],
            [0, 0, 0,   1]
        ])
        return self.get_projection(perspective_mat)

    def perspective_two_point(self, dy=200, dz=200):
        perspective_mat = np.array([
            [1, 0, 0,     0],
            [0, 1, 0, 1/dy],
            [0, 0, 1, 1/dz],
            [0, 0, 0,     0]
        ])
        return self.get_projection(perspective_mat)

    def perspective_three_point(self, dx=200, dy=200, dz=200):
        perspective_mat = np.array([
            [1, 0, 0, 1/dx],
            [0, 1, 0, 1/dy],
            [0, 0, 1, 1/dz],
            [0, 0, 0,     0]
        ])
        return self.get_projection(perspective_mat)

    def __str__(self):
        return str(self.point_list)


class Cylinder(Figure):
    """
    создаёт цилиндр с единичной длиной и единичным радиусом. направлен по оси OZ
    """
    def __init__(self, segments_count):
        angle_step = (np.pi/180) * 360 / segments_count
        first_point = np.array([1, 0, 0])
        first_behind_point = np.array([1, 0, 1])

        points = [first_point, first_behind_point]
        edges = [(0, 1), (0, 2), (1, 3)]
        current_angle = 0
        index = 0
        all_cnt_points = 2*segments_count
        for _ in range(segments_count):
            current_angle += angle_step
            index += 2
            new_point = np.array([np.cos(current_angle), np.sin(current_angle), 0])
            behind_point = new_point + np.array([0, 0, 1])
            points.append(new_point)
            points.append(behind_point)

            edges += [(index, index+1), (index, (index+2) % all_cnt_points),
                      (index+1, (index+3) % all_cnt_points)]

        Figure.__init__(self, points, edges)


class LinedSurface(Figure):
    def __init__(self, f_points, g_points):
        if len(f_points) != len(g_points):
            raise Exception("Expected 2 lists with the same length")
        point_list = [(x, y, 0) for x, y in f_points] + [(x, y, 1) for x, y in g_points]
        cnt_points = len(f_points)
        edges = ([(i, i+1) for i in range(cnt_points-1)]        # связи между точками первой кривой
                + [(i+cnt_points, i+cnt_points+1) for i in range(cnt_points-1)] # связи между точками второй кривой
                + [(i, i+cnt_points) for i in range(cnt_points)]) # связи между точками первой и второй кривой
        Figure.__init__(self, point_list, edges)
