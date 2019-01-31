import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan

from numpy import arange, array, pi, float32, cos, sin, inf

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt


class SLAM(QWidget):
    def __init__(self):
        super().__init__(self)

        #self.

        self.init_UI()

    def init_UI(self):
        self.setGeometry(300, 300, 280, 170)


class get_odom(Node):
    def __init__(self):
        super().__init__("turtlebot3")

        self.create_subscription(LaserScan, "/scan", self.LaserScan_callback)


    def LaserScan_callback(self, data):

        self.angle = arange(0, 360*data.angle_increment, data.angle_increment, dtype=float32)
        self.range = array(data.ranges)

        self.range_max = data.range_max

        self.odom_base_map()

    def odom_base_map(self):
        self.x = self.range*cos(self.angle)
        self.y = self.range*sin(self.angle)

        self.x[self.x == -inf] = self.range_max
        self.x[self.x == inf] = self.range_max

        self.y[self.y == -inf] = self.range_max
        self.y[self.y == inf] = self.range_max

        print(self.x)


def main():
    rclpy.init()

    node = get_odom()

    rclpy.spin(node)

    node.destroy_node()
    #try:
    #    print("worked!")
    #    rclpy.spin(node)
    #except:
    #    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
