from pyqtgraph import QtGui

from .utils import compute_bbox


class ExportDialog:

    def __init__(self, window):

        bbox = compute_bbox(window.viewBox.addedItems)
        self.bbox_height = 2
        self.bbox_width = 2

        if bbox is not None:
            self.bbox_width = bbox[1][0] - bbox[0][0]
            self.bbox_height = bbox[1][1] - bbox[0][1]

        self.dialog = QtGui.QDialog(window.win)
        layout = QtGui.QGridLayout(self.dialog)

        label_1 = QtGui.QLabel("File name:")
        layout.addWidget(label_1, 0, 0)

        self.file_name_line_edit = QtGui.QLineEdit()
        layout.addWidget(self.file_name_line_edit, 0, 1)

        button_1 = QtGui.QPushButton("Choose a file")
        layout.addWidget(button_1, 0, 2)
        button_1.clicked.connect(self._choose_file)

        label_2 = QtGui.QLabel("XKCD:")
        layout.addWidget(label_2, 1, 0)

        self.xkcd_checkbox = QtGui.QCheckBox("")
        layout.addWidget(self.xkcd_checkbox, 1, 1)

        self.width_label = QtGui.QLabel("Width (in cm):")
        layout.addWidget(self.width_label, 2, 0)

        self.width_line_edit = QtGui.QLineEdit()
        validator = QtGui.QDoubleValidator(1.0, 50.0, 2)
        self.width_line_edit.setValidator(validator)
        layout.addWidget(self.width_line_edit, 2, 1)
        self.width_line_edit.textChanged.connect(self._width_changed)

        self.width_radio = QtGui.QRadioButton("")
        layout.addWidget(self.width_radio, 2, 2)
        self.width_radio.toggled.connect(self._radio_buttons_toggled)

        self.height_label = QtGui.QLabel("Height (in cm):")
        layout.addWidget(self.height_label, 3, 0)

        self.height_line_edit = QtGui.QLineEdit()
        self.height_line_edit.setValidator(validator)
        layout.addWidget(self.height_line_edit, 3, 1)
        self.height_line_edit.textChanged.connect(self._height_changed)

        self.height_radio = QtGui.QRadioButton("")
        layout.addWidget(self.height_radio, 3, 2)

        button_2 = QtGui.QPushButton("Export")
        layout.addWidget(button_2, 4, 2)
        button_2.clicked.connect(self._export)

        self.width_radio.setChecked(True)
        self.width_line_edit.setText("3.0")
        self.width = None
        self._width_changed()

    def _export(self):
        errors = []

        file_name = self.file_name_line_edit.text()
        if file_name == "":
            errors.append("ERROR: empty file.")

        width = self.width_line_edit.text()
        if width == "":
            errors.append("ERROR: width not set.")

        height = self.height_line_edit.text()
        if height == "":
            errors.append("ERROR: height not set.")

        if errors:
            dialog = QtGui.QDialog(self.dialog)
            dialog.setWindowTitle("Error")
            layout = QtGui.QGridLayout(dialog)

            for i, e in enumerate(errors):
                label = QtGui.QLabel(e)
                label.setStyleSheet("QLabel {color: red;}")
                layout.addWidget(label, i, 0)

            button = QtGui.QPushButton("OK")
            layout.addWidget(button, len(errors), 0)
            button.clicked.connect(dialog.close)
            dialog.exec()

    def _radio_buttons_toggled(self):
        width_checked = self.width_radio.isChecked()
        self.width_label.setEnabled(width_checked)
        self.width_line_edit.setEnabled(width_checked)

        height_checked = self.height_radio.isChecked()
        self.height_label.setEnabled(height_checked)
        self.height_line_edit.setEnabled(height_checked)

    def _width_changed(self):
        if self.width_line_edit.isEnabled():
            try:
                w = float(self.width_line_edit.text())
                h = w * self.bbox_height / self.bbox_width
                self.height_line_edit.setText(str(h))
            except ValueError:
                pass

    def _height_changed(self):
        if self.height_line_edit.isEnabled():
            try:
                h = float(self.height_line_edit.text())
                w = h * self.bbox_width / self.bbox_height
                self.width_line_edit.setText(str(w))
            except ValueError:
                pass

    def exec(self):
        self.dialog.exec()

    def check_xkcd(self):
        self.xkcd_checkbox.setChecked(True)

    def _choose_file(self):

        file_name = QtGui.QFileDialog.getSaveFileName(None,
                                                      "Save File",
                                                      "",
                                                      "Files (*.png, *.pdf)")

        if file_name[-4:] != ".png" and file_name[-4:] != ".pdf":
            file_name += ".png"

        self.file_name_line_edit.setText(file_name)
