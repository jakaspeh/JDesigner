from pyqtgraph import RectROI

from pyqtgraph import QtCore
from pyqtgraph import QtGui
from pyqtgraph import LayoutWidget

from .utils import delete_content

from .color import JChooseColor
from .color import setup_color

from .remove_item import JRemoveItem


class Jrectangle(RectROI, JChooseColor, JRemoveItem):

    def __init__(self, pos, size, info_dock=None, viewbox=None):
        RectROI.__init__(self, pos, size)

        JChooseColor.__init__(self)
        JRemoveItem.__init__(self, viewbox)

        self.info_dock = info_dock

        self._menu = self._build_menu()
        self._display_info_dock()

        for h in self.handles:
            handle = h["item"]
            handle.currentPen.setColor(QtGui.QColor(0, 0, 0))

    @classmethod
    def load(cls, s, info_dock=None, viewbox=None):
        if "*JRectangle" not in s:
            print("Error reading a rectangle from a string %s" % s)

        s = s.replace("*JRectangle", "")

        if s[0] != "{" or s[-1] != "}":
            print("Error the string is in the wrong format")

        data = eval(s)
        rectangle = cls(data["pos"], data["size"], info_dock=info_dock,
                        viewbox=viewbox)
        setup_color(rectangle, data["color"])
        return rectangle

    def save(self, file):

        data = {}
        data["color"] = self._color
        data["pos"] = [self.pos().x(), self.pos().y()]
        data["size"] = [self.size().x(), self.size().y()]

        file.write("*JRectangle\n")
        file.write(str(data) + "\n")

    def _build_menu(self):
        menu = QtGui.QMenu()
        menu.setTitle("Rectangle")
        menu.addAction("Remove", self.remove_item)
        return menu

    def mouseClickEvent(self, ev):
        self._display_info_dock()
        if ev.button() == QtCore.Qt.RightButton:
            self._raise_menu(ev)

    def paint(self, p, *args):

        p.setRenderHint(QtGui.QPainter.Antialiasing)
        self.currentPen.setWidth(2)
        p.setPen(self.currentPen)
        super().paint(p, *args)

    def _raise_menu(self, event):
        pos = event.screenPos()
        self._menu.popup(QtCore.QPoint(pos.x(), pos.y()))

    def _display_info_dock(self):
        if self.info_dock is None:
            return

        delete_content(self.info_dock)

        container = LayoutWidget()
        label1 = QtGui.QLabel("Rectangle")
        container.addWidget(label1, row=0, col=0)

        color_dock_widget = self.get_color_dock_widget()
        container.addWidget(color_dock_widget, row=1, col=0)

        remove_item_widget = self.get_remove_item_dock_widget()
        container.addWidget(remove_item_widget, row=2, col=0)

        vertical_spacer = QtGui.QSpacerItem(1, 1, QtGui.QSizePolicy.Minimum,
                                            QtGui.QSizePolicy.Expanding)
        container.layout.addItem(vertical_spacer, 3, 0)

        self.info_dock.addWidget(container)
