import math
import time
from enum import Enum


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    ON_LINE = 3

EPS = 1e-15

def module(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

def cosin(p1, p2):
    v1 = 0, -1
    v2 = p2[0] - p1[0], p2[1] - p1[1]
    scalar = v1[0]*v2[0] + v1[1] * v2[1]
    return scalar / (module(v1) * module(v2))


def get_first_edge(points):
    points.sort()
    first_point = points[0]
    points = points[1:]
    cosines = [cosin(first_point, p) for p in points]
    pairs = zip(cosines, points)
    second_point = min(pairs)[1]
    # if second_point[1]
    return first_point, second_point


def point_arrangement(line, point):
    p1, p2 = line
    line_vector = p2[0] - p1[0], p2[1] - p1[1]
    point_vector = point[0] - p1[0], point[1] - p1[1]
    expression = point_vector[1] * line_vector[0] - point_vector[0] * line_vector[1]
    if abs(expression) < EPS:
        return Direction.ON_LINE
    if expression > 0:
        return Direction.LEFT
    if expression < 0:
        return Direction.RIGHT


def det(a, b, c, d):
    return a*d - c*b


def calc_intersection(line1, line2):
    a1, b1, c1 = line1
    a2, b2, c2 = line2
    det_denom = det(a1, b1, a2, b2)
    x = -det(c1, b1, c2, b2) / det_denom
    y = -det(a1, c1, a2, c2) / det_denom
    return x, y


def to_equation(p1, p2):
    a = p2[1] - p1[1]
    b = p1[0] - p2[0]
    c = -(a*p1[0] + b*p1[1])
    return a, b, c


def get_perpendicular(a, b, c, p):
    a_per = b
    b_per = -a
    c_per = -(a_per*p[0] + b_per*p[1])
    return a_per, b_per, c_per


def get_mid(p1, p2):
    return (p1[0] + p2[0])/2, (p1[1] + p2[1])/2


def calc_radius(p1, p2, p3):
    a, b, c = to_equation(p1, p2)
    mid_point = get_mid(p1, p2)
    perpendicular1 = get_perpendicular(a, b, c, mid_point)
    a, b, c = to_equation(p2, p3)
    mid_point = get_mid(p2, p3)
    perpendicular2 = get_perpendicular(a, b, c, mid_point)
    common_point = calc_intersection(perpendicular1, perpendicular2)
    radius = math.sqrt((common_point[0]-p1[0])**2 + (common_point[1] - p1[1])**2)
    return radius if point_arrangement((p1, p2), common_point) == Direction.RIGHT else -radius


def delone(points):
    triangles = []
    live_edges = set()

    first_edge = get_first_edge(points)
    points = set(points)
    # used_points.add(first_edge[0])
    # used_points.add(first_edge[1])
    points.remove(first_edge[0])
    points.remove(first_edge[1])
    edges = [first_edge]
    live_edges.add(first_edge)

    while len(live_edges) > 0:
        edge = live_edges.pop()
        p1, p2 = edge
        min_radius = 1e+10
        new_point = (-1, -1)
        for p in points:
            if point_arrangement(edge, p) != Direction.RIGHT:
                # print("point {} outside line {}".format(p, edge))
                continue
            radius = calc_radius(p1, p2, p)
            if radius < min_radius:
                min_radius = radius
                new_point = p

        edges.append(edge)
        if new_point == (-1, -1):
            continue
        edge1 = p1, new_point
        edge2 = new_point, p2

        for edge in (edge1, edge2):
            if edge in live_edges in live_edges:
                edges.append(edge)
                live_edges.remove(edge)
            elif (edge[1], edge[0]) in live_edges:
                edges.append((edge[1], edge[0]))
                live_edges.remove((edge[1], edge[0]))
            else:
                live_edges.add(edge)

    print("size of edges: {}".format(len(edges)))
    return edges

