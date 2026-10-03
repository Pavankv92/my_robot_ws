# Debugging

## Tools

- `rqt_graph` and the many other rqt plugins (see [16_rqt.md](16_rqt.md))
- Log messages: `rqt_console`
- `ros2 doctor`

## `ros2 doctor`

- With no nodes running, it checks the ROS 2 installation itself.
- With nodes running, it checks the nodes as well as the system.

```bash
ros2 doctor
ros2 doctor --report              # print all reports
ros2 doctor --report-failed       # only the failed checks
ros2 doctor --include-warnings    # treat warnings as failures
ros2 doctor hello                 # check network connectivity between hosts
```

Save the report to a file:

```bash
ros2 doctor --report > report.txt
```

## Common problems

| Symptom | First thing to check |
|---|---|
| `ros2 run`: "No executable found" | Rebuilt and **re-sourced** `install/setup.bash`? Entry point in `setup.py` / `install(TARGETS ...)` in CMake? |
| `ros2 launch`: file not found | Launch folder installed into `share` in `CMakeLists.txt`? ([08_launch_files.md](08_launch_files.md)) |
| Subscriber receives nothing | Topic name/namespace (`ros2 topic list`), then QoS (`ros2 topic info -v`, [18_qos.md](18_qos.md)) |
| Node doesn't see a parameter | Declared in the node? Correct node name in the YAML? ([07_parameters.md](07_parameters.md)) |
| TF / RViz errors in Gazebo | `use_sim_time` on every node ([19_simulation_time.md](19_simulation_time.md)) |
| A callback never runs / node freezes | Executor deadlock or starvation ([09_executors.md](09_executors.md)) |

See also the debugging checklist in [02_nodes_and_topics.md](02_nodes_and_topics.md#debugging).
