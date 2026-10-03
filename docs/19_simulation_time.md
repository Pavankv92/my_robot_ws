# Simulation Time (`use_sim_time`)

In simulation, **Gazebo's clock** is the true time, not the PC's wall clock. Gazebo can run slower or faster than real time, and it pauses.

- Gazebo publishes its time on **`/clock`**.
- Every node started with **`use_sim_time:=true`** uses `/clock` instead of the wall clock.

## When

| Running | `use_sim_time` |
|---|---|
| Gazebo simulation | `true` for **every** node: `robot_state_publisher`, RViz, controllers, your own nodes |
| Real robot | `false` (the default) |
| Replaying a bag with `--clock` | `true` (see [20_ros2_bag.md](20_ros2_bag.md)) |

## How

**1. Bridge `/clock` from Gazebo.** Add this to the bridge YAML (e.g. `my_robot_bringup/config/gazebo_bridge.yaml`):

```yaml
- ros_topic_name: "/clock"
  gz_topic_name: "/clock"
  ros_type_name: "rosgraph_msgs/msg/Clock"
  gz_type_name: "gz.msgs.Clock"
  direction: GZ_TO_ROS
```

**2. Set the parameter on the nodes.**

Single node:

```bash
ros2 run <pkg_name> <node_name> --ros-args -p use_sim_time:=true
```

Launch file (XML), per node:

```xml
<node pkg="robot_state_publisher" exec="robot_state_publisher">
    <param name="use_sim_time" value="true" />
</node>
```

Launch file (Python), for **all** nodes that follow:

```python
from launch_ros.actions import SetParameter
SetParameter(name='use_sim_time', value=True)
```

## In code

Always take time from the node, never from Python's `time` module, so it works in both simulation and reality:

```python
now = self.get_clock().now()          # ✅ sim time or wall time, depending on use_sim_time
msg.header.stamp = now.to_msg()
```

## Gotchas

| Symptom | Cause |
|---|---|
| TF "extrapolation into the future/past", RViz drops messages | Some nodes use sim time, others wall time. Set it on **all** nodes. |
| Timers never fire, time stays at 0 | `use_sim_time:=true`, but nothing publishes `/clock` (bridge missing, or Gazebo paused) |
| Robot model in RViz jumps or lags | Same as the first row; check `ros2 param get /node use_sim_time` on each node |

## See also

[14_tf2.md](14_tf2.md) · [13_urdf_and_xacro.md](13_urdf_and_xacro.md)
