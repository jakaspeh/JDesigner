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

        if xkcd:
            plt.xkcd()

        if size is not None:
            plt.figure(figsize=size)

        for obj in self.objects:

            if type(obj) is Jcomposition:
                for o in obj.objects:
                    points = o._get_drawing_points()
                    color = o._color
                    self._plot(points, color)
            elif type(obj) is JtextROI:
                print("Skipping JtextROI")
            elif type(obj) is Jtext:
                print("Skipping Jtext")
            else:
                points = obj._get_drawing_points()
                self._plot(points, obj._color)

        self.compute_bbox()
        x0, y0 = self._bbox[0]
        x1, y1 = self._bbox[1]
        eps_x = (x1 - x0) / 100
        eps_y = (y1 - y0) / 100
        plt.xlim([x0 - eps_x, x1 + eps_x])
        plt.ylim([y0 - eps_y, y1 + eps_y])

        plt.axis("off")
        plt.axes().set_aspect("equal")

        plt.savefig(filename, bbox_inches="tight", pad_inches=0)

    def _plot(self, points, color):
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        plt.plot(x, y, color=color, linestyle="-")
