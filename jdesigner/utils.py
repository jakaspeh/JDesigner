import numpy as np


def perpendicular(vector):
    return np.array([-vector[1], vector[0]])


def normalize(vector):
    return vector / np.linalg.norm(vector)


def construct_arrow(start, end, width):
    vector = end - start
    per = normalize(perpendicular(vector))
    length = np.linalg.norm(vector) * width

    mid1 = start + per * length
    mid2 = start - per * length

    return [start, mid1, end, mid2, start]


def delete_content(info_dock):
    info_dock.currentRow = 0
    info_dock.widgets.clear()

    layout = info_dock.layout
    item = layout.itemAtPosition(0, 0)
    # print(item)
    if item is not None:
        # print(item.widget())
        layout.removeItem(item)
        item.widget().setParent(None)


def get_bigger_bbox(bbox1, bbox2):
    """
    :param bbox1:
    :param bbox2:
    :return:
    Assumption: One bounding box is contained inside another
    """

    min_x_1 = min([x for x, y in bbox1])
    min_y_1 = min([y for x, y in bbox1])
    max_x_1 = max([x for x, y in bbox1])
    max_y_1 = max([y for x, y in bbox1])

    min_x_2 = min([x for x, y in bbox2])
    min_y_2 = min([y for x, y in bbox2])
    max_x_2 = max([x for x, y in bbox2])
    max_y_2 = max([y for x, y in bbox2])

    if min_x_1 < min_x_2 or min_y_1 < min_y_2:
        return bbox1

    if max_x_2 < max_x_1 or max_y_2 < max_y_1:
        return bbox1

    return bbox2

