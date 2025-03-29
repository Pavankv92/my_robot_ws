import rclpy
from rclpy.node import Node

from example_interfaces.srv import AddTwoInts
from functools import partial

class AddTwoIntsServerClient(Node):
    def __init__(self):
        super().__init__('add_two_ints_server')
        self._client = self.create_client(AddTwoInts, 'add_two_ints')
        self.get_logger().info("Add Two Ints Client has been started")
        
    # create a request, send it, set up a callback 
    def call_add_two_int(self, a :int, b :int):
        while not self._client.wait_for_service(1.0):
            self.get_logger().info("Service not available, waiting again...")
        
        #create a request
        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        # send a request async
        future = self._client.call_async(request)
        # future.add_done_callback(self.callback_call_add_two_int) --> this works!
        # to add an extra parameter to future.add_done_callback --> use partial
        future.add_done_callback(
            partial(self.callback_call_add_two_int, request=request))

    # callback for the call function
    def callback_call_add_two_int(self, future, request):
        response = future.result()
        self.get_logger().info(f'Got a response: {response.sum}')



def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsServerClient() 
    node.call_add_two_int(4, 7)
    node.call_add_two_int(1, 7)
    node.call_add_two_int(4, 3)

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()



if __name__ == "__main__":
    main()