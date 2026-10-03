# Nodes and Topics

## Run a node

```bash
ros2 run <pkg_name> <node_name>
ros2 run <pkg_name> <node_name> --ros-args ...
```

## Nodes

```bash
ros2 node list
ros2 node info /node_name
```

### Rename at runtime

Launch the same node under a different name or namespace. `--remap` and `-r` are equivalent.

```bash
ros2 run <pkg_name> <node_name> --ros-args --remap __node:=new_node_name
ros2 run <pkg_name> <node_name> --ros-args --remap __ns:=/new_namespace
```

## Topics

```bash
ros2 topic list
ros2 topic echo /topic_name
ros2 topic pub /topic_name <msg_type> "<data>"
ros2 topic info /topic_name
ros2 topic hz /topic_name
```

### Remap a topic

```bash
ros2 run <pkg_name> <node_name> --ros-args -r topic_name:=new_topic_name
```

### Rename node and topic together

```bash
ros2 run <pkg_name> <node_name> --ros-args -r __node:=new_node_name -r topic_name:=new_topic_name
```

## rqt

```bash
rqt_graph
```

## Debugging

Problems can be frustrating, especially with several nodes running. Work through these:

1. `topic list`, `node list`, `info`, `echo`, `pub`
2. Remappings: renamed nodes and topics
3. `ros2 interface show`
4. `rqt_graph`

## Leading slash in topic names

| In the node | Result |
|---|---|
| `self.create_publisher(String, '/my_topic', 10)` (**with** leading slash) | The topic is absolute. The node's namespace is **not** added. |
| `self.create_publisher(String, 'my_topic', 10)` (**without** leading slash) | The topic is relative. The leading slash and the node's namespace **are** added automatically. |

**Recommendation:** don't put a leading slash in topic names inside the node. The namespace is then added automatically, so the topic name stays flexible and consistent with the node's namespace.

## See also

[03_communication_overview.md](03_communication_overview.md) · [18_qos.md](18_qos.md) (subscriber receives nothing?) · [16_rqt.md](16_rqt.md)
