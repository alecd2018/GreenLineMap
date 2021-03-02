# util.py is a file exclusively used to store low level helper functions

import math


def distTwoPoints(a, b):
    return math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)


def distPointLine(p, a, b):
    (x1, y1) = a
    (x2, y2) = b
    (x3, y3) = p
    px = x2 - x1
    py = y2 - y1
    q = px * px + py * py
    u = ((x3 - x1) * px + (y3 - y1) * py) / float(q)
    if u > 1:
        u = 1
    elif u < 0:
        u = 0
    x = x1 + u * px
    y = y1 + u * py
    dx = x - x3
    dy = y - y3
    dist = math.sqrt(dx * dx + dy * dy)
    return dist