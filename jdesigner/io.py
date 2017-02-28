from pyqtgraph import QtGui

from .jpolyline import JpolyLine
from .jtext import JtextROI
from .jrectangle import Jrectangle
from .bezier_curve import BezierCurve


def split_strings(file_name, split="*"):

    strings = []
    s = ""
    with open(file_name) as file:
        for line in file:

            if len(line) == 0:
                continue

            if line[0] == split:
                if s != "":
                    strings.append(s)
                    s = ""
            line = line.strip()
            s += line

    strings.append(s)

    return strings


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
    control_points = curve.get_control_points()
    degree = len(control_points) - 1

    s = ""
    s += "Bezier curve:\n"
    s += "Degree:\n" + str(degree) + "\n"
    s += "Control points:\n"

    for point in control_points:
        x, y = point
        s += str(x) + " " + str(y) + "\n"

    return s


def get_open_filename():
    file_name = QtGui.QFileDialog.getOpenFileName(None,
                                                  "Load File",
                                                  "",
                                                  "Files (*.jdes)")
    if file_name[-5:] != ".jdes":
        print("Wrong format, cannot open file %s" % file_name)
        return None

    return file_name

def construct_object(string, viewbox):
    object = None
    if "*JRectangle" in string:
        object = Jrectangle.load(string, info_dock=viewbox.info_dock,
                                 viewbox=viewbox)
    if "*JBezierCurve" in string:
        object = BezierCurve.load(string, info_dock=viewbox.info_dock,
                                  viewbox=viewbox)
    if "*JPolyline" in string:
        object = JpolyLine.load(string, info_dock=viewbox.info_dock,
                                viewbox=viewbox)
    if "*JText" in string:
        object = JtextROI.load(string, info_dock=viewbox.info_dock,
                               viewbox=viewbox)
    return object
