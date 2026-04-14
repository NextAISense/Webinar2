import rclpy
from rclpy.node import Node
from rc_car.srv import SetVelocity

class VelocityClient(Node):
    def __init__(self):
        super().__init__('velocity_client')
        self.cli = self.create_client(SetVelocity, 'set_velocity')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')
        self.req = SetVelocity.Request()

    def send_request(self, linear_x, angular_z):
        self.req.linear_x = linear_x
        self.req.angular_z = angular_z
        future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()

def main():
    rclpy.init()
    client = VelocityClient()

    # Example: Set velocity to 1 m/s linear and 0.5 rad/s angular
    response = client.send_request(1.0, 0.5)
    if response.success:
        print("Velocity set successfully!")
    else:
        print("Failed to set velocity.")

    rclpy.shutdown()

if __name__ == '__main__':
    main()

