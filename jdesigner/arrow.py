from pyqtgraph import QtGui
from pyqtgraph import LayoutWidget


class JArrowDock:

    def __init__(self):
        self._arrow = False
        self._arrow_start = 0.9
        self._arrow_width = 0.5

    def get_arrow_dock_widget(self):
        layout = LayoutWidget()
        label1 = QtGui.QLabel("Arrow:")
        layout.addWidget(label1, row=0, col=0, colspan=2)

        label4 = QtGui.QLabel("On/Off:")
        layout.addWidget(label4, row=1, col=0)
        chBox4 = QtGui.QCheckBox()
        layout.addWidget(chBox4, row=1, col=1)
        chBox4.setChecked(self._arrow)
        chBox4.toggled.connect(self._dock_toggle_arrow)
        self._arrow_check_box = chBox4

        label2 = QtGui.QLabel("Start:")
        layout.addWidget(label2, row=2, col=0)
        self._arrow_label2 = label2
        edit2 = QtGui.QLineEdit(str(self._arrow_start))
        validator2 = QtGui.QDoubleValidator(0.01, 0.99, 2)
        edit2.setValidator(validator2)
        edit2.textChanged.connect(self._changed_arrow)
        layout.addWidget(edit2, row=2, col=1)
        self._arrow_start_edit = edit2

        label3 = QtGui.QLabel("Width:")
        layout.addWidget(label3, row=3, col=0)
        self._arrow_label3 = label3
        edit3 = QtGui.QLineEdit(str(self._arrow_width))
        validator3 = QtGui.QDoubleValidator(0.01, 100, 2)
        edit3.setValidator(validator3)
        edit3.textChanged.connect(self._changed_arrow)
        layout.addWidget(edit3, row=3, col=1)
        self._arrow_width_edit = edit3

        self._dock_toggle_arrow()

        layout.layout.setContentsMargins(0, 0, 0, 5)

        return layout

    def _changed_arrow(self):
        try:
            #fix if zero
            self._arrow_start = float(self._arrow_start_edit.text())
            self._arrow_width = float(self._arrow_width_edit.text())
        except ValueError:
            pass
        self.update()

    def _dock_toggle_arrow(self):
        b = self._arrow_check_box.isChecked()
        self._arrow_label2.setEnabled(b)
        self._arrow_start_edit.setEnabled(b)
        self._arrow_label3.setEnabled(b)
        self._arrow_width_edit.setEnabled(b)
        if b != self._arrow:
            self._arrow = b
            self.update()


