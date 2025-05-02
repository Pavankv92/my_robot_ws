import rclpy
from rclpy.node import Node
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle.node import LifecycleState, TransitionCallbackReturn

from example_interfaces.msg import Int64



class NumberPublisherNode(LifecycleNode):
    def __init__(self):
        super().__init__('number_publisher_lifecycle')
        self.get_logger().info("In unconfigure state")
        self._number = 1
        self._publishe_frequency = 1.0
        self._pub = None
        self._timer = None

    # Create ROS2 communication, connect to HW etc. 
    def on_configure(self, previous_state : LifecycleState) -> TransitionCallbackReturn:
        self.get_logger().info("In on_configure")
        self._pub = self.create_lifecycle_publisher(Int64, 'number', 10)
        self._timer = self.create_timer(1.0/self._publishe_frequency, self._on_pub)
        self._timer.cancel()
        return TransitionCallbackReturn.SUCCESS
    
    # Activate/Enable HW
    def on_activate(self, previous_state : LifecycleState) -> TransitionCallbackReturn:
        self.get_logger().info("In on_activate")
        self._timer.reset()
        return super().on_activate(previous_state)
    
    # Deactivate/Disable HW
    def on_deactivate(self, previous_state : LifecycleState) -> TransitionCallbackReturn:
        self.get_logger().info("In on_deactivate")
        self._timer.cancel()
        return super().on_deactivate(previous_state)
    
    # destroy ROS2 communication, disconnect to HW etc. 
    def on_cleanup(self, previous_state : LifecycleState) -> TransitionCallbackReturn:
        self.get_logger().info("In on_cleanup")
        self.destroy_lifecycle_publisher(self._pub)
        self.destroy_timer(self._timer)
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, previous_state : LifecycleState) -> TransitionCallbackReturn:
        self.get_logger().info("In on_shutdown")
        self.destroy_lifecycle_publisher(self._pub)
        self.destroy_timer(self._timer)
        return TransitionCallbackReturn.SUCCESS
    
    # Prcocess the error
    def on_error(self, previous_state : LifecycleState) -> TransitionCallbackReturn:
        self.get_logger().info("In on_error")
        self.destroy_lifecycle_publisher(self._pub)
        self.destroy_timer(self._timer)

        # do some check, if okay return SUCCESSS, f not, FAILURE
        
        return TransitionCallbackReturn.SUCCESS # from here SUCCESS --> go to unconfigure, FAILURE --> go to finalized
        
    
    def _on_pub(self):
        msg = Int64()
        msg.data = self._number 
        self._pub.publish(msg)
        # self.get_logger().info(f"Published: {msg.data}")
        self._number +=1
   
def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisherNode()   
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()