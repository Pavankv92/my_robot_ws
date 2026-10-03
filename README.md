# my_robot_ws: ROS 2 from Basics to Advanced

My ROS 2 learning workspace: example packages for each core concept, a simulated differential-drive robot in Gazebo, and notes written along the way.

- **ROS 2:** Jazzy (Ubuntu 24.04)
- **Language:** Python (`rclpy`), plus CMake packages for interfaces, URDF and launch files
- **Simulator:** Gazebo (`ros_gz_sim`)

---

## Contents

| Package | Concept | Executables |
|---|---|---|
| [`my_py_pkg`](src/my_py_pkg) | Nodes, publishers, subscribers, parameters | `first_node`, `my_publisher`, `my_subscriber`, `hardware_status_publisher`, `number_publisher`, `param_publisher` |
| [`services_py`](src/services_py) | Service servers and clients | `add_two_ints_server`, `add_two_ints_client`, `add_two_ints_client_no_oop` |
| [`actions_py`](src/actions_py) | Action servers and clients | `count_until_server`, `count_until_client`, `move_robot_server`, `move_robot_client` |
| [`my_robot_interfaces`](src/my_robot_interfaces) | Custom interfaces | msg `HardwareStatus` · srv `EulerToQuaternion`, `QuaternionToEuler`, `GoHomePosition` · action `CountUntil`, `MoveRobot` |
| [`executor_py`](src/executor_py) | Single- and multi-threaded executors, callback groups | `single_threaded_executor`, `multi_threaded_executor`, `multiple_nodes_in_executor`, `multiple_nodes_in_multithreaded_executor`, `number_publisher_with_executor` |
| [`lifecycle_py`](src/lifecycle_py) | Lifecycle (managed) nodes | `number_publisher_lifecycle`, `lifecycle_node_manager` |
| [`components_py`](src/components_py) | Composing several nodes in one process | `manual_composition` |
| [`my_robot_utils`](src/my_robot_utils) | Python and C++ in one `ament_cmake` package | `angle_conversion_server.py` |
| [`my_ctk_pkg`](src/my_ctk_pkg) | A Tkinter GUI running alongside a ROS node | `number_publisher` |
| [`my_robot_description`](src/my_robot_description) | URDF/xacro of a differential-drive robot, with Gazebo plugins | launch: `display.launch.xml` / `.py` |
| [`my_robot_bringup`](src/my_robot_bringup) | Gazebo simulation, ROS–Gazebo bridge, lifecycle demo | launch: `my_robot_gazebo.launch.xml`, `lifecycle_test.launch.xml` / `.py` |

---

## Notes

Notes in learning order, in [`docs/`](docs):

| # | Topic | # | Topic |
|---|---|---|---|
| 01 | [Workspace and build](docs/01_workspace_and_build.md) | 12 | [Creating packages: Python, C++, both, external libraries](docs/12_creating_packages.md) |
| 02 | [Nodes and topics](docs/02_nodes_and_topics.md) | 13 | [URDF and xacro](docs/13_urdf_and_xacro.md) |
| 03 | [Communication overview](docs/03_communication_overview.md) | 14 | [TF2](docs/14_tf2.md) |
| 04 | [Services](docs/04_services.md) | 15 | [ros2_control](docs/15_ros2_control.md) |
| 05 | [Actions](docs/05_actions.md) | 16 | [rqt](docs/16_rqt.md) |
| 06 | [Custom interfaces](docs/06_custom_interfaces.md) | 17 | [Debugging](docs/17_debugging.md) |
| 07 | [Parameters](docs/07_parameters.md) | 18 | [Quality of Service (QoS)](docs/18_qos.md) |
| 08 | [Launch files](docs/08_launch_files.md) | 19 | [Simulation time (`use_sim_time`)](docs/19_simulation_time.md) |
| 09 | [Executors](docs/09_executors.md) | 20 | [ros2 bag](docs/20_ros2_bag.md) |
| 10 | [Lifecycle nodes](docs/10_lifecycle_nodes.md) | 21 | [C++ basics (rclcpp)](docs/21_cpp_basics.md) |
| 11 | [Components](docs/11_components.md) | | |

Each note follows the same shape: **when** to use it, the **commands**, minimal **code**, **gotchas**, and **see also** links.

---

## Setup

```bash
# 1. Clone (the repository is the whole workspace)
git clone https://github.com/Pavankv92/my_robot_ws.git ~/my_robot_ws
cd ~/my_robot_ws

# 2. Install common tools (xacro, colcon, rqt, rviz2, ...)
bash scripts/install_basic_packages.sh jazzy

# 3. Install the packages' dependencies
rosdep install --from-paths src --ignore-src -y

# 4. Build
colcon build --symlink-install
source install/setup.bash
```

---

## Try it

```bash
# Publisher / subscriber
ros2 run my_py_pkg my_publisher
ros2 run my_py_pkg my_subscriber

# Service
ros2 run services_py add_two_ints_server
ros2 run services_py add_two_ints_client

# Action
ros2 run actions_py count_until_server
ros2 run actions_py count_until_client

# Lifecycle node + manager
ros2 launch my_robot_bringup lifecycle_test.launch.xml

# Robot model in RViz (with joint sliders)
ros2 launch my_robot_description display.launch.xml

# Robot in Gazebo, drive it with /cmd_vel
ros2 launch my_robot_bringup my_robot_gazebo.launch.xml
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
