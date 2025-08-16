import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class AutoAvoid(Node):
    def __init__(self):
        super().__init__('auto_avoid_debug')
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.twist = Twist()

    def scan_callback(self, msg):
        # Split ranges into sectors
        front = msg.ranges[0:10] + msg.ranges[-10:]   # 0° ± small angle
        left = msg.ranges[len(msg.ranges)//4 : len(msg.ranges)//4 + 20]  # 90° ± small angle
        right = msg.ranges[-(len(msg.ranges)//4 + 20) : -(len(msg.ranges)//4)]  # -90° ± small angle

        # Get min distances
        min_front = min(front)
        min_left = min(left)
        min_right = min(right)

        # Debug output
        self.get_logger().info(
            f"Front: {min_front:.2f} m | Left: {min_left:.2f} m | Right: {min_right:.2f} m"
        )

        # Simple avoidance logic
        if min_front < 0.5:
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.5 if min_left > min_right else -0.5
        else:
            self.twist.linear.x = 0.2
            self.twist.angular.z = 0.0

        self.cmd_pub.publish(self.twist)
        self.get_logger().info(
            f"CMD → linear.x: {self.twist.linear.x:.2f}, angular.z: {self.twist.angular.z:.2f}"
        )

def main(args=None):
    rclpy.init(args=args)
    node = AutoAvoid()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

