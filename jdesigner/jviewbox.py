from pyqtgraph import ViewBox
from pyqtgraph import QtCore
from pyqtgraph import QtGui

from .bezier_curve import BezierCurve
from .items import Items
from .jrectangle import Jrectangle
from .jpolyline import JpolyLine
from .jtext import Jtext
from .jtext import JtextROI
from .io import split_strings

class JviewBox(ViewBox):

    def __init__(self, label, info_dock, **kargs):
        ViewBox.__init__(self, **kargs)
        self.label = label
        self.items = Items()
        self.info_dock = info_dock

        self._creating_curve = False
        self._creating_polyline = False
        self._creating_square = False
        self._creating_text = False
        self._curve_control_points = []
        self._polyline_points = []
        self._square_points = []

        self.setBackgroundColor((255, 255, 255))
        self.border.setColor(QtGui.QColor(255, 0, 0))
        self._menu = self._build_menu()

    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self._raise_menu(ev)
        else:
            super().mouseClickEvent(ev)

    def removeItem(self, item):
        self.label.setText("Item removed.")
        if type(item) is Jtext:
            try:
                self.addedItems.remove(item)
            except:
                pass
        elif type(item) is JtextROI:
            super().removeItem(item.text)
            super().removeItem(item)
        else:
            super().removeItem(item)

    def mousePressEvent(self, event):

        if self._process_event():

            if self._creating_curve:
                self._creating_curve_press_event(event)

            if self._creating_polyline:
                self._creating_polyline_press_event(event)

            if self._creating_square:
                self._creating_square_press_event(event)

            if self._creating_text:
                self._creating_text_press_event(event)

        else:
            super().mousePressEvent(event)

    def add_curve(self):
        self._reset_private_variables()
        self._creating_curve = True

    def add_line(self):
        self._reset_private_variables()
        self._creating_polyline = True

    def add_square(self):
        self._reset_private_variables()
        self._creating_square = True

    def add_text(self):
        self._reset_private_variables()
        self._creating_text = True

    def _process_event(self):
        return self._creating_polyline or self._creating_square or \
               self._creating_curve or self._creating_text

    def _creating_square_press_event(self, event):
        p = self.mapSceneToView(event.scenePos())
        point = [p.x(), p.y()]
        self._square_points.append(point)

        if len(self._square_points) < 2:
            self.label.setText("Creating square. Click to create upper right point...")
        else:
            self.label.setText("New square created.")

            p0 = self._square_points[0]
            p1 = self._square_points[1]

            dx = abs(p1[0] - p0[0])
            dy = abs(p1[1] - p0[1])
            size = [dx, dy]

            rectangle = Jrectangle(p0, size, info_dock=self.info_dock, viewbox=self)
            self.addItem(rectangle)
            self.items.add_item(rectangle)

            self._reset_private_variables()

    def _creating_polyline_press_event(self, event):
        p = self.mapSceneToView(event.scenePos())
        point = [p.x(), p.y()]
        self._polyline_points.append(point)

        if event.button() == QtCore.Qt.LeftButton:
            self.label.setText("Creating polyline, left click to create points, right click to stop.")
        elif event.button() == QtCore.Qt.RightButton:
            self.label.setText("New polyline created.")
            polyline = JpolyLine(self._polyline_points, info_dock=self.info_dock, viewbox=self)
            self.addItem(polyline)
            self.items.add_item(polyline)

            self._reset_private_variables()

    def _creating_curve_press_event(self, event):
        p = self.mapSceneToView(event.scenePos())
        point = [p.x(), p.y()]
        self._curve_control_points.append(point)

        num_control_points = len(self._curve_control_points)
        if num_control_points < 4:
            diff = 4 - num_control_points
            self.label.setText("Create " + str(diff) + " more control points.")
        else:
            self.label.setText("New curve created")

            curve = BezierCurve(self._curve_control_points, info_dock=self.info_dock, viewbox=self)
            self.addItem(curve)
            self.items.add_item(curve)

            self._reset_private_variables()

    def _creating_text_press_event(self, event):
        p = self.mapSceneToView(event.scenePos())
        point = [p.x(), p.y()]

        self.label.setText("New text created")

        text = Jtext("Text")
        self.addItem(text)
        self.items.add_item(text)

        text_roi = JtextROI(point, self.viewRange(), text, info_dock=self.info_dock, viewbox=self)
        self.addItem(text_roi)
        self.items.add_item(text_roi)

        self._reset_private_variables()

    def _reset_private_variables(self):
        self._creating_curve = False
        self._curve_control_points = []

        self._creating_polyline = False
        self._polyline_points = []

        self._creating_square = False
        self._square_points = []

        self._creating_text = False

    def save_as(self):
        file_name = QtGui.QFileDialog.getSaveFileName(None,
                                                      "Save File",
                                                      "",
                                                      "Files (*.jdes)")
        if file_name[-5:] != ".jdes":
            file_name += ".jdes"

        # add label
        with open(file_name, "w") as file:
            for item in self.addedItems:
                if type(item) is Jtext:
                    continue
                else:
                    item.save(file)

    def load(self):
        file_name = QtGui.QFileDialog.getOpenFileName(None,
                                                      "Load File",
                                                      "",
                                                      "Files (*.jdes)")
        if file_name[-5:] != ".jdes":
            print("Wrong format, cannot open file %s", file_name)
            # add label

        strings = split_strings(file_name)
        print(strings)

        for s in strings:
            if "*JRectangle" in s:
                rectangle = Jrectangle.load(s, info_dock=self.info_dock,
                                            viewbox=self)
                self.addItem(rectangle)

    def _build_menu(self):
        menu = QtGui.QMenu()
        menu.setTitle("JviewBox")
        menu.addAction("Save As", self.save_as)
        return menu

    def _raise_menu(self, event):
        pos = event.screenPos()
        self._menu.popup(QtCore.QPoint(pos.x(), pos.y()))

