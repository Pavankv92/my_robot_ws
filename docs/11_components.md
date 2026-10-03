# Components

Code: [`src/components_py`](../src/components_py)

**Composition** means running several nodes in **one process** instead of one process per node.

## When to use

- **Many small nodes:** fewer processes, less memory and start-up time.
- **Large data between nodes** (images, point clouds): in C++, nodes in the same process can pass messages **without copying** (intra-process communication).

For a handful of nodes passing small messages, separate processes are fine and easier to debug.

## Python: manual composition

Python has no component containers. You compose by hand: create the nodes and add them to one executor.

```python
rclpy.init()
node_1 = Node1()
node_2 = Node2()

executor = SingleThreadedExecutor()   # or MultiThreadedExecutor
executor.add_node(node_1)
executor.add_node(node_2)
executor.spin()
```

See `manual_composition.py`.

## C++: components

In C++, a node can be built as a **component** (a plugin) and loaded into a running **container** process, at runtime or from a launch file. Runtime composition is only available in C++.

```bash
ros2 run rclcpp_components component_container              # start an empty container
ros2 component types                                         # list available components
ros2 component load /ComponentManager <pkg> <pkg>::<Class>   # load one into the container
ros2 component list                                          # what's loaded where
```

In launch files, use `ComposableNodeContainer` with `ComposableNode` entries.

## Gotchas

- All nodes in a process share one executor. A slow callback in one node can delay the others (see [09_executors.md](09_executors.md)).
- If one node crashes, the whole process, and every node in it, goes down.

## See also

[09_executors.md](09_executors.md)
