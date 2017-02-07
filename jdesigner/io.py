from pyqtgraph import QtGui

from .jpolyline import JpolyLine
from .jtext import JtextROI
from .jrectangle import Jrectangle
from .bezier_curve import BezierCurve


class ExportDialog:

    def __init__(self, window):
        self.dialog = QtGui.QDialog(window)
        layout = QtGui.QGridLayout(self.dialog)

        label_1 = QtGui.QLabel("File name:")
        layout.addWidget(label_1, 0, 0)

        line_edit_1 = QtGui.QLineEdit()
        layout.addWidget(line_edit_1, 0, 1)

        button_1 = QtGui.QPushButton("Load a file")
        layout.addWidget(button_1, 0, 2)

        label_2 = QtGui.QLabel("XKCD:")
        layout.addWidget(label_2, 1, 0)

        radio = QtGui.QRadioButton("")
        layout.addWidget(radio, 1, 1)

        label_3 = QtGui.QLabel("Width (in cm):")
        layout.addWidget(label_3, 2, 0)

        line_edit_2 = QtGui.QLineEdit()
        validator = QtGui.QDoubleValidator(1.0, 50.0, 2)
        line_edit_2.setValidator(validator)
        layout.addWidget(line_edit_2, 2, 1)

        label_4 = QtGui.QLabel("Height (in cm):")
        layout.addWidget(label_4, 3, 0)

        line_edit_3 = QtGui.QLineEdit()
        line_edit_3.setValidator(validator)
        layout.addWidget(line_edit_3, 3, 1)

        button_2 = QtGui.QPushButton("Export")
        layout.addWidget(button_2, 4, 2)

    def exec(self):
        self.dialog.exec()


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


def get_open_filename():
    file_name = QtGui.QFileDialog.getOpenFileName(None,
                                                  "Load File",
                                                  "",
                                                  "Files (*.jdes)")
    if file_name[-5:] != ".jdes":
        print("Wrong format, cannot open file %s", file_name)
        return None
        #TODO add label

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
