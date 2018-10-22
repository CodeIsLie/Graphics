import math

EPS = 1e-15

def module(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

def cosin(p1, p2):
    v1 = 1, 0
    v2 = p2[0] - p1[0], p2[1] - p1[1]
    scalar = v1[0]*v2[0] + v1[1] * v2[1]
    return scalar / (module(v1) * module(v2))

def get_first_edge(points):
    points.sort()
    first_point = points[0]
    points = points[1:]
    products = [cosin(first_point, p) for p in points]
    pairs = zip(products, points)
    second_point = min(pairs)[1]
    return first_point, second_point


def points_arrangement(a, b):
    LEFT = 1
    RIGHT = 2
    ON_LINE = 3
    expression = b[1] * a[0] - b[0] * a[1]
    if abs(expression) < EPS:
        return ON_LINE
    if expression < 0:
        return LEFT
    if expression > 0:
        return RIGHT



def delone(points):
    triangles = []
    start_edge = []
    sleep_edges = []
    dead_edges = []
    live_edges = []

    edges = [get_first_edge(points)]
    return edges

