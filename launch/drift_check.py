import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import math

class DriftChecker(Node):
    def __init__(self):
        super().__init__('drift_checker')
        self.sub = self.create_subscription(Odometry, '/odom', self.cb, 10)
        self.start_x, self.start_y = None, None

    def cb(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        if self.start_x is None:
            self.start_x, self.start_y = x, y
            print(f"Baseline set at: X={x:.4f}, Y={y:.4f}")

        drift = math.sqrt((x - self.start_x)**2 + (y - self.start_y)**2) * 100
        print(f"Current Jitter/Drift: {drift:.2f} cm", end="\r")

def main():
    rclpy.init()
    rclpy.spin(DriftChecker())
if __name__ == '__main__':
    main()
