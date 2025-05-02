import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
import time



class Node1(Node):
    def __init__(self):
        super().__init__('node1')
        self._timer = self.create_timer(1.0, self._callback_timer_1)
        self._timer = self.create_timer(1.0, self._callback_timer_2)
        self._timer = self.create_timer(1.0, self._callback_timer_3)

        self.get_logger().info("Number publisher has been started")

    def _callback_timer_1(self):
        time.sleep(2.0)
        self.get_logger().info(f"callback_1")
    
    def _callback_timer_2(self):
        time.sleep(2.0)
        self.get_logger().info(f"callback_2")
    
    def _callback_timer_3(self):
        time.sleep(2.0)
        self.get_logger().info(f"callback_3")
        

def main(args=None):
    rclpy.init(args=args)
    node = Node1()   
    
    executor = SingleThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()