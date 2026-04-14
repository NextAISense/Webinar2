import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import math

class OdomListener(Node):
    def __init__(self):
        super().__init__('odom_listener')

        # Create subscriber to /odom
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.listener_callback,
            10
        )
        self.subscription  # prevent unused variable warning

        self.get_logger().info('Subscribed to /odom')

    def listener_callback(self, msg: Odometry):
        # Position
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        # Orientation (quaternion to yaw)
        q = msg.pose.pose.orientation
        yaw = self.get_yaw_from_quaternion(q)

        # Velocities
        lin_vel = msg.twist.twist.linear.x
        ang_vel = msg.twist.twist.angular.z

        # Log data
        self.get_logger().info(
            f'Position: x={x:.2f}, y={y:.2f}, Yaw={yaw:.2f} rad | '
            f'Linear vel: {lin_vel:.2f} m/s, Angular vel: {ang_vel:.2f} rad/s'
        )

    def get_yaw_from_quaternion(self, q):
        # Convert quaternion to yaw angle (Euler Z)
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        return math.atan2(siny_cosp, cosy_cosp)

def main(args=None):
    rclpy.init(args=args)
    node = OdomListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
