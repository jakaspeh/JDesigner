from .bezier_curve import BezierCurve


def string_to_curve(s):
    lines = s.split("\n")

    if lines[0] != "Bezier curve:":
        raise ValueError("String does not represent a Bezier curve")

    degree = int(lines[2])

    control_points = []
    for i in range(degree + 1):
        line = lines[4 + i]
        words = line.split(" ")
        x = float(words[0])
        y = float(words[1])

        control_points.append([x, y])

    return BezierCurve(control_points)


def read_curves(file_name):
    curves = []
    with open(file_name) as stream:

        s = ""

        for line in stream:

            if line == "\n":
                if s != "":
                    curve = string_to_curve(s)
                    curves.append(curve)
                    s = ""
            else:
                s += line
    return curves


def curve_to_string(curve):
    control_points = curve.getControlPoints()
    degree = len(control_points) - 1

    s = ""
    s += "Bezier curve:\n"
    s += "Degree:\n" + str(degree) + "\n"
    s += "Control points:\n"

    for point in control_points:
        x, y = point
        s += str(x) + " " + str(y) + "\n"

    return s
