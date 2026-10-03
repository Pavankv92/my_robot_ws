# Custom Interfaces

## Inspect interfaces

```bash
ros2 interface list
ros2 interface show std_msgs/msg/String
ros2 interface show <pkg_name>/srv/CustomService
ros2 interface show <pkg_name>/action/CustomAction
```

## Create custom interfaces

Naming convention: CamelCase, e.g. `HardwareStatus.msg`.

## Build custom interfaces

### `package.xml`

Add:

```xml
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

**If there are errors**, remove:

```xml
<test_depend>ament_lint_auto</test_depend>
<test_depend>ament_lint_common</test_depend>
```

### `CMakeLists.txt`

Add:

```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Num.msg"
  "msg/Sphere.msg"
  "srv/AddThreeInts.srv"
  DEPENDENCIES geometry_msgs  # packages the messages above depend on
)

ament_export_dependencies(rosidl_default_runtime)
```

## Use custom interfaces

Add the interface package as a dependency of the package that uses it.
