#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import EulerToQuaternion, QuaternionToEuler
from tf_transformations import quaternion_from_euler, euler_from_quaternion

class AngleConversionServer(Node):
    def __init__(self):
        super().__init__('angle_conversion_server')
        self._euler_to_quaternion = self.create_service(EulerToQuaternion, 'euler_to_quaternion', self.callback_euler_to_quaternion)
        self._quaternion_to_euler = self.create_service(QuaternionToEuler, 'quaternion_to_euler', self.callback_quaternion_to_euler)

        self.get_logger().info("Angle conversion services has been started...")

    def callback_euler_to_quaternion(self, request : EulerToQuaternion.Request, response : EulerToQuaternion.Response) -> EulerToQuaternion.Response:
        response = EulerToQuaternion.Response()
        (response.x, response.y, response.z, response.w) = quaternion_from_euler(request.roll, request.pitch, request.yaw)
        return response
    
    def callback_quaternion_to_euler(self, request : QuaternionToEuler.Request, response : QuaternionToEuler.Response) -> QuaternionToEuler.Response:
        response = QuaternionToEuler.Response()

        (response.roll, response.pitch, response.yaw) = euler_from_quaternion([request.x, request.y, request.z, request.w])
        
        return response

def main(args=None):
    rclpy.init(args=args)
    node = AngleConversionServer()   
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()