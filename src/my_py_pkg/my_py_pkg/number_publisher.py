import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64



class NumberPublisherNode(Node):
    def __init__(self):
        super().__init__('number_publisher')
        self._number = 1
        self._publishe_frequency = 1.0
        self._pub = self.create_publisher(Int64, 'number', 10)
        self._timer = self.create_timer(1.0/self._publishe_frequency, self._on_pub)
        self.get_logger().info("Number publisher has been started")



    def _on_pub(self):
        msg = Int64()
        msg.data = self._number 
        self._pub.publish(msg)
        self.get_logger().info(f"Published: {msg.data}")
        self._number +=1

def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisherNode()   
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()