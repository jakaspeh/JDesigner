from pyqtgraph.Qt import QtGui

from jdesigner.jwindow import Jwindow


def main():
    app = QtGui.QApplication([])
    w = Jwindow()
    w.show()

    QtGui.QApplication.instance().exec_()

if __name__ == "__main__":
    main()
