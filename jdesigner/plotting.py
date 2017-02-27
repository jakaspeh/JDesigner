import matplotlib.pyplot as plt

from .utils import compute_bbox
from .jtext import JtextROI
from .jtext import Jtext
from .jcomposition import Jcomposition


class JPlotting:

    def __init__(self, objects):

        self.objects = [obj for obj in objects]
        self._bbox = None

    def add_object(self, obj):
        self.objects.append(obj)

    def compute_bbox(self):
        self._bbox = compute_bbox(self.objects)

    def plot(self, filename, xkcd=False, size=None):

        plt.close("all")

        self.compute_bbox()
        x0, y0 = self._bbox[0]
        x1, y1 = self._bbox[1]

        width = x1 - x0
        height = y1 - y0

        if xkcd:
            plt.xkcd()

        if size is not None:
            plt.figure(figsize=size)

        for obj in self.objects:

            if type(obj) is Jcomposition:
                for o in obj.objects:
                    points = o.get_drawing_points()
                    color = o._color
                    self._plot(points, color)
            elif type(obj) is JtextROI:
                self._plot_text(obj)
            elif type(obj) is Jtext:
                pass
            else:
                points = obj.get_drawing_points()
                self._plot(points, obj._color)

        eps_x = width / 100
        eps_y = height / 100
        plt.xlim([x0 - eps_x, x1 + eps_x])
        plt.ylim([y0 - eps_y, y1 + eps_y])

        plt.axis("off")
        plt.axes().set_aspect("equal")

        plt.tight_layout()
        plt.savefig(filename)

        # resets the xkcd style
        plt.rcdefaults()

    def _plot(self, points, color):
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        plt.plot(x, y, color=color, linestyle="-")

    def _plot_text(self, text_roi):

        x = text_roi.pos().x()
        y = text_roi.pos().y()

        size = text_roi.size
        color = text_roi._color
        text = text_roi.text.textItem.toPlainText()
        transpose = text_roi._transpose

        if transpose:
            plt.text(x, y, text, color=color, va="bottom", ha="center",
                     rotation="vertical", size=size)
        else:
            plt.text(x, y, text, color=color, ha="left", va="top", size=size)
