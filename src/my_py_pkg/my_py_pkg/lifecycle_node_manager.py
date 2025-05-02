import rclpy
from rclpy.parameter import Parameter
from rclpy.node import Node
from lifecycle_msgs.srv import ChangeState
from lifecycle_msgs.msg import Transition
import time



class LifecycleNodeManager(Node):
    def __init__(self):
        super().__init__('lifecycle_node_manager')
        self.get_logger().info("lifecycle_node_manager has been started...")
        self.declare_parameter("managed_node_name", value="number_publisher_lifecycle")
        # to set the param name from the terminal
        # self.declare_parameter("managed_node_name", Parameter.Type.STRING)
        node_name = self.get_parameter("managed_node_name").value
        service_change_state_name = "/" + node_name + "/change_state"
        self.client = self.create_client(ChangeState, service_change_state_name)
    
    def change_state(self, trasition: Transition):
        self.client.wait_for_service()
        request = ChangeState.Request()
        request.transition = trasition
        future = self.client.call_async(request=request)
        rclpy.spin_until_future_complete(self, future)

    def initialization_sequence(self):
        # unconfigured to Inactive
        self.get_logger().info("unconfigure --> Inactive")
        transition = Transition()
        transition.id = Transition.TRANSITION_CONFIGURE
        transition.label = "configure"
        self.change_state(transition)
        self.get_logger().info("Configured!")

        time.sleep(3)

        # Inactive to Active
        self.get_logger().info("Inactive --> Active")
        transition = Transition()
        transition.id = Transition.TRANSITION_ACTIVATE
        transition.label = "activate"
        self.change_state(transition)
        self.get_logger().info("Acivated!")

        

def main(args=None):
    rclpy.init(args=args)
    node = LifecycleNodeManager() 
    node.initialization_sequence()  
    rclpy.shutdown()


if __name__ == "__main__":
    main()