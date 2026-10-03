# Parameters

Parameters are runtime settings for a node. Each node keeps its own set of parameters.

**When:** configuration values that change between runs or robots, but not every cycle: rates, gains, names, limits, file paths. Not for data (use topics).

## Command line

```bash
ros2 param list
ros2 param get <node_name> <param_name>
ros2 param set <node_name> <param_name> <value>
```

Dump all parameters of a node:

```bash
ros2 param dump <node_name>                     # to the screen
ros2 param dump <node_name> > file_name.yaml    # to a file
ros2 param load <node_name> file_name.yaml      # load them back
```

Pass parameters when starting a node:

```bash
ros2 run <pkg_name> <node_name> --ros-args -p param_name:=value
ros2 run <pkg_name> <node_name> --ros-args --params-file file_name.yaml
```

## In the node

```python
self.declare_parameter(...)
self.get_parameter(...)
self.add_post_set_parameters_callback(...)
```

### How does a node keep track of parameter changes?

Register a callback with `add_post_set_parameters_callback()`. It's called after parameters are changed.

## Services created automatically

ROS 2 automatically adds parameter service servers to every node:

```
/param_publisher/describe_parameters
/param_publisher/get_parameter_types
/param_publisher/get_parameters
/param_publisher/get_type_description
/param_publisher/list_parameters
/param_publisher/set_parameters
/param_publisher/set_parameters_atomically
```

## YAML file

```yaml
/namespace/node_name:
  ros__parameters:
    number: 8
    timer_period: 0.5
```

Wildcard: `/**` matches all nodes.

## Gotcha

A parameter must be **declared** (`declare_parameter`) before it can be read or set. Setting an undeclared parameter from the command line or YAML is silently ignored, or fails with "parameter not declared".

## See also

[08_launch_files.md](08_launch_files.md) (passing parameters from launch files) · [19_simulation_time.md](19_simulation_time.md) (`use_sim_time`)
