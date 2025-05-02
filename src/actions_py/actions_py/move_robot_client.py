import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus
from my_robot_interfaces.action import MoveRobot
from example_interfaces.msg import Empty
import time



class MoveRobotClientNode(Node):
    def __init__(self):
        super().__init__('move_robot_client')
        self._goal_handle = None
        self._move_robot_client = ActionClient(self, MoveRobot, 'move_robot')
        self._cancel_sub = self.create_subscription(Empty, "cancel_move", self._cancel_move_callback, 10)
        self.get_logger().info("Move robot client has been started...")

        # # create goal handle attribute
        # self._goal_handle = ClientGoalHandle()

    def send_goal(self, position, velocity):
        # wait for the server to be up.
        self._move_robot_client.wait_for_server()

        # create a goal
        goal = MoveRobot.Goal()
        goal.position= position
        goal.velocity = velocity

        # send a goal async. async doesn't block the thread
        self.get_logger().info('sending the goal')
        # send including feedback callback
        future = self._move_robot_client.send_goal_async(goal, feedback_callback=self._feedback_callback)

        future.add_done_callback(self._goal_response_callback)

        # send a cancel request
        # self._timer = self.create_timer(0.5, self.cancel_goal)

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
            # get the result
            future = self._goal_handle.get_result_async()
            future.add_done_callback(self._result_callback)
        else:
            self.get_logger().warn('goal has been rejected')


    # did our goal succeed? check the status and handle accordingly
    def _result_callback(self, future):

        # objects
        result  = MoveRobot.Result()

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
        self.get_logger().info(f'Result: {result.position}')
        self.get_logger().info(f'Message: {result.message}')


    # topic
    def _feedback_callback(self, msg):
        current_position = msg.feedback.current_position 
        self.get_logger().info(f'feedback -> current_position: {current_position}')

    def _cancel_move_callback(self, msg):
        self.cancel_goal()

    def cancel_goal(self):
        if self._goal_handle is not None:
            self.get_logger().info('sending the cancel goal request')
            self._goal_handle.cancel_goal_async()



        
def main(args=None):
    rclpy.init(args=args)
    node = MoveRobotClientNode()  
    node.send_goal(51, 3) 
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()