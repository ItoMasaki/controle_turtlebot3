import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan

class get_odom(Node):
    def __init__(self):
        super().__init__("turtlebot3")

        self.create_subscription(LaserScan, "/scan", self.callback)


    def callback(self, data):
        print(data)


def main():
    rclpy.init()

    node = get_odom()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()



if __name__ == "__main__":
    main()
