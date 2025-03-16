import rclpy
from rclpy.node import Node
from std_msgs.msg import String



class MyPublisher(Node):
    def __init__(self):
        super().__init__('my_publisher')
        self._pub = self.create_publisher(String, 'my_topic', 10)
        self.get_logger().info("My Publisher has been started")
        self._timer = self.create_timer(1.0, self._pub_callback)


    def _pub_callback(self):
        msg = String()
        msg.data = "Hello World!"
        self._pub.publish(msg)
        self.get_logger().info(f"Published: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = MyPublisher()   
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()