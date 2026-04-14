#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from rc_car_interfaces.msg import WheelSpeeds
from builtin_interfaces.msg import Time

WHEEL_RADIUS = 0.135  # meters

class WheelSpeedPublisher(Node):
    def __init__(self):
        super().__init__('wheel_speed_publisher')
        self.sub = self.create_subscription(Odometry, '/odom', self.odom_cb, 10)
        self.pub = self.create_publisher(WheelSpeeds, '/wheel_speeds', 10)

    def odom_cb(self, msg: Odometry):
        vx = msg.twist.twist.linear.x

        # Convert linear velocity to RPM for both wheels (fake same speed both sides)
        rpm = (vx / (2 * 3.1416 * WHEEL_RADIUS)) * 60.0

        wheel_msg = WheelSpeeds()
        wheel_msg.left_rpm = float(rpm)
        wheel_msg.right_rpm = float(rpm)
        wheel_msg.stamp = self.get_clock().now().to_msg()

        self.pub.publish(wheel_msg)
        self.get_logger().info(f'Wheel RPM: {rpm:.2f}')

def main():
    rclpy.init()
    node = WheelSpeedPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
