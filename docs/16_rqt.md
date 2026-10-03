# rqt

rqt is a GUI with plugins for looking inside a running ROS system.

## Install

```bash
sudo apt install '~nros-jazzy-rqt*'
```

## Start

```bash
rqt                       # empty window, add plugins from the Plugins menu
rqt --force-discover      # if newly installed plugins don't show up
```

## Most useful plugins

| Plugin (menu) | Use it to | Standalone command |
|---|---|---|
| Introspection → **Node Graph** | See nodes and topics and how they connect | `rqt_graph` |
| Topics → **Topic Monitor** | See every topic, its rate and its latest value | |
| Topics → **Message Publisher** | Publish test messages by hand | |
| Services → **Service Caller** | Call a service by hand | |
| Configuration → **Parameter Reconfigure** | Change a node's parameters live | |
| Visualization → **Plot** | Plot numeric fields over time, e.g. `/joint_states/position[0]` | `ros2 run rqt_plot rqt_plot` |
| Visualization → **TF Tree** | See the TF tree live (install `ros-jazzy-rqt-tf-tree` first) | `ros2 run rqt_tf_tree rqt_tf_tree` |
| Logging → **Console** | Filter and read log messages from all nodes | `ros2 run rqt_console rqt_console` |

## Log levels

Start a node with a different log level:

```bash
ros2 run <pkg_name> <node_name> --ros-args --log-level WARN
```

Levels: `DEBUG` < `INFO` (default) < `WARN` < `ERROR` < `FATAL`.

## See also

[17_debugging.md](17_debugging.md)
