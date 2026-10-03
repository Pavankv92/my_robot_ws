# Launch Files

## XML

```xml
<node pkg="pkg_name" exec="executable_name" name="new_node_name">
    <remap from="old_topic_name" to="new_topic_name" />
    <param name="param_name" value="value" />
</node>
```

With a namespace:

```xml
<node pkg="pkg_name" exec="executable_name" name="new_node_name" namespace="/new_namespace">
    <remap from="old_topic_name" to="new_topic_name" />
    <param name="param_name" value="value" />
</node>
```

## Python

`Node(...)` arguments:

```python
remappings=[('old_topic_name', 'new_topic_name')]   # list of tuples
parameters=[{'param_name': value}]                  # list of dicts
parameters=['path/to/config_file.yaml']             # or a list of YAML files
namespace='/new_namespace'
```

## Parameters / config

Put them in a YAML file (see [07_parameters.md](07_parameters.md)).

## Namespaces

Prefix with `/new_namespace`.

## Launch arguments

Declare a launch argument to pass values on the command line:

```python
turtlesim_ns_launch_arg = DeclareLaunchArgument(
    'turtlesim_ns',
    default_value='turtlesim1'
)

turtlesim_node = Node(
    package='turtlesim',
    namespace=LaunchConfiguration('turtlesim_ns'),
    executable='turtlesim_node',
    name='sim'
)
```

Use `LaunchConfiguration('turtlesim_ns')` to read the value of a declared argument.

Show the available arguments:

```bash
ros2 launch launch_tutorial example_substitutions_launch.py --show-args
```
```
Arguments (pass arguments as '<name>:=<value>'):

    'turtlesim_ns':
        no description given
        (default: 'turtlesim1')
```

Launch with a value:

```bash
ros2 launch launch_tutorial example_substitutions_launch.py turtlesim_ns:='turtlesim3'
```

## `CMakeLists.txt`

Every directory you create in a package that should be found at runtime (launch files, URDF, config) must be installed into `share`:

```cmake
install(
  DIRECTORY urdf launch
  DESTINATION share/${PROJECT_NAME}/
)
```

`ros2 launch` only finds launch files that are installed in `share`.

## `package.xml`

```xml
<exec_depend>ros2launch</exec_depend>
```
