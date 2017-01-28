from pyqtgraph import ROI
from pyqtgraph import QtGui
from pyqtgraph import QtCore

from .color import JChooseColor
from .utils import compute_bbox


class Jcomposition(ROI, JChooseColor):

    def __init__(self, objects, info_dock=None, viewbox=None):

        pos = [0, 0]
        ROI.__init__(self, pos, size=[1, 1])

        self.objects = objects

        self.setPen(200, 200, 200)

        self.info_dock = info_dock
        self.viewbox = viewbox
        bbox = self.compute_bbox()

        for corner in bbox:
            self.addFreeHandle(corner)

        JChooseColor.__init__(self)

    def compute_bbox(self):

        points = []
        for obj in self.objects:
            bbox = obj.compute_bbox()
            points.append([bbox[0][0], bbox[0][1]])
            points.append([bbox[1][0], bbox[1][1]])

        return compute_bbox(points)

    def shape(self):
        bbox = self.compute_bbox()
        x_1, y_1 = bbox[0]
        x_2, y_2 = bbox[1]

        p = QtGui.QPainterPath()
        p.moveTo(x_1, y_1)
        p.lineTo(x_1, y_2)
        p.lineTo(x_2, y_2)
        p.lineTo(x_2, y_1)
        p.lineTo(x_1, y_1)
        return p

    def boundingRect(self):
        return self.shape().boundingRect()

    def paint(self, p, *args):

        p.setRenderHint(QtGui.QPainter.Antialiasing)

        for obj in self.objects:
            p.setPen(obj.currentPen)
            pts = obj._get_drawing_points()
            points = [QtCore.QPointF(pt[0], pt[1]) for pt in pts]
            for i in range(len(points) - 1):
                p.drawLine(points[i], points[i + 1])


