import rclpy
from rclpy.node import Node
from std_msgs.msg import String



class MySubscriber(Node):
    def __init__(self):
        super().__init__('my_subscriber')
        self._sub = self.create_subscription(String, 'my_topic', self._sub_callback, 10)
        self.get_logger().info("My Subscriber has been started")
       
    def _sub_callback(self, msg):
        self.get_logger().info(f"Received: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = MySubscriber()   
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()