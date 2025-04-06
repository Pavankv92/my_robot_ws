import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import HardwareStatus



class HardwareStatusPublisherNode(Node):
    def __init__(self):
        super().__init__('hardware_status_publisher')
        self._hardware_status_pub = self.create_publisher(HardwareStatus, 'hardware_status', 10)
        self.get_logger().info("Hardware_status Publisher has been started")
        self._timer = self.create_timer(1.0, self._pub_callback)


    def _pub_callback(self):
        msg = HardwareStatus()
        msg.temperature = 25.5
        msg.are_motors_ready = True
        msg.debug_message = "Nothing!"
        self._hardware_status_pub.publish(msg)
        self.get_logger().info(f"Msg Published!")

def main(args=None):
    rclpy.init(args=args)
    node = HardwareStatusPublisherNode()   
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()