from launch import LaunchDescription
from launch_ros.actions import LifecycleNode

def generate_launch_description():

    number_node = LifecycleNode(
        package = "lifecycle_py",
        executable = "number_publisher_lifecycle",
        name = "number_publisher_lifecycle",
        namespace=""
    )

    lifecycle_node_manager = LifecycleNode(
        package = "lifecycle_py",
        executable = "lifecycle_node_manager",
        name = "lifecycle_node_manager",
        namespace=""
    )

    return LaunchDescription([
        number_node,
        lifecycle_node_manager
    ])