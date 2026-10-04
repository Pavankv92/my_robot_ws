# CMakeLists.txt and package.xml Explained

What every line in these two files means, and how to choose between the options that look alike.

**New to this?** Start with [00_what_the_hell_is_cmakelists.md](00_what_the_hell_is_cmakelists.md): how C++ code is organised, why there's a build step, what libraries (`.a`, `.so`) and Makefiles are, and where everything goes after building.

For ready-to-copy templates per package type (Python, C++, both, external libraries), see [12_creating_packages.md](12_creating_packages.md).

The C++ examples come from the ST3215 servo project (the `scservo_sdk`, `st3215_servo` and `my_robot_hardware` packages), which adds ros2_control with real motors to this robot.

- **Part 1:** `package.xml`, tag by tag.
- **Part 2:** `CMakeLists.txt`, line by line.

> **In short**
> - **`package.xml`** says what a package **needs**. **`CMakeLists.txt`** says how to **build** it and where to **install** it.
> - They must agree: almost every `<depend>` has a matching `find_package()`.

---

## The two files in one sentence each

| File | Answers | Read by |
|---|---|---|
| **`package.xml`** | "What is this package, and **what does it need**?" | colcon (build order), rosdep (installing dependencies), `ros2 pkg` |
| **`CMakeLists.txt`** | "**How** do I build it, and **where** do the results go?" | CMake, through colcon |

They must agree: almost every dependency appears **in both**, as a `<depend>` in `package.xml` and a `find_package()` in `CMakeLists.txt`.

```
package.xml                         CMakeLists.txt
<depend>rclcpp</depend>   ◀──────▶  find_package(rclcpp REQUIRED)
                                    target_link_libraries(my_node rclcpp::rclcpp)
```

---

# Part 1: package.xml

## Annotated example

```xml
<?xml version="1.0"?>
<package format="3">                              <!-- format 3 = current ROS 2 schema -->
  <name>my_robot_hardware</name>                  <!-- = folder name = project() in CMake -->
  <version>0.0.0</version>
  <description>What this package does</description>
  <maintainer email="you@example.com">Your Name</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend> <!-- the build system itself -->

  <depend>rclcpp</depend>                           <!-- needed to build AND to run -->
  <depend>hardware_interface</depend>
  <exec_depend>robot_state_publisher</exec_depend>  <!-- only needed at runtime -->

  <test_depend>ament_lint_auto</test_depend>        <!-- only for tests -->

  <export>
    <build_type>ament_cmake</build_type>            <!-- ament_cmake or ament_python -->
  </export>
</package>
```

## The dependency tags

| Tag | Needed when… | Use it for |
|---|---|---|
| `<buildtool_depend>` | the build **tool** runs | `ament_cmake`, `ament_cmake_python`, `rosidl_default_generators` |
| `<depend>` | **building and running** (= the three below combined) | ✅ **The default choice.** Anything you `find_package()` and link against: `rclcpp`, `hardware_interface`, your SDK |
| `<build_depend>` | building only | Rare: a header-only tool used only at compile time |
| `<build_export_depend>` | **packages that build against yours** need it too | Rare on its own; included in `<depend>` |
| `<exec_depend>` | **running** only | Things you don't compile against: nodes started from your launch files (`robot_state_publisher`, `rviz2`), plugins loaded at runtime, `ros2launch`, `xacro`, Python modules in CMake packages |
| `<test_depend>` | running tests | `ament_lint_auto`, `ament_lint_common`, `ament_cmake_gtest` |
| `<member_of_group>` | – | Interface packages only: `rosidl_interface_packages` |

**Rule of thumb:**
- You `find_package()` it in CMake → `<depend>`
- You only start it (launch file, `ros2 run`) or load it at runtime → `<exec_depend>`
- It's the build system → `<buildtool_depend>`

### What goes inside a dependency tag

A **rosdep key**, which can be one of three things:

| Kind | Example | Installed by rosdep as |
|---|---|---|
| ROS package | `rclcpp`, `hardware_interface` | `ros-jazzy-rclcpp`, ... |
| Your own workspace package | `scservo_sdk`, `my_robot_interfaces` | Nothing (built by colcon). Sets the **build order**. |
| System library | `libserial-dev`, `python3-serial`, `python3-tk` | The apt package |

`rosdep install --from-paths src --ignore-src -y` reads these tags and installs everything that's missing.

### Why `<depend>` matters even for your own packages

colcon uses the dependency tags to decide **build order**. If `st3215_servo` uses `scservo_sdk` but doesn't list it, colcon may build `st3215_servo` first, and `find_package(scservo_sdk)` fails, sometimes only on a clean build.

### Check your dependencies

```bash
colcon graph                                          # build order + who depends on whom
rosdep check --from-paths src --ignore-src            # anything missing on this PC?
rosdep install --from-paths src --ignore-src -y       # install what's missing
```

`colcon graph` for this repo (`+` = the package itself, `*` = a package that depends on it):

```
my_robot_description       +   *         ← my_robot_bringup depends on it, so it's built first
my_robot_interfaces         + * *        ← used by my_py_pkg and my_robot_utils
...
```

---

# Part 2: CMakeLists.txt

## Start small: the smallest C++ node package

The `tools_demo` example from [00_what_the_hell_is_cmakelists.md](00_what_the_hell_is_cmakelists.md#the-cmakeliststxt-for-our-example), turned into a ROS 2 package. Only the marked lines are new:

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_cpp_pkg)

find_package(ament_cmake REQUIRED)                  # NEW: ROS build helpers
find_package(rclcpp REQUIRED)                       # NEW: find the ROS C++ library

add_executable(my_node src/my_node.cpp)
target_link_libraries(my_node rclcpp::rclcpp)       # link rclcpp, like we linked "tools"

install(TARGETS my_node DESTINATION lib/${PROJECT_NAME})   # NEW: so `ros2 run` finds it

ament_package()                                     # NEW: always last
```

That's all a simple node needs. The full example below adds a library, headers, a plugin and exports.

## Annotated example

This is the real `my_robot_hardware` package from the ST3215 project: a ros2_control plugin library.

```cmake
cmake_minimum_required(VERSION 3.8)                 # (1) CMake version
project(my_robot_hardware)                          # (2) = <name> in package.xml

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)     # (3) warnings
endif()

find_package(ament_cmake REQUIRED)                  # (4) dependencies
find_package(rclcpp REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(pluginlib REQUIRED)
find_package(scservo_sdk REQUIRED)

add_library(${PROJECT_NAME} SHARED                  # (5) what to build
  src/mobile_base_hardware_interface.cpp
)
target_compile_features(${PROJECT_NAME} PUBLIC cxx_std_17)
target_include_directories(${PROJECT_NAME} PUBLIC   # (6) where headers are
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include/${PROJECT_NAME}>
)
target_link_libraries(${PROJECT_NAME} PUBLIC        # (7) what to link
  rclcpp::rclcpp
  hardware_interface::hardware_interface
  pluginlib::pluginlib
  scservo_sdk::scservo_sdk
)

pluginlib_export_plugin_description_file(           # (8) plugin registration
  hardware_interface my_robot_hardware_interface.xml)

install(DIRECTORY include/                          # (9) install
  DESTINATION include/${PROJECT_NAME})
install(TARGETS ${PROJECT_NAME}
  EXPORT export_${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin)

ament_export_targets(export_${PROJECT_NAME} HAS_LIBRARY_TARGET)   # (10) for other packages
ament_export_dependencies(rclcpp hardware_interface pluginlib scservo_sdk)

ament_package()                                     # (11) always last
```

## Line by line

### (1) `cmake_minimum_required(VERSION 3.8)`

The oldest CMake that may build this file. Leave the generated value.

### (2) `project(name)`

The name must equal `<name>` in `package.xml`. It sets `${PROJECT_NAME}`, which is used everywhere below, so renaming the package means changing only these two places.

### (3) `add_compile_options(-Wall -Wextra -Wpedantic)`

Turns on compiler warnings. **Keep it for your own code**, because warnings often point at real bugs. **Remove it for vendor code** you won't fix (e.g. `scservo_sdk`), so its warnings don't hide yours.

### (4) `find_package(<pkg> REQUIRED)`

Loads another package's CMake config, which makes its **targets** (`rclcpp::rclcpp`, ...) available. `REQUIRED` = stop with an error if it's not found.
- One `find_package` per `<depend>` you compile against.
- Fails with "Could not find a package configuration file…" → the package isn't installed, isn't built yet, or the workspace isn't sourced.

### (5) What to build: `add_executable` vs `add_library`

| Command | Builds | Use for | Installed to |
|---|---|---|---|
| `add_executable(name src/a.cpp)` | A program | Nodes, tools (`ros2 run pkg name`) | `lib/${PROJECT_NAME}` |
| `add_library(name SHARED src/a.cpp)` | A shared library `libname.so` | **Plugins** (ros2_control hardware, controllers), code shared by several packages | `lib` |
| `add_library(name STATIC src/a.cpp)` | A static library `libname.a` | Code linked into one executable. Avoid for anything that ends up in a plugin. | `lib` |
| `add_library(name INTERFACE)` | Nothing; headers only | Header-only libraries | – |

**Plugins must be `SHARED`.** ros2_control loads them at runtime with pluginlib. Everything linked **into** a shared library must be compiled with `-fPIC` (position-independent code). Shared libraries are, static ones usually aren't. That's why the vendor's static `libSCServo.a` couldn't be used and `scservo_sdk` builds a shared library instead.

### (6) `target_include_directories(target PUBLIC|PRIVATE|INTERFACE dirs)`

Where the compiler looks for `#include "..."` files.

**Visibility keywords** (also used by `target_link_libraries`):

| Keyword | The target itself uses it | Targets that link to it also get it | Use when |
|---|---|---|---|
| `PRIVATE` | ✅ | ❌ | Only your own `.cpp` files need it (typical for executables) |
| `PUBLIC` | ✅ | ✅ | Your **public headers** need it too (typical for libraries) |
| `INTERFACE` | ❌ | ✅ | Header-only libraries |

**Generator expressions:** the paths differ before and after installing:

```cmake
$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>   # while building in the workspace
$<INSTALL_INTERFACE:include/${PROJECT_NAME}>             # after install (relative to install/<pkg>/)
```

For a simple executable, `target_include_directories(my_node PRIVATE include)` is enough.

The old `include_directories(include)` (no target) applies to **everything** in the file. It works, but the per-target version is preferred.

### (7) Linking: `target_link_libraries` vs `ament_target_dependencies`

Both give your target a dependency's library **and** its include paths.

| | Example | Notes |
|---|---|---|
| **`target_link_libraries`** (modern CMake) | `target_link_libraries(my_node PUBLIC rclcpp::rclcpp)` | ✅ Preferred. Works for any CMake package, including non-ROS libraries. |
| `ament_target_dependencies` (ROS helper) | `ament_target_dependencies(my_node rclcpp example_interfaces)` | Shorter, takes **package** names. Fine in Jazzy, but being phased out in newer ROS releases. |

Target names for `target_link_libraries`:

| Dependency | Target |
|---|---|
| Most ROS packages | `<pkg>::<pkg>`, e.g. `rclcpp::rclcpp`, `pluginlib::pluginlib` |
| Message/service/action packages | `${<pkg>_TARGETS}`, e.g. `${example_interfaces_TARGETS}` |
| Your own SDK package | Whatever it exports, e.g. `scservo_sdk::scservo_sdk` |
| System library via pkg-config | `PkgConfig::<NAME>` (see [12_creating_packages.md](12_creating_packages.md#a-system-package-apt)) |

**Don't mix** the plain and keyword forms on the same target: either always `target_link_libraries(t PUBLIC ...)` / `PRIVATE`, or never.

### (8) `pluginlib_export_plugin_description_file(<base_pkg> <file.xml>)`

Only for **plugins**. It registers your plugin XML so pluginlib can find your class by name. The first argument is the package that defines the **base class**:

| Plugin type | First argument |
|---|---|
| ros2_control hardware interface | `hardware_interface` |
| ros2_control controller | `controller_interface` |

Three names must match: `<plugin>` in the URDF = `class name` in the XML = the class given to `PLUGINLIB_EXPORT_CLASS(...)` in the `.cpp`. And `library path` in the XML = the `add_library` name.

### (9) `install(...)`: where things go

Nothing is usable until it's **installed** into `install/<pkg>/`. ROS tools only look there, never in `src/`.

| What | Command | Destination | Found by |
|---|---|---|---|
| Executables | `install(TARGETS my_node DESTINATION lib/${PROJECT_NAME})` | `install/<pkg>/lib/<pkg>/` | `ros2 run <pkg> my_node` |
| Libraries / plugins | `install(TARGETS lib ... LIBRARY DESTINATION lib)` | `install/<pkg>/lib/` | the dynamic loader, pluginlib |
| Headers | `install(DIRECTORY include/ DESTINATION include/${PROJECT_NAME})` | `install/<pkg>/include/<pkg>/` | other packages' `#include` |
| Launch, config, URDF, RViz | `install(DIRECTORY launch config urdf DESTINATION share/${PROJECT_NAME}/)` | `install/<pkg>/share/<pkg>/` | `ros2 launch`, `$(find-pkg-share <pkg>)` |
| Python scripts | `install(PROGRAMS scripts/tool.py DESTINATION lib/${PROJECT_NAME})` | `install/<pkg>/lib/<pkg>/` | `ros2 run <pkg> tool.py` |
| Single files | `install(FILES lib/libvendor.so DESTINATION lib)` | where you say | – |

`install(TARGETS ...)` variants:

| Keyword | For |
|---|---|
| `LIBRARY DESTINATION lib` | Shared libraries (`.so`) |
| `ARCHIVE DESTINATION lib` | Static libraries (`.a`) |
| `RUNTIME DESTINATION bin` | Executables/DLLs (Windows); harmless on Linux |
| `EXPORT export_<name>` | Remember this target for `ament_export_targets` (10) |

**`--symlink-install`** makes installed files **links** back to `src/`, so edits to Python scripts, launch files, URDFs and YAML show up without rebuilding. C++ still needs a rebuild after every change.

### (10) Exports: for packages that use **yours**

Only needed if **another package** will `find_package()` yours, i.e. libraries. Executables-only packages can skip these.

| Command | Does |
|---|---|
| `ament_export_targets(export_<name> HAS_LIBRARY_TARGET)` | Creates `<pkg>::<target>` for other packages. `HAS_LIBRARY_TARGET` also adds `lib/` to the library path when the workspace is sourced. |
| `ament_export_dependencies(a b c)` | Packages that use yours automatically `find_package` these too. List what your **public headers** include. |
| `ament_export_include_directories(include)`, `ament_export_libraries(...)` | Older style, superseded by `ament_export_targets` |

### (11) `ament_package()`

Generates the package's CMake config and environment hooks. **Must be the last line.** Anything after it is ignored or breaks the export.

---

## Other commands you'll meet

| Command | Package type | Does | See |
|---|---|---|---|
| `rosidl_generate_interfaces(${PROJECT_NAME} "msg/X.msg" ...)` | Interface packages | Generates C++/Python code for messages, services and actions | [06_custom_interfaces.md](06_custom_interfaces.md) |
| `rosidl_get_typesupport_target(var ${PROJECT_NAME} rosidl_typesupport_cpp)` + `target_link_libraries(node "${var}")` | A package that defines **and** uses its own messages | Links a node to messages generated in the same package | |
| `ament_python_install_package(${PROJECT_NAME})` | Python inside a CMake package | Makes `import <pkg>` work | [12_creating_packages.md](12_creating_packages.md#3-python--c-in-one-package) |
| `target_compile_features(t PUBLIC cxx_std_17)` | C++ | Sets the C++ standard for this target and its users | |
| `if(BUILD_TESTING) find_package(ament_lint_auto REQUIRED) ament_lint_auto_find_test_dependencies() endif()` | Any | Runs the linters from `<test_depend>` with `colcon test`. Safe to delete if you don't use them. | |

---

## Where `package.xml` and `CMakeLists.txt` meet

| You want to… | `package.xml` | `CMakeLists.txt` |
|---|---|---|
| Use `rclcpp` in a node | `<depend>rclcpp</depend>` | `find_package(rclcpp REQUIRED)` + `target_link_libraries(node rclcpp::rclcpp)` |
| Use messages from `example_interfaces` | `<depend>example_interfaces</depend>` | `find_package(example_interfaces REQUIRED)` + `target_link_libraries(node ${example_interfaces_TARGETS})` |
| Use your own SDK package | `<depend>scservo_sdk</depend>` | `find_package(scservo_sdk REQUIRED)` + `target_link_libraries(t scservo_sdk::scservo_sdk)` |
| Use an apt library | `<depend>libserial-dev</depend>` | `pkg_check_modules(...)` + link `PkgConfig::...` |
| Start another package's node from your launch file | `<exec_depend>robot_state_publisher</exec_depend>` | nothing |
| Ship launch files | `<exec_depend>ros2launch</exec_depend>` | `install(DIRECTORY launch DESTINATION share/${PROJECT_NAME}/)` |
| Write a ros2_control plugin | `<depend>hardware_interface</depend>` `<depend>pluginlib</depend>` | `add_library(... SHARED ...)` + `pluginlib_export_plugin_description_file(hardware_interface x.xml)` |

---

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `Could not find a package configuration file provided by "X"` | `X` not installed / not built / workspace not sourced, or missing from `package.xml` (wrong build order) | `rosdep install`, build `X` first, `source install/setup.bash`, add `<depend>X</depend>` |
| `ros2 run`: "No executable found" | Missing `install(TARGETS ... DESTINATION lib/${PROJECT_NAME})` | Add the install line, rebuild |
| `ros2 launch`: file not found | Launch folder not installed into `share` | `install(DIRECTORY launch DESTINATION share/${PROJECT_NAME}/)` |
| `fatal error: x.hpp: No such file or directory` | Include dir not set, or the dependency isn't linked | `target_include_directories`, link the dependency's target |
| `undefined reference to ...` | Library not linked | Add it to `target_link_libraries` |
| `relocation ... can not be used when making a shared object; recompile with -fPIC` | A static library linked into a shared library/plugin | Build that code as a `SHARED` library |
| `error while loading shared libraries: libX.so` | `.so` not installed into `lib/` or workspace not sourced | `install(TARGETS/FILES ... DESTINATION lib)`, source |
| ros2_control: plugin class "… does not exist" | Plugin names don't match, XML not exported, or invalid XML | Check the three names, `pluginlib_export_plugin_description_file`, XML syntax |
| Typo in a `<depend>` (e.g. `hardware_interafce`) | rosdep: "Cannot locate rosdep definition" | Fix the spelling |
| `ament_package()` not last | Strange export/find errors in other packages | Move it to the end |

### See what the build is really doing

```bash
# Show the full compiler output of one package straight in the terminal
colcon build --packages-select my_pkg --event-handlers console_direct+

# Show the real c++ commands CMake runs (the same ones as in 00_what_the_hell_is_cmakelists.md)
colcon build --packages-select my_pkg --cmake-args -DCMAKE_VERBOSE_MAKEFILE=ON --event-handlers console_direct+

# CMake remembers old settings: start this package's configuration fresh
colcon build --packages-select my_pkg --cmake-clean-cache

# Last resort: clean everything and start from scratch
rm -rf build install log && colcon build
```

## See also

[12_creating_packages.md](12_creating_packages.md) · [01_workspace_and_build.md](01_workspace_and_build.md) · [21_cpp_basics.md](21_cpp_basics.md)
