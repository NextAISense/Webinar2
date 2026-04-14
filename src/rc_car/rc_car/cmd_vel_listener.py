import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CmdVelListener(Node):
    def __init__(self):
        super().__init__('cmd_vel_listener')

        # Create a subscriber to /cmd_vel topic
        self.subscription = self.create_subscription(
            Twist,               # Message type
            '/cmd_vel',          # Topic name
            self.listener_callback,  # Callback function
            10                   # QoS
        )
        self.subscription  # prevent unused variable warning

        self.get_logger().info('Subscribed to /cmd_vel')

    def listener_callback(self, msg: Twist):
        # Print the received message
        self.get_logger().info(f'Received: Linear={msg.linear.x:.2f}, Angular={msg.angular.z:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
