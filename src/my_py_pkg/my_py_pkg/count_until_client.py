import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus
from my_robot_interfaces.action import CountUntil
import time



class CountUntilClientNode(Node):
    def __init__(self):
        super().__init__('count_until_client')
        self._count_until_client = ActionClient(self, CountUntil, 'count_until')
        self.get_logger().info("count_until_action_client has been started...")

        # # create goal handle attribute
        # self._goal_handle = ClientGoalHandle()

    def send_goal(self, target_number, period):
        # wait for the server to up.
        self._count_until_client.wait_for_server()

        # create a goal
        goal = CountUntil.Goal()
        goal.target_number = target_number
        goal.period = period

        # send a goal async. async doesn't block the thread
        self.get_logger().info('sending the goal')
        future = self._count_until_client.send_goal_async(goal, feedback_callback=self._feedback_callback)

        future.add_done_callback(self._goal_response_callback)

        # send a cancel request
        # self._timer = self.create_timer(0.5, self.cancel_goal)

    def cancel_goal(self):
        self.get_logger().info('sending the cancel goal request')
        self._goal_handle.cancel_goal_async()
        self._timer.cancel()


       
    # check if our goal is accepted or not!
        # if accpeted, request result 
    def _goal_response_callback(self, future): 
        # this is the server's accepted/rejected response of type ClientGoalHandle
        # future object returns a client handle object
        self._goal_handle : ClientGoalHandle = future.result()
        # if the goal is accepted, get the result (async) after the execution 
        if self._goal_handle.accepted:
            # request result
            self.get_logger().info('goal has been accepted')
            future = self._goal_handle.get_result_async()
            future.add_done_callback(self._result_callback)
        else:
            self.get_logger().warn('goal has been rejected')


    # did our goal succeed? check the status and handle accordingly
    def _result_callback(self, future):

        # objects
        result  = CountUntil.Result()

        # get 
        status = future.result().status
        result = future.result().result

        # check
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(f'Goal succeeded!')

        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().error(f'Goal aborted!')

        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().warn(f'Goal canceled!')
        
        # finally print the result. we will recieve the result even if the goal was aborted
        self.get_logger().info(f'Result: {result.reached_number}')

    # topic
    def _feedback_callback(self, msg):
        current_number = msg.feedback.current_number 
        self.get_logger().info(f'feedback -> current_number: {current_number}')


        
def main(args=None):
    rclpy.init(args=args)
    node = CountUntilClientNode()  
    node.send_goal(6, 1.0) 
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()