from rclpy.node import Node
import time

class Node2(Node):
    def __init__(self):
        super().__init__('node2')
        self._timer = self.create_timer(1.0, self._callback_timer_4)
        self._timer = self.create_timer(1.0, self._callback_timer_5)
        self._timer = self.create_timer(1.0, self._callback_timer_6)

        self.get_logger().info("Node_2 : Number publisher has been started")

    def _callback_timer_4(self):
        time.sleep(2.0)
        self.get_logger().info(f"callback_4")
    
    def _callback_timer_5(self):
        time.sleep(2.0)
        self.get_logger().info(f"callback_5")
    
    def _callback_timer_6(self):
        time.sleep(2.0)
        self.get_logger().info(f"callback_6")