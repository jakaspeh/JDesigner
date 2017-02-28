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
    obj = None
    if "*JRectangle" in string:
        obj = Jrectangle.load(string, info_dock=viewbox.info_dock, viewbox=viewbox)
    if "*JBezierCurve" in string:
        obj = BezierCurve.load(string, info_dock=viewbox.info_dock, viewbox=viewbox)
    if "*JPolyline" in string:
        obj = JpolyLine.load(string, info_dock=viewbox.info_dock, viewbox=viewbox)
    if "*JText" in string:
        obj = JtextROI.load(string, info_dock=viewbox.info_dock, viewbox=viewbox)
    return obj
