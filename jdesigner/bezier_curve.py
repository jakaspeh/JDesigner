import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph import LayoutWidget

from .algorithms import de_casteljau
from .algorithms import degree_elevation

from .utils import construct_arrow
from .utils import delete_content

from .color import JChooseColor

from .arrow import JArrowDock

from .remove_item import JRemoveItem


class BezierCurve(pg.ROI, JChooseColor, JArrowDock, JRemoveItem):
    def __init__(self, positions, resolution=100, info_dock=None, viewbox=None):

        pos = [0, 0]
        pg.ROI.__init__(self, pos, size=[1, 1])
        self.handlePen.setColor(QtGui.QColor(0, 0, 0))

        for p in positions:
            self.addFreeHandle(p)

        self.setPen(200, 200, 220)
        self.resolution = resolution
        self.info_dock = info_dock
        self.menu = self.buildMenu()

        JChooseColor.__init__(self)
        JArrowDock.__init__(self)
        JRemoveItem.__init__(self, viewbox)
        self._display_info_dock()

    def save(self, file):
        print("Saving bezier curve")

    def getControlPoints(self):

        controlPoints = []
        for p in self.handles:
            vector = np.array([p["pos"].x(), p["pos"].y()])
            controlPoints.append(vector)

        return controlPoints

    def shape(self):
        p = QtGui.QPainterPath()
        controlPoints = self.getControlPoints()

        if len(controlPoints) == 0:
            return p

        start = controlPoints[0]

        p.moveTo(start[0], start[1])
        for point in controlPoints[1:]:
            p.lineTo(point[0], point[1])

        p.lineTo(start[0], start[1])
        return p

    def boundingRect(self):
        return self.shape().boundingRect()

    def _get_drawing_points(self):
        if not self._arrow:
            cps = self.getControlPoints()
            parameters = np.linspace(0.0, 1.0, self.resolution)
            return [de_casteljau(cps, t) for t in parameters]
        else:
            cps = self.getControlPoints()
            parameters = np.linspace(0.0, self._arrow_start, self.resolution)
            curve = [de_casteljau(cps, t) for t in parameters]
            last_2 = curve[-1]
            last = cps[-1]
            arrow_points = construct_arrow(last_2, last, self._arrow_width)
            curve.extend(arrow_points[1:])
            return curve

    def paint(self, p, *args):

        pts = self._get_drawing_points()
        points = [QtCore.QPointF(pt[0], pt[1]) for pt in pts]

        p.setRenderHint(QtGui.QPainter.Antialiasing)
        self.currentPen.setWidth(2)
        p.setPen(self.currentPen)
        for i in range(len(points) - 1):
            p.drawLine(points[i], points[i + 1])

    def mouseClickEvent(self, ev):
        self._display_info_dock()
        if ev.button() == QtCore.Qt.RightButton:
            self.raiseMenu(ev)

    def buildMenu(self):
        menu = QtGui.QMenu()
        menu.setTitle("Bezier Curve")
        menu.addAction("Elevate Degree", self.elevateDegree)
        menu.addAction("Remove", self.remove_item)
        return menu

    def elevateDegree(self):
        control_points = self.getControlPoints()
        new_control_points = degree_elevation(control_points)

        for handle in self.handles[:]:
            self.removeHandle(handle["item"])

        for point in new_control_points:
            p = [point[0], point[1]]
            self.addFreeHandle(p)

    def _toggle_arrow(self):
        self._arrow = not self._arrow
        self.update()

    def raiseMenu(self, event):
        pos = event.screenPos()
        self.menu.popup(QtCore.QPoint(pos.x(), pos.y()))

    def clear_points(self):

        while 0 < len(self.handles):
            self.removeHandle(self.handles[0]["item"])

    def _changed_resolution(self):
        try:
            self.resolution = float(self._resolution_edit.text())
        except ValueError:
            pass
        self.update()

    def get_resolution_dock(self):

        layout = LayoutWidget()

        label = QtGui.QLabel("Resolution")
        layout.addWidget(label, row=0, col=0)

        line_edit = QtGui.QLineEdit(str(self.resolution))
        validator = QtGui.QIntValidator(20, 1000)
        line_edit.setValidator(validator)
        line_edit.textChanged.connect(self._changed_resolution)
        layout.addWidget(line_edit, row=0, col=1)
        self._resolution_edit = line_edit

        layout.layout.setContentsMargins(0, 0, 0, 5)

        return layout

    def get_degree_elevate_dock(self):

        layout = LayoutWidget()
        button = QtGui.QPushButton("Elevate Degree")
        button.clicked.connect(self.elevateDegree)
        layout.addWidget(button, row=0, col=0)

        layout.layout.setContentsMargins(0, 0, 0, 0)

        return layout

    def _display_info_dock(self):
        if self.info_dock is None:
            return

        delete_content(self.info_dock)

        container = LayoutWidget()
        label = QtGui.QLabel("Curve")
        container.addWidget(label, row=0, col=0)

        degree_dock_widget = self.get_degree_elevate_dock()
        container.addWidget(degree_dock_widget, row=1, col=0)

        resolution_dock_widget = self.get_resolution_dock()
        container.addWidget(resolution_dock_widget, row=2, col=0)

        arrow_dock_widget = self.get_arrow_dock_widget()
        container.addWidget(arrow_dock_widget, row=3, col=0)

        color_dock_widget = self.get_color_dock_widget()
        container.addWidget(color_dock_widget, row=4, col=0)

        remove_item_widget = self.get_remove_item_dock_widget()
        container.addWidget(remove_item_widget, row=5, col=0)

        vertical_spacer = QtGui.QSpacerItem(1, 1, QtGui.QSizePolicy.Minimum,
                                            QtGui.QSizePolicy.Expanding)
        container.layout.addItem(vertical_spacer, 6, 0)

        self.info_dock.addWidget(container)



