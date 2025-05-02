from rclpy.node import Node
import time



class Node1(Node):
    def __init__(self):
        super().__init__('node1')
        self._timer = self.create_timer(1.0, self._callback_timer_1)
        self._timer = self.create_timer(1.0, self._callback_timer_2)
        self._timer = self.create_timer(1.0, self._callback_timer_3)

        self.get_logger().info("Node_1 : Number publisher has been started")

    def _callback_timer_1(self):
        time.sleep(2.0)
        self.get_logger().info(f"callback_1")
    
    def _callback_timer_2(self):
        time.sleep(2.0)
        self.get_logger().info(f"callback_2")
    
    def _callback_timer_3(self):
        time.sleep(2.0)
        self.get_logger().info(f"callback_3")