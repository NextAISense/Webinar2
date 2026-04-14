import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import time

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')

        # Publisher for DiffDrive (cmd_vel)
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        # Publisher for JointPositionController (joint_5)
        self.joint_pub = self.create_publisher(Float64, 'steering_joint', 10)

        self.get_logger().info("Robot Controller Node has started.")

    def move_robot(self, linear_x=0.5, angular_z=0.0, duration=2.0):
        """Move the robot with a given linear and angular velocity for a duration."""
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z

        start_time = time.time()
        while time.time() - start_time < duration:
            self.cmd_vel_pub.publish(msg)
            time.sleep(0.1)

        # Stop robot
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.cmd_vel_pub.publish(msg)

    def move_joint(self, position=1.0):
        """Move joint j5 to a target position."""
        msg = Float64()
        msg.data = position
        self.joint_pub.publish(msg)
        self.get_logger().info(f"Moved joint j5 to {position}")

def main(args=None):
    rclpy.init(args=args)
    controller = RobotController()

    try:
        # Move the joint
        controller.move_joint(-1.0)
        # Move forward for 2 seconds
        controller.move_robot(1.0, 0.0, 30.0)

        # Turn right for 1 second
        # controller.move_robot(0.0, -0.5, 1.0)



    except KeyboardInterrupt:
        pass

    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

