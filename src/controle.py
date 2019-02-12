import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

from time import sleep

from sys import exit

class Controle(Node):
    def __init__(self):
        super().__init__("turtlebot3")

        self.pub = self.create_publisher(Twist, "/cmd_vel")

        self.twist = Twist()

        for i in range(2):
            self.run(0.20, 0.0)
            sleep(19)
            self.run(0.0, 0.0)
            sleep(1)

            self.run(0.0, 0.25)
            sleep(6.5)
            self.run(0.0, 0.0)
            sleep(1)

            self.run(0.20, 0.0)
            sleep(4)
            self.run(0.0, 0.0)
            sleep(1)

            self.run(0.0, 0.25)
            sleep(5.8)
            self.run(0.0, 0.0)
            sleep(1)

        self.run(0.0, 0.0)

    def run(self, l, a):
        self.twist.linear.x = float(l)
        self.twist.angular.z = float(a)

        self.pub.publish(self.twist)

def main():
    rclpy.init()

    node = Controle()

    
    try:
        rclpy.spin(node)
    except:
        node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()


