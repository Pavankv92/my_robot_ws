# Creating Packages

How to set up the four kinds of package you'll need:

| # | Package | Build type | Example in this repo |
|---|---|---|---|
| 1 | [Python only](#1-python-package) | `ament_python` | [`src/my_py_pkg`](../src/my_py_pkg) |
| 2 | [C++ only](#2-c-package) | `ament_cmake` | (see [21_cpp_basics.md](21_cpp_basics.md)) |
| 3 | [Python + C++ in one package](#3-python--c-in-one-package) | `ament_cmake` + `ament_cmake_python` | [`src/my_robot_utils`](../src/my_robot_utils) |
| 4 | [Using an external C++ library (`.so`)](#4-using-an-external-c-library-so) | `ament_cmake` | the ST3215 servo SDK (`scservo_sdk`) |

What each line in these files means: [22_cmakelists_and_package_xml.md](22_cmakelists_and_package_xml.md).

All packages live in `src/`, and are created **from inside `src/`**:

```bash
cd ~/my_robot_ws/src
```

---

## 1. Python package

**When:** nodes written in Python. This is the quickest way to get started.

```bash
ros2 pkg create my_py_pkg --build-type ament_python --dependencies rclpy example_interfaces
```

```
my_py_pkg/
├── package.xml
├── setup.py              ← executables (entry points) + extra files to install
├── setup.cfg             ← where executables are installed (generated, leave as is)
├── resource/my_py_pkg    ← empty marker file (generated, leave as is)
├── my_py_pkg/            ← your Python code (same name as the package)
│   ├── __init__.py
│   └── my_node.py
├── launch/               ← optional
└── test/
```

### `package.xml`

```xml
<depend>rclpy</depend>
<depend>example_interfaces</depend>      <!-- every package you import -->

<export>
  <build_type>ament_python</build_type>
</export>
```

### `setup.py`

Each node is an **entry point**: `executable_name = package.module:function`.

```python
import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'my_py_pkg'

setup(
    name=package_name,
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # install launch files (only if you have a launch/ folder)
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
    ],
    entry_points={
        'console_scripts': [
            'my_node = my_py_pkg.my_node:main',
        ],
    },
    # ... maintainer, description, license
)
```

### Build and run

```bash
cd ~/my_robot_ws
colcon build --packages-select my_py_pkg --symlink-install
source install/setup.bash
ros2 run my_py_pkg my_node
```

### Gotchas

- The node file needs a `main()` function. The entry point calls it.
- **New node or new entry point → rebuild**, even with `--symlink-install`. Only edits to existing files are picked up without rebuilding.
- Launch/config files are only found if they're listed in `data_files`.

---

## 2. C++ package

**When:** performance-critical nodes, or anything that must be C++ (e.g. ros2_control hardware interfaces).

```bash
ros2 pkg create my_cpp_pkg --build-type ament_cmake --dependencies rclcpp example_interfaces
```

```
my_cpp_pkg/
├── package.xml
├── CMakeLists.txt
├── include/my_cpp_pkg/   ← headers (.hpp)
├── src/                  ← sources (.cpp)
└── launch/               ← optional
```

### `package.xml`

```xml
<buildtool_depend>ament_cmake</buildtool_depend>

<depend>rclcpp</depend>
<depend>example_interfaces</depend>      <!-- every package you find_package() -->

<export>
  <build_type>ament_cmake</build_type>
</export>
```

### `CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 1. Dependencies (one find_package per <depend> in package.xml)
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(example_interfaces REQUIRED)

# 2. One block per executable
add_executable(my_node src/my_node.cpp)
target_include_directories(my_node PRIVATE include)
ament_target_dependencies(my_node rclcpp example_interfaces)

# 3. Install executables (so `ros2 run` finds them) ...
install(TARGETS my_node
  DESTINATION lib/${PROJECT_NAME}
)

# ... and folders like launch/ and config/ (so `ros2 launch` finds them)
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
```

### Build and run

```bash
cd ~/my_robot_ws
colcon build --packages-select my_cpp_pkg
source install/setup.bash
ros2 run my_cpp_pkg my_node
```

### Gotchas

- Every executable needs **both** `add_executable(...)` and an entry in `install(TARGETS ...)`. Without the install, `ros2 run` says "No executable found".
- C++ must be **rebuilt after every change**. `--symlink-install` doesn't help here.
- `package.xml` and `CMakeLists.txt` must agree: each `<depend>` normally has a matching `find_package()`.

---

## 3. Python + C++ in one package

**When:** a package needs both, e.g. C++ nodes plus Python helper scripts, or Python modules that other packages import. The package is an `ament_cmake` package that **also** installs Python.

Shows how to put Python and C++ files in the same package. Files in this package can be imported and used by both Python and C++ packages.

```bash
ros2 pkg create my_robot_utils --build-type ament_cmake --dependencies rclcpp rclpy
```

```
my_robot_utils/
├── package.xml
├── CMakeLists.txt
├── include/my_robot_utils/      ← C++ headers
├── src/                         ← C++ sources
└── my_robot_utils/              ← Python: folder with the SAME name as the package
    ├── __init__.py              ← empty, makes it an importable module
    └── angle_conversion_server.py
```

Each Python executable starts with the shebang, and must be executable:

```python
#!/usr/bin/env python3
```

```bash
chmod +x my_robot_utils/angle_conversion_server.py
```

### `package.xml`

```xml
<buildtool_depend>ament_cmake</buildtool_depend>
<buildtool_depend>ament_cmake_python</buildtool_depend>

<depend>rclcpp</depend>
<depend>rclpy</depend>
<depend>my_robot_interfaces</depend>

<export>
  <build_type>ament_cmake</build_type>
</export>
```

### `CMakeLists.txt`

```cmake
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(my_robot_interfaces REQUIRED)

# C++ executables: exactly as in a C++ package
add_executable(my_cpp_node src/my_cpp_node.cpp)
target_include_directories(my_cpp_node PRIVATE include)
ament_target_dependencies(my_cpp_node rclcpp my_robot_interfaces)
install(TARGETS my_cpp_node DESTINATION lib/${PROJECT_NAME})

# Python module: makes `import my_robot_utils` work from other packages
ament_python_install_package(${PROJECT_NAME})

# Python executables: installed as scripts next to the C++ executables
install(PROGRAMS
  ${PROJECT_NAME}/angle_conversion_server.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
```

### Run

```bash
ros2 run my_robot_utils my_cpp_node
ros2 run my_robot_utils angle_conversion_server.py      # note: Python scripts keep the .py
```

### Dependencies

```bash
sudo apt install python3-transforms3d
```

### Gotchas

- There's no `setup.py` here. Python executables are installed with `install(PROGRAMS ...)` instead of entry points.
- With `--symlink-install`, the installed script is a link to your source file, so the **source** file needs `chmod +x`. Otherwise `ros2 run` fails with "permission denied".
- `ament_python_install_package(${PROJECT_NAME})` needs the Python folder to have **the same name** as the package, with an `__init__.py`.

---

## 4. Using an external C++ library (`.so`)

**When:** your code needs a library that isn't a ROS package, e.g. a motor vendor's SDK.

Pick the first option that fits:

| Option | Library comes as | Example |
|---|---|---|
| **A. System package** | An apt package (`lib...-dev`) | `libserial-dev` |
| **B. SDK package** | Source code you have to ship yourself | The ST3215 servo SDK → `scservo_sdk` |
| **C. Prebuilt `.so`** | Only a compiled `.so` + headers, no source | Closed-source vendor driver |

### A. System package (apt)

```bash
sudo apt install libserial-dev
```

`package.xml` (rosdep key, so `rosdep install` can install it on other machines):

```xml
<depend>libserial-dev</depend>
```

`CMakeLists.txt`. If the library ships a CMake config, `find_package(<Lib> REQUIRED)` is enough. Otherwise use pkg-config:

```cmake
find_package(PkgConfig REQUIRED)
pkg_check_modules(LIBSERIAL REQUIRED IMPORTED_TARGET libserial)

target_link_libraries(my_node PkgConfig::LIBSERIAL)
```

### B. SDK package: build the vendor's source as its own ROS package

This is what was done for the ST3215 servo. The vendor's `.cpp`/`.h` files go into their own package, which builds a **shared library** (`.so`) that any other package can use. That's the same idea as ROBOTIS's `dynamixel_sdk`.

```
scservo_sdk/
├── package.xml                  ← no ROS dependencies
├── CMakeLists.txt
├── include/scservo_sdk/*.h      ← vendor headers, unmodified
└── src/*.cpp                    ← vendor sources, unmodified
```

**The SDK package's `CMakeLists.txt`:**

```cmake
cmake_minimum_required(VERSION 3.8)
project(scservo_sdk)

find_package(ament_cmake REQUIRED)
# No -Wall -Wextra -Wpedantic: vendor code isn't ours to fix

# 1. Build the vendor sources as a shared library -> libscservo_sdk.so
add_library(${PROJECT_NAME} SHARED
  src/SCS.cpp
  src/SCSerial.cpp
  src/SMS_STS.cpp
)

# 2. Headers: users write #include <scservo_sdk/SMS_STS.h>
target_include_directories(${PROJECT_NAME}
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include/${PROJECT_NAME}>
  PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include/${PROJECT_NAME}   # vendor files use #include "SMS_STS.h"
)

# 3. Install headers and library
install(DIRECTORY include/ DESTINATION include/${PROJECT_NAME})
install(TARGETS ${PROJECT_NAME}
  EXPORT export_${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

# 4. Let other packages find_package() it and link scservo_sdk::scservo_sdk
ament_export_targets(export_${PROJECT_NAME} HAS_LIBRARY_TARGET)

ament_package()
```

**A package that uses it:**

`package.xml`:
```xml
<depend>scservo_sdk</depend>
```

`CMakeLists.txt`:
```cmake
find_package(scservo_sdk REQUIRED)

add_executable(ping_servo src/ping_servo.cpp)
target_include_directories(ping_servo PRIVATE include)
target_link_libraries(ping_servo scservo_sdk::scservo_sdk)    # library + its include path
```

Code:
```cpp
#include <scservo_sdk/SMS_STS.h>
```

### C. Prebuilt `.so` (no source)

Put the files in your package and wrap them in an **imported target**:

```
my_driver/
├── lib/libvendor.so
└── include/vendor/vendor.h
```

```cmake
add_library(vendor SHARED IMPORTED)
set_target_properties(vendor PROPERTIES
  IMPORTED_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/lib/libvendor.so
  INTERFACE_INCLUDE_DIRECTORIES ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(my_node vendor)

# The .so must be installed too, or the program can't load it at runtime
install(FILES lib/libvendor.so DESTINATION lib)
```

### Gotchas

- **`error while loading shared libraries: libX.so: cannot open shared object file`**: the `.so` wasn't installed into `lib/`, or the workspace isn't sourced. Check with `ldd install/<pkg>/lib/<pkg>/<executable>`.
- **Static `.a` libraries** are often compiled without `-fPIC` and **can't** be linked into a shared library such as a ros2_control plugin. Build from source as a `SHARED` library instead (option B).
- **Keep vendor files unmodified.** Updating the SDK is then just copying the new files in.
- **Check the licence** before putting vendor code in a public repository.

---

## See also

[01_workspace_and_build.md](01_workspace_and_build.md) · [06_custom_interfaces.md](06_custom_interfaces.md) (interface packages) · [08_launch_files.md](08_launch_files.md) · [21_cpp_basics.md](21_cpp_basics.md)
