#!/usr/bin/env python3
import math, time
import rclpy
from rclpy.node import Node
from rclpy.action.server import ActionServer, CancelResponse, GoalResponse
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rc_car_interfaces.action import DriveDistance
from copy import deepcopy
from rclpy.executors import MultiThreadedExecutor


FEEDBACK_HZ = 10
LINEAR_GAIN  = 0.6           # Ratio of max speed to command

class DriveDistanceServer(Node):
    def __init__(self):
        super().__init__('drive_distance_server')

        self.declare_parameter('limit', 1.0)  # shared with service

        # Publishers/Subscribers
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self._odom_cb, 10)

        # Action server
        self.action_srv = ActionServer(
            self,
            DriveDistance,
            'drive_distance',
            execute_callback=self._execute_cb,
            goal_callback=self._goal_cb,
            cancel_callback=self._cancel_cb)

        self._curr_pose = None

    # Odometry callback
    def _odom_cb(self, msg: Odometry):
        self._curr_pose = msg.pose.pose

    # Goal validation
    def _goal_cb(self, *args):
    # Compatibility with both 1-arg (old) and 2-arg (new) callback API
        if len(args) == 2:
            goal_request, goal_id = args
        elif len(args) == 1:
            goal_request = args[0]
            goal_id = None
        else:
            self.get_logger().error(f"Invalid number of args to _goal_cb: {len(args)}")
            return GoalResponse.REJECT

        if self._curr_pose is None:
            self.get_logger().warn('No odom yet—rejecting goal')
            return GoalResponse.REJECT

        self.get_logger().info(f"Goal received: {goal_request.distance_m:.2f} m")
        return GoalResponse.ACCEPT


    # Cancel handling
    def _cancel_cb(self, goal_handle):
        self.get_logger().info('Goal cancel requested')
        return CancelResponse.ACCEPT

    # Main execution
    def _execute_cb(self, goal_handle):
        goal = goal_handle.request
        target = float(goal.distance_m)

        # Wait until we get a valid odometry reading
        while rclpy.ok() and self._curr_pose is None:
            self.get_logger().warn('Waiting for odometry...')
            time.sleep(0.1)

        start = deepcopy(self._curr_pose)
        remaining = abs(target)

        # Determine speed sign
        direction = math.copysign(1.0, target)
        max_speed = self.get_parameter('limit').value
        cmd_speed = LINEAR_GAIN * max_speed * direction

        twist = Twist()
        twist.linear.x = cmd_speed

        last_feedback = self.get_clock().now()

        self.get_logger().info(f'Driving {target:.2f} m ({cmd_speed:.2f} m/s)')

        while rclpy.ok() and not goal_handle.is_cancel_requested:
            time.sleep(0.01)

            if self._curr_pose is None:
                continue

            dx = self._curr_pose.position.x - start.position.x
            dy = self._curr_pose.position.y - start.position.y
            distance_moved = math.sqrt(dx*dx + dy*dy)
            remaining = abs(target) - distance_moved

            if remaining <= 0.01:
                break

            self.cmd_pub.publish(twist)

            now = self.get_clock().now()
            if (now - last_feedback).nanoseconds > 1e9 / FEEDBACK_HZ:
                goal_handle.publish_feedback(
                    DriveDistance.Feedback(remaining_m=max(0.0, remaining)))
                last_feedback = now

        if goal_handle.is_cancel_requested:
            self.cmd_pub.publish(Twist())  # <== stop here too
            goal_handle.canceled()
            self.get_logger().info('Drive canceled')
            return DriveDistance.Result(reached=False)

        self.cmd_pub.publish(Twist())  # <== stop if goal reached
        goal_handle.succeed()
        self.get_logger().info('Target reached')
        return DriveDistance.Result(reached=True)




def main():
    rclpy.init()
    server = DriveDistanceServer()
    executor = MultiThreadedExecutor()
    executor.add_node(server)

    try:
        executor.spin()
    except KeyboardInterrupt:
        server.get_logger().info('Shutting down drive server')
    finally:
        server.cmd_pub.publish(Twist())   # Ensure stop
        server.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
