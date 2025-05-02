import rclpy
from rclpy.executors import SingleThreadedExecutor, MultiThreadedExecutor
from components_py.node_1 import Node1
from components_py.node_2 import Node2

      

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