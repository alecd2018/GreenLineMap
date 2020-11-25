# util.py is a file exclusively used to store low level helper functions

import math


def distTwoPoints(a, b):
    return math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

# TODO: add distance between lines

# TODO: add color functions