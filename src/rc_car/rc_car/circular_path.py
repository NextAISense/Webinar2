import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CircularPath(Node):
    def __init__(self):
        super().__init__('circular_path')

        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info("Robot Controller Node has started.")

        self.running = True

        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz
        self.create_shutdown_handler()

    def create_shutdown_handler(self):
        import signal
        signal.signal(signal.SIGINT, self.shutdown_handler)  # Handles Ctrl+C gracefully

    def shutdown_handler(self, signum, frame):
        self.get_logger().info("Ctrl+C received, stopping robot...")
        self.running = False

    def timer_callback(self):
        if self.running:
            msg = Twist()
            msg.linear.x = 1.0
            msg.angular.z = 1.0
            self.cmd_vel_pub.publish(msg)
        else:
            stop_msg = Twist()  # All zeros
            self.cmd_vel_pub.publish(stop_msg)
            self.get_logger().info("Robot has stopped.")
            rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    controller = CircularPath()
    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()

if __name__ == '__main__':
    main()
