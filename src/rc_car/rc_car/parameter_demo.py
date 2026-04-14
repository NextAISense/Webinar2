#!/usr/bin/env python3
import rclpy
from geometry_msgs.msg import Twist

def main():
    rclpy.init()
    node = rclpy.create_node('param_demo',
              parameters=[rclpy.parameter.Parameter('speed', rclpy.Parameter.Type.DOUBLE, 0.5)])
    pub = node.create_publisher(Twist, '/cmd_vel', 10)
    timer = node.create_timer(1.0, lambda: pub.publish(Twist(linear={'x': node.get_parameter('speed').value})))
    rclpy.spin(node)

if __name__ == '__main__':
    main()
