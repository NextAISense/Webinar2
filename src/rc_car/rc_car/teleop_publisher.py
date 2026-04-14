#!/usr/bin/env python3
import sys, termios, tty, rclpy
from geometry_msgs.msg import Twist

KEY_BINDINGS = {'w': ( 1.0, 0.0),
                's': (-1.0, 0.0),
                'a': ( 0.6, 1.5),
                'd': ( 0.6,-1.5),
                ' ': ( 0.0, 0.0)}

def get_key():
    fd, old = sys.stdin.fileno(), termios.tcgetattr(sys.stdin.fileno())
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def main():
    rclpy.init()
    node = rclpy.create_node('rc_car_teleop')
    pub  = node.create_publisher(Twist, '/cmd_vel', 10)
    node.get_logger().info('Use WASD keys to drive; space to stop.')
    rate = node.create_rate(10)
    try:
        while rclpy.ok():
            key = get_key()
            if key in KEY_BINDINGS:
                lin, ang = KEY_BINDINGS[key]
                msg = Twist()
                msg.linear.x, msg.angular.z = lin, ang
                pub.publish(msg)
                node.get_logger().info(f'Publishing to cmd_vel → lin={lin:.2f} ang={ang:.2f}')
            elif key == '\x03':  # Ctrl‑C
                break
            rate.sleep()
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()

if __name__ == '__main__':
    main()
