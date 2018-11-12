import numpy as np
from Affine3D import *


class Camera:
    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 600

    def __init__(self, position, view_direction, polyhedron, matrix):
        self.position = position
        self.direction = view_direction
        self.polyhedron = polyhedron.get_clone()
        self.matrix = matrix

    def switch_to_camera_view(self, image_draw):
        self.draw(image_draw)

    def to_2D(self, face):
        # specified projection matrix
        points = self.get_transformed_points(self.matrix, face.points)
        points = [x[:2] for x in points]
        lines = list(zip(points, [points[-1]]+points[0:-1]))
        return lines

    def get_draw_lines(self):
        res = []
        for face in self.polyhedron.edges:
            res += self.to_2D(face)
        return res

    def draw(self, image_draw):
        # translation
        center = self.polyhedron.center_point
        self.polyhedron.translate(self.DEFAULT_WIDTH/2 - self.position[0],
                                  self.DEFAULT_HEIGHT/2 - self.position[1],
                                  0)
        # rotation

        lines = self.get_draw_lines()
        for i in range(len(lines)):
            print(i)
            x1, y1 = lines[i][0]
            x2, y2 = lines[i][1]
            image_draw.line([x1, y1, x2, y2], width=1, fill='black')

    def get_transformed_points(self, matrix, points):
        new_points = []
        for point in points:
            new_points.append(point_transform(point, matrix))
        return new_points


