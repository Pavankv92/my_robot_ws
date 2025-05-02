import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
import threading
import tkinter as tk
import time
from .application import Application


class NumberPublisherNode(Node):
    def __init__(self):
        super().__init__('number_publisher')
        self._number = 1
        self._publish_frequency = 1.0
        self._pub = self.create_publisher(Int64, 'number', 10)
        self.get_logger().info("Number publisher has been started")

    def publish_custom_number(self, number):
        try:
            value = int(number)
        except ValueError:
            self.get_logger().warn("Invalid number input")
            return
        msg = Int64()
        msg.data = value
        self._pub.publish(msg)
        self.get_logger().info(f"Published from GUI: {msg.data}")

def create_gui(node):
    app = Application(node)
    app.mainloop()

def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisherNode()

    gui_thread = threading.Thread(target=create_gui, args=(node,), daemon=True)
    gui_thread.start()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
