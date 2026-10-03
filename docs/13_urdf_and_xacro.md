# URDF and Xacro

Code: [`src/my_robot_description`](../src/my_robot_description)

## URDF

URDF is the physical description of a robot.

| Used by | Needs |
|---|---|
| RViz | `<visual>` tags |
| Gazebo | `<collision>` and `<inertial>` tags as well |

- The `origin` in a `<visual>` tag is the position of the link's own geometry, relative to the link's frame.
- The `origin` in a `<joint>` tag is the transform between two links (parent → child).
- **Workflow:** set the visual origins to zero first → adjust the joints/transforms → go back and adjust the visuals.

### Visualise a URDF model

```bash
sudo apt install ros-<distro>-urdf-tutorial
ros2 launch urdf_tutorial display.launch.py model:=my_robot.urdf
```

### Create a PDF of the TF tree

```bash
sudo apt install ros-<distro>-tf2-tools
ros2 run tf2_tools view_frames      # while /tf is being published
```

## TF

The relative transforms between the robot's links. To check the transform between two frames:

```bash
ros2 run tf2_ros tf2_echo base_link second_link
```

## Nodes

### `robot_state_publisher`

Inputs:
1. The URDF, as the `robot_description` parameter.
2. Current joint values on `/joint_states`, which come from one of:
   - encoders on the real robot
   - a Gazebo simulation
   - a fake source, `joint_state_publisher_gui`:
     ```bash
     sudo apt install ros-<distro>-joint-state-publisher-gui
     ros2 run joint_state_publisher_gui joint_state_publisher_gui
     ```
     It reads `/robot_description`, shows a slider per joint, and publishes `/joint_states`.

Output: `/tf`.

### RViz

Visualises `/tf` and `/robot_description`.

## Xacro

Xacro adds variables and functions to URDF, for parametric designs.

Property (variable):

```xml
<xacro:property name="wheel_radius" value="0.1" />
```

Macro (function):

```xml
<xacro:macro name="dummy_macro" params="a b c">
    ${a}
</xacro:macro>
```

Generate a plain URDF from a xacro file:

```bash
xacro file_name.xacro
```

## Gazebo

```bash
ros2 launch ros_gz_sim gz_sim.launch.py
```
