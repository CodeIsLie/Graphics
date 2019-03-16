import numpy as np

EPS = 1e-10

def find_square_roots(a, b, c):
    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return None
    return (-b + np.sqrt(discriminant))/(2*a), (-b - np.sqrt(discriminant))/(2*a)


def find_point_intersections(line_1, line_2, cnt_lines, cylinder_rad):
    point_a, point_b = line_1
    point_c, point_d = line_2

    intersection_points = []

    vec_ab = point_b - point_a
    vec_cd = point_d - point_c
    for i in range(cnt_lines+1):
        x_n, y_n, z_n = point_a + vec_ab * (i / cnt_lines)
        x_m, y_m, z_m = point_c + vec_cd * (i / cnt_lines)

        ro = (x_m - x_n)/(z_m - z_n)
        delta = (y_m - y_n)/(z_m - z_n)

        a = ro**2 + delta**2
        b = 2 * (ro*x_n + delta*y_n - z_n*(ro**2 + delta**2))
        c = (x_n - ro*z_n)**2 + (y_n - delta*z_n)**2 - cylinder_rad**2

        if abs(a) < EPS:
            return None

        roots = find_square_roots(a, b, c)
        if roots is None:
            continue
        z1, z2 = roots
        new_points = [np.array([x_n+ro*(z-z_n),
                                y_n+delta*(z-z_n), z]) for z in (z1, z2)]
        intersection_points += new_points

    return intersection_points
