#!/usr/bin/env python3
import rclpy
from rclpy.action import ActionClient
from rc_car_interfaces.action import DriveDistance
import sys
import signal

def feedback_cb(feedback_msg):
    feedback = feedback_msg.feedback
    print(f'⏱ Remaining distance: {feedback.remaining_m:.2f} m')

def main():
    rclpy.init()
    node = rclpy.create_node('drive_action_client')
    client = ActionClient(node, DriveDistance, 'drive_distance')

    # Check if user provided a distance argument
    if len(sys.argv) < 2:
        print("❌ Usage: ros2 run rc_car drive_action_client <distance_in_meters>")
        rclpy.shutdown()
        return

    try:
        distance = float(sys.argv[1])
    except ValueError:
        print("❌ Invalid distance value. Please provide a number.")
        rclpy.shutdown()
        return

    if not client.wait_for_server(timeout_sec=5.0):
        node.get_logger().error('Action server not available')
        rclpy.shutdown()
        return

    goal_msg = DriveDistance.Goal()
    goal_msg.distance_m = distance
    node.get_logger().info(f'Sending goal: {goal_msg.distance_m:.2f} m')

    future_goal = client.send_goal_async(goal_msg, feedback_callback=feedback_cb)

    def cancel_goal_on_interrupt(signum, frame):
        node.get_logger().warn('Ctrl+C detected! Cancelling goal...')
        if future_goal.done():
            goal_handle = future_goal.result()
            goal_handle.cancel_goal_async()
        rclpy.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, cancel_goal_on_interrupt)

    rclpy.spin_until_future_complete(node, future_goal)
    goal_handle = future_goal.result()

    if not goal_handle.accepted:
        node.get_logger().warn('Goal was rejected by server')
        node.destroy_node()
        rclpy.shutdown()
        return

    node.get_logger().info('Goal accepted, waiting for result...')
    result_future = goal_handle.get_result_async()
    rclpy.spin_until_future_complete(node, result_future)

    result = result_future.result().result
    if result.reached:
        node.get_logger().info('✅ Goal succeeded!')
    else:
        node.get_logger().warn('❌ Goal failed or cancelled')

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
