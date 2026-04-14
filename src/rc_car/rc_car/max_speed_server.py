#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rc_car_interfaces.srv import SetMaxSpeed

MAX_ALLOWED = 10.0          # Absolute ceiling in m/s (safety)

class MaxSpeedServer(Node):
    def __init__(self):
        super().__init__('max_speed_server')

        # Declare the parameter once; can be overridden via YAML or CLI
        self.declare_parameter('limit', 1.0)
        self.get_logger().info(f"Initial max_speed limit = {self.get_parameter('limit').value:.2f} m/s")

        # Service
        self.srv = self.create_service(
            SetMaxSpeed,
            'set_max_speed',
            self.handle_set_speed,
            qos_profile=rclpy.qos.QoSProfile(depth=1))

    def handle_set_speed(self, request: SetMaxSpeed.Request, response: SetMaxSpeed.Response):
        new_val = float(request.max_speed)

        if new_val < 0.0:
            self.get_logger().warn('Negative speed rejected')
            response.accepted = False
            return response

        if new_val > MAX_ALLOWED:
            self.get_logger().warn(f'Request {new_val:.2f} > {MAX_ALLOWED} m/s; clamped')
            new_val = MAX_ALLOWED

        old_val = self.get_parameter('limit').value
        self.set_parameters([Parameter('limit', Parameter.Type.DOUBLE, new_val)])

        self.get_logger().info(f'Limit changed {old_val:.2f} → {new_val:.2f} m/s')
        response.accepted = True
        return response


def main():
    rclpy.init()
    server = MaxSpeedServer()
    rclpy.spin(server)
    server.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
