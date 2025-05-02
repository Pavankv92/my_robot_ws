from launch import LaunchDescription
from launch_ros.actions import LifecycleNode

def generate_launch_description():

    number_node = LifecycleNode(
        package = "my_py_pkg",
        executable = "number_publisher_lifecycle",
        name = "number_publisher_lifecycle",
        namespace=""
    )

    lifecycle_node_manager = LifecycleNode(
        package = "my_py_pkg",
        executable = "lifecycle_node_manager",
        name = "lifecycle_node_manager",
        namespace=""
    )

    return LaunchDescription([
        number_node,
        lifecycle_node_manager
    ])