import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
from example_interfaces.msg import Int64


class ParamPublisher(Node):
    def __init__(self):
        super().__init__('param_publisher')

        self.declare_parameter('number', value=2)
        self.declare_parameter('time_period', value=1.0)
        # trace for param change

        self._pub = self.create_publisher(Int64, 'my_topic', 10)
        self.get_logger().info("My Publisher has been started")
        self._number = self.get_parameter('number').value
        self._timer_period =  self.get_parameter('time_period').value
        self._timer = self.create_timer(self._timer_period, self._on_pub)
        self.add_post_set_parameters_callback(self._on_param_change)



    def _on_pub(self):
        msg = Int64() 
        msg.data = self._number 
        self._pub.publish(msg)
        self.get_logger().info(f"Published: {msg.data}")

    def _on_param_change(self, params: list[Parameter]) -> SetParametersResult:
        result = SetParametersResult()
        for param in params:
            if param.name == 'number' and param.type_ == Parameter.Type.INTEGER :
                self._number = param.value
                self.get_logger().info(f'param number changed! new value is : {self._number}')
                result.successful = True
        
        return result


def main(args=None):
    rclpy.init(args=args)
    node = ParamPublisher()   
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()