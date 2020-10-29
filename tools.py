from vector import *


def normalizeAngle(angle):
    return angle - ceil(angle / 360.0 - 0.5) * 360.0


def normalizeRadian(radian):
    return atan2(sin(radian), cos(radian))


def inTolerance(angle, tolerance):
    return abs(angle) <= tolerance