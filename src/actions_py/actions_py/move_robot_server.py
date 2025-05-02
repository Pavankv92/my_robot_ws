import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle, GoalResponse, CancelResponse
from my_robot_interfaces.action import MoveRobot
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from std_msgs.msg import String
from threading import Lock
import time

class MoveRobotServerNode(Node):
    def __init__(self):
        super().__init__('move_robot_server')
        self._robot_position = 50

        self._goal_handle : ServerGoalHandle = None
        self._goal_handle_lock = Lock()
        self._goal_queue = []

        self._move_robot_server = ActionServer(
            self, 
            MoveRobot, 
            'move_robot',
            goal_callback=self._on_goal_request,
            cancel_callback=self._on_goal_cancel,
            execute_callback=self._on_goal_execute,
            callback_group=ReentrantCallbackGroup())
        
        self.get_logger().info("Move Robot action server has been started")
        self.get_logger().info(f"robot position: {self._robot_position}")
       
    def _on_goal_request(self, goal_request: MoveRobot.Goal) -> GoalResponse:
        self.get_logger().info("Received a goal")
        
        # # goal policy : refuse the new goal if the current goal is active.
        # with self._goal_handle_lock:
        #     if self._goal_handle is not None and self._goal_handle.is_active:
        #         self.get_logger().info("A goal is still active, Rejecting the goal")
        #         return GoalResponse.REJECT
        
        # validate the requested the goal
        if goal_request.position not in range(0, 100) or goal_request.velocity <=0:
            self.get_logger().info("Invalid Position or velocity, Rejecting the goal")
            return GoalResponse.REJECT
        else: 
            # Goal policy : scrap the current goal if the validated new goal comes in while executing the current one.
            with self._goal_handle_lock:
                if self._goal_handle is not None and self._goal_handle.is_active:
                    self.get_logger().info("New goal received while executing the current one. Srcapping the current one.")
                    self._goal_handle.abort()

            self.get_logger().info("Accepted the goal")
            return GoalResponse.ACCEPT

    
    def _on_goal_execute(self, goal_handle : ServerGoalHandle) -> MoveRobot.Result:

        with self._goal_handle_lock:
            self._goal_handle = goal_handle
        
        #objects
        feedback = MoveRobot.Feedback()
        result = MoveRobot.Result()

        goal_position = goal_handle.request.position
        goal_velocity = goal_handle.request.velocity
        self.get_logger().info(f"received goal position: {goal_position}")
        self.get_logger().info(f"received goal velocity: {goal_velocity}")
        self.get_logger().info("executing...")

        while rclpy.ok(): # infinite loop, rclpy.ok() returns False when cmd: ctrl+c
            # check if the goal is aborted
            if not goal_handle.is_active:
                result.position = self._robot_position
                result.message = "current goal is aborted and replaced by a new goal"
                return result
            
            # check if the goal is cancelled
            if goal_handle.is_cancel_requested:
                result.position = self._robot_position
                if goal_position == self._robot_position :
                    result.message = "Success even though goal is canelled"
                    goal_handle.succeed()
                else:
                    result.message = "Cancelled"
                    goal_handle.canceled()
                    self.get_logger().info("cancelled the goal!")

                return result

            
            diff = goal_position - self._robot_position

            if diff == 0:
                # reached the goal
                result.position = self._robot_position
                result.message = "Success"
                goal_handle.succeed()
                return result

            elif diff > 0:
                if diff >= goal_velocity:
                    self._robot_position += goal_velocity
                else :
                    self._robot_position += diff

            else:
                if abs(diff) >= goal_velocity:
                    self._robot_position -= goal_velocity
                else :
                    self._robot_position -= abs(diff)

            # feedback
            feedback.current_position = self._robot_position
            goal_handle.publish_feedback(feedback=feedback)
            self.get_logger().info(f"robot position: {self._robot_position}")


            time.sleep(1.0)

    def _on_goal_cancel(self, goal_handle: ServerGoalHandle) -> CancelResponse:
        self.get_logger().info("Received a cancel request")
        self.get_logger().info("cancel request is accepted!")
        return CancelResponse.ACCEPT # accept : accept the cancel request, reject : well! reject the cancel request
    
def main(args=None):
    rclpy.init(args=args)
    node = MoveRobotServerNode()   
    rclpy.spin(node, MultiThreadedExecutor())
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()