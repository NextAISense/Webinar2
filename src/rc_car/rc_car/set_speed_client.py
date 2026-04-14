#!/usr/bin/env python3
import sys, rclpy
from rc_car_interfaces.srv import SetMaxSpeed

def main():
    rclpy.init()
    node = rclpy.create_node('set_speed_client')

    if len(sys.argv) != 2:
        node.get_logger().info('Usage: ros2 run rc_car set_speed_client <max_speed>')
        return

    try:
        max_speed = float(sys.argv[1])
    except ValueError:
        node.get_logger().error('Please provide a valid float for max_speed.')
        return

    client = node.create_client(SetMaxSpeed, 'set_max_speed')
    if not client.wait_for_service(timeout_sec=3.0):
        node.get_logger().error('Service not available!')
        return

    req = SetMaxSpeed.Request()
    req.max_speed = max_speed

    future = client.call_async(req)

    rclpy.spin_until_future_complete(node, future)

    if future.result():
        node.get_logger().info(f'Service response: accepted={future.result().accepted}')
    else:
        node.get_logger().error('Service call failed!')

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
