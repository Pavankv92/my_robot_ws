import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor, MultiThreadedExecutor
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
        

def main(args=None):
    rclpy.init(args=args)
    node_1 = Node1()  
    node_2 = Node2()   

    
    executor = SingleThreadedExecutor()
    executor.add_node(node_1)
    executor.add_node(node_2)

    executor.spin()
    
    node_1.destroy_node()
    node_2.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()