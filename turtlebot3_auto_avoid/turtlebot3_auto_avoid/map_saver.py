import rclpy
from rclpy.node import Node
from nav2_msgs.srv import SaveMap

class MapSaver(Node):
    def __init__(self):
        super().__init__('map_saver_node')
        self.cli = self.create_client(SaveMap, '/map_saver/save_map')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for map_saver service...')

        self.req = SaveMap.Request()
        self.req.map_topic = '/map'
        self.req.map_url = 'my_saved_map'  # Will create my_saved_map.pgm + .yaml
        self.req.image_format = 'pgm'
        self.req.free_thresh = 0.25
        self.req.occupied_thresh = 0.65

    def save_map(self):
        self.get_logger().info("Calling map_saver service...")
        future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info("✅ Map saved successfully!")
        else:
            self.get_logger().error("❌ Failed to save map.")

def main(args=None):
    rclpy.init(args=args)
    node = MapSaver()
    node.save_map()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

