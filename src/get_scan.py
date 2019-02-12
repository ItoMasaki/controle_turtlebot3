import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Vector3, Quaternion, Point
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry

from tf import Quaternion2Euler

import sys

from time import sleep

import numpy
from numpy import arange, array, pi, float32, inf, float64
from numpy import cos, sin, arctan2, rad2deg, deg2rad
from numpy import sqrt, round

from matplotlib import pyplot as plt


# 現在位置からの物体距離を計算
class make_map(Node):

    def __init__(self):
        super(make_map, self).__init__("turtlebot3")

        # 型の初期化
        self.position        = Point()
        self.orientation     = Quaternion()
        self.range           = array(0)
        self.angle           = array(0)
        self.range_max       = array(0)

        self.x               = float(0.0)
        self.y               = float(0.0)

        self.range_min       = float(0)
        self.range_min_num   = float(0)
        self.angle_min       = float(0)
        self.angle_increment = float(0)

        # 読み込みノード作成
        self.create_subscription(LaserScan, "/scan", self.LaserScan_callback)
        self.create_subscription(Odometry, "/odom", self.Odometry_callback)
        self.create_timer(0.2, self.PositionCalc)

        self.vel_pub_node = self.create_publisher(Twist, "/cmd_vel")

    def LaserScan_callback(self, data):
        self.angle_increment = data.angle_increment
        self.angle           = arange(90*self.angle_increment, 450*self.angle_increment, self.angle_increment, dtype=float32)
        self.range           = array(data.ranges)
        self.range_min       = self.range.min()
        self.range_min_num   = self.range.argmin()

    def Odometry_callback(self, data):
        self.position.x      = -data.pose.pose.position.y
        self.position.y      = data.pose.pose.position.x
        self.orientation     = data.pose.pose.orientation

    def PositionCalc(self):
        self.euler = Quaternion2Euler(self.orientation)

        self.x     = self.range*cos(self.angle - self.euler.z) + self.position.x
        self.y     = self.range*sin(self.angle - self.euler.z) + self.position.y

        self.x     = round(self.x, 3)
        self.y     = round(self.y, 3)

        self.SearchMin()
        self.Controle()

        #self.testControle()

        try:
            self.Plot(False)
        except:
            sys.exit()


    def SearchMin(self):
        self.angle_min = self.range_min_num * self.angle_increment - self.euler.z

        if self.angle_min < 0:
            self.angle_min += 2*pi

        if self.angle_min > 2*pi:
            self.angle_min -= 2*pi

        print("BODY:{0}".format(round(rad2deg(self.euler.z), 3)))

    def testControle(self):
        vel = Twist()

        vel.linear.x = 0.20

        stop = False

        if self.range_min < 0.20:
            stop = True
            vel.linear.x = 0.0
            vel.angular.z = 0.1

        self.vel_pub_node.publish(vel)

    def Controle(self):
        vel = Twist()

        angle = rad2deg(self.angle_min)
        body  = rad2deg(self.euler.z)

        if body < -90 or 90 < body:

            vel.linear.x = 0.1

            if 45 < angle and angle < 135 and self.range_min < 0.40:
                vel.angular.z = -0.20

            elif angle > 225 and angle < 315 and self.range_min < 0.40:
                vel.angular.z = 0.20

            else:
                pass

        elif -90 < body and body < 90:

            vel.linear.x = 0.1

            if 0 < angle and angle < 180:
                vel.angular.z = -0.20

            elif angle > 180 and angle < 360:
                vel.angular.z = 0.20
            else:
                pass
        else:
            pass

        if self.range_min < 0.15:
            vel.linear.x = -0.25

        self.vel_pub_node.publish(vel)

    def Plot(self, cla=True):
        if cla:
            plt.cla()
        plt.xlim(-3, 3)
        plt.ylim(-3, 3)
        plt.scatter(self.x, self.y, s=0.5, color="blue")
        plt.scatter(self.position.x, self.position.y, s=1, color="black")
        #plt.quiver(self.position.x, self.position.y, cos(self.angle_min + deg2rad(90)), sin(self.angle_min + deg2rad(90)))
        #plt.quiver(self.position.x, self.position.y, cos(self.euler.z + deg2rad(90)), sin(self.euler.z + deg2rad(90)))
        plt.pause(0.1)


def main():
    rclpy.init()
    node = make_map()
    rclpy.spin(node)

if __name__ == "__main__":
    main()
