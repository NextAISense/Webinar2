import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class MirrorSteering(Node):
    def __init__(self):
        super().__init__('mirror_steering')
        self.sub = self.create_subscription(Float64, '/steering_joint', self.callback, 10)
        self.pub = self.create_publisher(Float64, '/steering_joint_mirrored', 10)

    def callback(self, msg):
        mirrored = Float64()
        mirrored.data = -msg.data
        self.pub.publish(mirrored)

def main(args=None):
    rclpy.init(args=args)
    node = MirrorSteering()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
