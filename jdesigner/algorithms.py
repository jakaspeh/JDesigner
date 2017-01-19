

def de_casteljau(control_points, t):

    cp = [p for p in control_points]
    n = len(cp)

    for j in range(1, n):
        for i in range(n - j):
            cp[i] = cp[i] * (1 - t) + cp[i + 1] * t

    return cp[0]


def degree_elevation(control_points):
    degree = len(control_points) - 1
    new_control_points = []
    for i in range(degree + 2):
        if i == 0:
            new_control_points.append(control_points[i])
        elif i == degree + 1:
            new_control_points.append(control_points[i - 1])
        else:
            fraction = i / (degree + 1)
            point = fraction * control_points[i - 1] + (1 - fraction) * control_points[i]
            new_control_points.append(point)
    return new_control_points
