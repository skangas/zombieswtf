from fife.fife import DoublePoint3D
from math import sqrt

def get_angle(pos1, pos2):
    x = pos2.x - pos1.x
    y = pos2.y - pos1.y
    a = DoublePoint3D(x, y)
    a.normalize()
    return a
