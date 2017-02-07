import matplotlib.pyplot as plt

from .utils import compute_bbox
from .jtext import JtextROI


class JPlotting:

    def __init__(self, objects):

        self.objects = [obj for obj in objects]
        self._bbox = None

    def add_object(self, obj):
        self.objects.append(obj)

    def compute_bbox(self):
        points = []
        for obj in self.objects:
            bbox = obj.compute_bbox()
            points.append([bbox[0][0], bbox[0][1]])
            points.append([bbox[1][0], bbox[1][1]])
        self._bbox = compute_bbox(points)

    def plot(self, filename, xkcd=False, size=None):

        plt.close("all")

        if xkcd:
            plt.xkcd()

        if size is not None:
            plt.figure(figsize=size)

        for obj in self.objects:

            if type(obj) is JtextROI:
                pass
            else:
                points = obj._get_drawing_points()

                x = [p[0] for p in points]
                y = [p[1] for p in points]

                color = obj._color

                plt.plot(x, y, color=color, linestyle="-")

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
