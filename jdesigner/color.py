from pyqtgraph import LayoutWidget
from pyqtgraph import QtGui


class JChooseColor:

    def __init__(self):
        self._set_black_color()
        # self._color_label = None

    def _set_red_color(self):
        self._color = "red"
        self._color_rgb = (255, 0, 0)
        # self.update_color_label()
        self.setPen(color="r")

    def _set_blue_color(self):
        self._color = "blue"
        self._color_rgb = (0, 0, 255)
        #self.update_color_label()
        self.setPen(color="b")

    def _set_green_color(self):
        self._color = "green"
        self._color_rgb = (0, 255, 0)
        #self.update_color_label()
        self.setPen(color="g")

    def _set_white_color(self):
        self._color = "white"
        self._color_rgb = (255, 255, 255)
        #self.update_color_label()
        self.setPen(color="w")

    def _set_black_color(self):
        self._color = "black"
        self._color_rgb = (0, 0, 0)
        self.setPen(color=(0, 0, 0))

    #def update_color_label(self):
    #    self._color_label.setText("Current color: " + self._color)

    def get_color_dock_widget(self):

        layout = LayoutWidget()
        # self._color_label = QtGui.QLabel("Current color: " + self._color)
        # layout.addWidget(self._color_label, row=0, col=0, colspan=3)

        label2 = QtGui.QLabel("Color:")
        layout.addWidget(label2, row=0, col=0, colspan=3)

        button_red = QtGui.QPushButton("Red")
        button_red.setMinimumWidth(45)
        button_red.clicked.connect(self._set_red_color)
        layout.addWidget(button_red, row=1, col=0)

        button_green = QtGui.QPushButton("Green")
        button_green.setMinimumWidth(45)
        button_green.clicked.connect(self._set_green_color)
        layout.addWidget(button_green, row=1, col=1)

        button_blue = QtGui.QPushButton("Blue")
        button_blue.setMinimumWidth(45)
        button_blue.clicked.connect(self._set_blue_color)
        layout.addWidget(button_blue, row=1, col=2)

        button_white = QtGui.QPushButton("White")
        button_white.setMinimumWidth(45)
        button_white.clicked.connect(self._set_white_color)
        layout.addWidget(button_white, row=2, col=0)

        button_black = QtGui.QPushButton("Black")
        button_black.setMinimumWidth(45)
        button_black.clicked.connect(self._set_black_color)
        layout.addWidget(button_black, row=2, col=1)

        layout.layout.setContentsMargins(0, 0, 0, 5)

        return layout
