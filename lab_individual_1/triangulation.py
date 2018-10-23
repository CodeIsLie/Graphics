import math
from enum import Enum
class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    ON_LINE = 3

EPS = 1e-15

def module(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

def cosin(p1, p2):
    v1 = -p1[0], -p1[1]
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
    expression = point[1] * line_vector[0] - point[0] * line_vector[1]
    if abs(expression) < EPS:
        return Direction.ON_LINE
    if expression > 0:
        return Direction.LEFT
    if expression < 0:
        return Direction.RIGHT


def delone(points):
    triangles = []
    sleep_edges = []
    dead_edges = []
    live_edges = set()

    first_edge = get_first_edge(points)
    points = set(points)
    # used_points.add(first_edge[0])
    # used_points.add(first_edge[1])
    points.remove(first_edge[0])
    points.remove(first_edge[1])
    edges = [first_edge]
    live_edges.add(first_edge)

    edge = first_edge
    p1, p2 = edge
    min_radius = 1e+10
    new_point = (-1, -1)
    for p in points:
        if point_arrangement(edge, p) != Direction.RIGHT:
            print("point {} outside line {}".format(p, edge))
            continue
        radius = 5
        if radius < min_radius:
            min_radius = radius
            new_point = p
    edge1 = p1, new_point
    edge2 = p2, new_point

    for edge in (edge1, edge2):
        if edge in live_edges:
            edges.append(edge)
            live_edges.remove(edge)
        else:
            live_edges.add(edge)

    # edges.extend(live_edges)

    return edges

