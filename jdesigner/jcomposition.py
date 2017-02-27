from pyqtgraph import ROI
from pyqtgraph import QtGui
from pyqtgraph import QtCore
from pyqtgraph import LayoutWidget

from .utils import compute_bbox
from .utils import compute_weights
from .utils import compute_points
from .utils import delete_content

from .remove_item import JRemoveItem


class Jcomposition(ROI, JRemoveItem):

    def __init__(self, objects, info_dock=None, viewbox=None):

        pos = [0, 0]
        ROI.__init__(self, pos, size=[1, 1])

        self.objects = objects

        self.setPen(200, 200, 200)

        self.info_dock = info_dock
        self.viewbox = viewbox
        bbox = self.compute_bbox()

        self.handlePen.setColor(QtGui.QColor(0, 0, 0))
        for corner in bbox:
            self.addFreeHandle(corner)

        self.weights = None
        self.set_weights()

        JRemoveItem.__init__(self, viewbox)
        self._display_info_dock()

    def set_weights(self):
        bbox = self.get_bbox()
        self.weights = []
        for obj in self.objects:
            points = obj.get_drawing_points()
            weights_of_points = compute_weights(bbox, points)
            self.weights.append(weights_of_points)

    def compute_bbox(self):
        return compute_bbox(self.objects)

    def get_bbox(self):
        handle0 = self.handles[0]["pos"]
        handle1 = self.handles[1]["pos"]
        return [[handle0.x(), handle0.y()], [handle1.x(), handle1.y()]]

    def shape(self):
        bbox = self.get_bbox()
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

        bbox = self.get_bbox()
        for obj, w in zip(self.objects, self.weights):
            p.setPen(obj.currentPen)
            pts = compute_points(bbox, w)
            points = [QtCore.QPointF(pt[0], pt[1]) for pt in pts]
            for i in range(len(points) - 1):
                p.drawLine(points[i], points[i + 1])

    def _display_info_dock(self):

        if self.info_dock is None:
            return

        delete_content(self.info_dock)

        container = LayoutWidget()
        label = QtGui.QLabel("Composition")
        container.addWidget(label, row=0, col=0)

        remove_item_widget = self.get_remove_item_dock_widget()
        container.addWidget(remove_item_widget, row=1, col=0)

        vertical_spacer = QtGui.QSpacerItem(1, 1, QtGui.QSizePolicy.Minimum,
                                            QtGui.QSizePolicy.Expanding)
        container.layout.addItem(vertical_spacer, 2, 0)
        self.info_dock.addWidget(container)
