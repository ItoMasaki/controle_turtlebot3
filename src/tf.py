from numpy import array
from numpy import arctan2, arcsin, sin
from numpy import pi

from geometry_msgs.msg import Quaternion

class Euler():
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

def Quaternion2Matrix(ary: Quaternion) -> array:

    x, y, z, w = ary.x, ary.y, ary.z, ary.w

    m00 = 1     - 2*y**2 - 2*z**2
    m01 = 2*x*y + 2*w*z
    m02 = 2*x*z - 2*w*y
    m03 = 0

    m10 = 2*x*y - 2*w*z
    m11 = 1     - 2*x**2 - 2*z**2
    m12 = 2*y*z + 2*w*x
    m13 = 0
    
    m20 = 2*x*z + 2*w*y
    m21 = 2*y*z - 2*w*x
    m22 = 1     - 2*x**2 - 2*y**2
    m23 = 0

    m30 = 0
    m31 = 0
    m32 = 0
    m33 = 1

    return array([
        [m00, m01, m02, m03],
        [m10, m11, m12, m13],
        [m20, m21, m22, m23],
        [m30, m31, m32, m33]
        ])


def Matrix2Euler(ary: array) -> array:
    euler = Euler()

    euler.x = arcsin(ary[2][1])
    euler.y = arctan2(-ary[2][0], ary[2][2])
    euler.z = arctan2(-ary[0][1], ary[1][1])

    if ary[2][1] == 1:
        euler.x = pi/2
        euler.y = 0
        euler.z = arctan2(ary[1][0], ary[0][0])

    elif ary[2][1] == -1:
        euler.x = -pi/2
        euler.y = 0
        euler.z = arctan(ary[1][0], ary[0][0])

    return euler


def Quaternion2Euler(ary: Quaternion) -> array:
    return Matrix2Euler(Quaternion2Matrix(ary))
