import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle, GoalResponse, CancelResponse
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
import time
import threading
from my_robot_interfaces.action import CountUntil



class CountUntilServerNode(Node):
    def __init__(self):
        super().__init__('count_until_server')

        self._goal_handle : ServerGoalHandle = None
        self._goal_handle_lock = threading.Lock()
        self._goal_queue = []

        self._count_until_server = ActionServer(
            self, 
            CountUntil, 
            'count_until', 
            goal_callback=self._on_goal_request, # if this returns ACCEPT, execute --> execute_callback
            handle_accepted_callback= self._handle_accepted_goals,
            cancel_callback=self._on_cancel,
            execute_callback=self._on_execute,
            callback_group=ReentrantCallbackGroup() # several callbacks can be run at the same time
            )
        self.get_logger().info("count_until_action_server has been started")

    def _on_goal_request(self, goal_request: CountUntil.Goal) -> GoalResponse:
        self.get_logger().info("Received a goal")
        
        # # goal policy : refuse the new goal if the current goal is active.
        # with self._goal_handle_lock:
        #     if self._goal_handle is not None and self._goal_handle.is_active:
        #         self.get_logger().info("A goal is still active, Rejecting the goal")
        #         return GoalResponse.REJECT
        
        # validate the requested the goal
        if goal_request.target_number <= 0:
            self.get_logger().info("Rejecting the goal")
            return GoalResponse.REJECT
        else: 
            # # Goal policy : scrap the current goal if the validated new goal comes in while executing the current one.
            # with self._goal_handle_lock:
            #     if self._goal_handle is not None and self._goal_handle.is_active:
            #         self.get_logger().info("New goal received while executing the current one. Srcapping the current one.")
            #         self._goal_handle.abort()

            self.get_logger().info("Accepted the goal")
            return GoalResponse.ACCEPT

    def _handle_accepted_goals(self, goal_handle: ServerGoalHandle):
        with self._goal_handle_lock:
            if self._goal_handle is not None:
                # for the second goal onwards=, self._goal_handle is goal_handle. Just add it to the queue
                self._goal_queue.append(goal_handle)
            else:
                goal_handle.execute() # calls self._on_execute() for the first goal
    
    def _on_cancel(self, goal_handle: ServerGoalHandle) -> CancelResponse:
        self.get_logger().info("Received a cancel request")
        self.get_logger().info("cancel request is accepted!")
        return CancelResponse.ACCEPT # accept : accept the cancel request, reject : well! reject the cancel request

    def _process_next_goal_in_queue(self):
        with self._goal_handle_lock:
            if len(self._goal_queue) > 0:
                current_goal_handle = self._goal_queue[0]
                self._goal_queue.pop(0)
                current_goal_handle.execute() # calls the fucntion defined in the execute_callback --> self._on_execute()
            else:
                self._goal_handle = None
                
            
    
    def _on_execute(self, goal_handle: ServerGoalHandle) -> CountUntil.Result: # goal_handle will be added automatically
        
        with self._goal_handle_lock:
            self._goal_handle = goal_handle
        
        # get the goals
        # self.get_logger().info("Getting goals")
        self._target_number = goal_handle.request.target_number
        self._period = goal_handle.request.period

        # objects
        feedback = CountUntil.Feedback()
        result = CountUntil.Result()
        # execute the goals and send feedback while executing
        self.get_logger().info("Executing...")

        counter = 0
        for i in range(self._target_number):
            # check if the current goal handle is aborted. If yes, return the result
            if not goal_handle.is_active:
                result.reached_number = counter
                self._process_next_goal_in_queue()
                return result
            
            # check for cancel request
            if goal_handle.is_cancel_requested:
                self.get_logger().info("canceling the goal")
                goal_handle.canceled()
                result.reached_number = counter
                self._process_next_goal_in_queue()

                return result

            counter +=1
            self.get_logger().info(f"counter: {counter}")
            
            # feedback
            feedback.current_number = counter
            goal_handle.publish_feedback(feedback)
            
            time.sleep(self._period)

        # once done with the execution, set the final goal state (suceeded, aborted)
        goal_handle.succeed()

        # publish the Result
        result.reached_number = counter
        self._process_next_goal_in_queue()

        return result 
            


def main(args=None):
    rclpy.init(args=args)
    node = CountUntilServerNode()   
    # entire _on_execute will run in a single thread, hence this node will not recognise cancel goal until the _on_execute is completed.
    # run the node in the multiple thread
    rclpy.spin(node, MultiThreadedExecutor()) 
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()