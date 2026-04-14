# import sys
import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
#
# print(sys.path)
import rclpy
from rclpy.node import Node
from service_test.srv import SetVelocity
from geometry_msgs.msg import Twist

class VelocityServer(Node):
    def __init__(self):
        super().__init__('velocity_server')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.srv = self.create_service(SetVelocity, 'set_velocity', self.set_velocity_callback)

    def set_velocity_callback(self, request, response):
        self.get_logger().info(f"Setting velocity: linear_x={request.linear_x}, angular_z={request.angular_z}")

        # Create a Twist message to publish to /cmd_vel
        twist_msg = Twist()
        twist_msg.linear.x = request.linear_x
        twist_msg.angular.z = request.angular_z

        # Publish the velocity
        self.publisher.publish(twist_msg)

        response.success = True
        return response

def main():
    rclpy.init()
    node = VelocityServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

