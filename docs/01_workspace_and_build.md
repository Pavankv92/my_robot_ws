# Workspace and Build

## Sourcing

| What | Command |
|---|---|
| Underlay (ROS 2 itself) | `source /opt/ros/<distro>/setup.bash` |
| Overlay (your workspace) | `source ~/my_robot_ws/install/setup.bash` |
| Tab completion for colcon | `source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash` |

## Create a package

```bash
ros2 pkg create --build-type ament_python <pkg_name>
ros2 pkg create --build-type ament_cmake <pkg_name>
```

What goes into `package.xml`, `setup.py` and `CMakeLists.txt` for each kind of package: [12_creating_packages.md](12_creating_packages.md).

## Build

The build installs the executables into the `install/` directory. For Python packages, the install location is defined in `setup.cfg`.

Always build from the workspace root (`~/my_robot_ws`), never from `src/`.

```bash
colcon build
colcon build --packages-select <pkg_name>
colcon build --symlink-install
```

## Naming

Keep the same name for the file name, node name and executable name.

## Passing arguments on the command line

| What | Syntax |
|---|---|
| Any ROS argument | `--ros-args ...` |
| A parameter | `--ros-args -p param_name:=value` |
