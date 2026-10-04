# What the Hell Is CMakeLists.txt?

The background behind every ROS 2 C++ package: how C++ code is organised, how it becomes a program, and why that needs a `CMakeLists.txt`. We start with plain C++, build a small example **by hand**, and step by step get to CMake and ROS 2.

When you're done here, [22_cmakelists_and_package_xml.md](22_cmakelists_and_package_xml.md) explains every line of `package.xml` and `CMakeLists.txt`.

> **In short**
> - C++ code is split into **headers** (`.h`/`.hpp`: what exists) and **sources** (`.cpp`: how it works).
> - Before it can run, it must be **compiled** (each `.cpp` → `.o`) and **linked** (`.o` files + libraries → program).
> - Doing that by hand gets out of control fast. A **Makefile** remembers the commands, and **CMake** writes the Makefile for you, from a recipe: `CMakeLists.txt`.
> - In ROS 2, `colcon build` runs CMake for every package, puts the results in **`install/`**, and `source install/setup.bash` tells your terminal where to find them.

---

## How C++ code is organised

### The file types

| Extension | Name | Contains | Notes |
|---|---|---|---|
| `.hpp` | C++ header | **Declarations**: which classes and functions exist, and their arguments | The ROS 2 convention for C++ |
| `.h` | Header | Same idea | Used by C and older C++ code, e.g. the servo SDK's `SMS_STS.h` |
| `.cpp` | Source | **Definitions**: the actual code of those functions | Also seen as `.cc` or `.cxx`, same thing |

`.h` and `.hpp` are both just text files. The compiler doesn't care about the extension; it's a convention telling **humans** "C++ only" (`.hpp`) or "maybe C too" (`.h`).

### Declaration vs. definition: the menu and the kitchen

| | Declaration (header) | Definition (source) |
|---|---|---|
| Says | "This exists, and here's how to call it" | "Here's what it actually does" |
| Like… | A **menu**: lists the dishes | The **kitchen**: cooks them |
| Example | `void setSpeed(double speed);` | `void Motor::setSpeed(double speed) { speed_ = speed; }` |
| Who needs it | Every file that **uses** it (via `#include`) | Compiled **once**, then linked in |

After compiling you get the **cooked meal**: machine code in `.o`, `.a` or `.so` files.

### A class split into header + source

```cpp
// motor.hpp: the menu
#pragma once                       // include this file only once per .cpp, even if included twice

class Motor {
public:
    void setSpeed(double speed);   // declarations only: no { } bodies
    double getSpeed() const;

private:
    double speed_ = 0.0;
};
```

```cpp
// motor.cpp: the kitchen
#include "motor.hpp"

void Motor::setSpeed(double speed) { speed_ = speed; }   // Motor:: = "this belongs to class Motor"
double Motor::getSpeed() const { return speed_; }
```

```cpp
// main.cpp: the customer
#include <iostream>
#include "motor.hpp"               // only the menu is needed to use Motor

int main() {
    Motor m;
    m.setSpeed(1.5);
    std::cout << m.getSpeed() << std::endl;
}
```

**Why split at all?**
- **Faster builds:** change the body of `setSpeed` and only `motor.cpp` is recompiled. Every file that just includes `motor.hpp` is untouched.
- **Clear interface:** the header is the "user manual". Readers see what a class offers without wading through its code.
- **Libraries:** you can ship compiled code (`.so`) plus headers, without the sources.

### Include guards: `#pragma once`

`#include` literally **pastes** the header's text into the `.cpp`. If a header gets included twice (directly, and through another header), its class would be defined twice → compile error. Guards prevent that:

```cpp
#pragma once                       // modern, short: supported by all common compilers
```
```cpp
#ifndef MY_PKG__MOTOR_HPP_         // classic version, same effect
#define MY_PKG__MOTOR_HPP_
// ... header content ...
#endif
```

**Every header needs one.**

### Header-only code

Some code lives **entirely** in the header: declarations **and** definitions. It's called **header-only**. Nothing to compile separately, nothing to link; the code arrives through `#include`.

- Typical for small helpers, templates, and libraries like Eigen.
- Our `ST3215Driver` (`st3215_driver.hpp`) is header-only.
- **Gotcha:** a normal function body in a header that is included by **two** `.cpp` files gives `multiple definition of 'twice(int)'` at link time (✅ tested). Fix: mark it `inline`, or define it inside the class body, which is automatically inline.

### Where the files go: folder layout

**A plain C++ project:**

```
my_project/
├── CMakeLists.txt
├── include/            ← headers (.hpp): the public "menu"
│   └── motor.hpp
└── src/                ← sources (.cpp): the "kitchen" + main
    ├── motor.cpp
    └── main.cpp
```

**A ROS 2 C++ package** uses the same idea, with one extra folder level so headers from different packages can't collide:

```
st3215_servo/
├── package.xml
├── CMakeLists.txt
├── include/st3215_servo/        ← #include "st3215_servo/st3215_driver.hpp"
│   └── st3215_driver.hpp
└── src/
    ├── ping_servo.cpp
    └── test_motors.cpp
```

The `include/<package_name>/` level is why ROS includes always start with the package name: `<rclcpp/rclcpp.hpp>`, `"st3215_servo/st3215_driver.hpp"`.

---

**So far these are just text files.** The rest of this note is about how they become a program you can run.

## Why C++ needs a build step (and Python doesn't)

**Python** is run directly from the `.py` file: the interpreter reads it at runtime. "Building" a Python package only **copies** files into place.

**C++** must be translated into machine code first:

```
 my_node.cpp ──┐                                                        ┌── executable  (my_node)
 helper.cpp  ──┼──▶ 1. compile ──▶ my_node.o, helper.o ──▶ 2. link ──────┤
 *.hpp       ──┘    (each .cpp       (object files:          + libraries └── or a library (libx.so)
  (#included)        separately)      machine code)          (rclcpp, ...)
```

1. **Compile:** each `.cpp` becomes an **object file** (`.o`). `#include "x.hpp"` simply pastes the header's text in first.
2. **Link:** the object files are joined with the **libraries** they use into one executable or library.

Remember the menu and the kitchen from above: your code `#include`s a header so the compiler knows a function exists. The **linker** then finds the compiled code for it in a library. Forget the header → "No such file"; forget the library → "undefined reference".

## Why CMake, then? A worked example

_Based on my CMake notes from July 2020. Every command below has been re-run on this PC; the outputs are real._

### The project

```
folder/
├── tools.h       declaration
├── tools.cpp     implementation
└── main.cpp      uses it
```

```cpp
// tools.h
#pragma once
#include <string>

void PrintYourName(std::string name);      // declaration: "this function exists"
```

```cpp
// tools.cpp
#include <iostream>
#include "tools.h"

void PrintYourName(std::string name) {     // implementation: what it does
    std::cout << name << std::endl;
}
```

```cpp
// main.cpp
#include "tools.h"

int main() {
    PrintYourName("Pavan");
}
```

### Attempt 1: compile only `main.cpp` → linker error

```bash
c++ -std=c++11 main.cpp -o main
```
```
main.cpp: undefined reference to `PrintYourName(std::__cxx11::basic_string<...>)'
collect2: error: ld returned 1 exit status
```

The error comes from the **linker** (`ld`), while building, so there's no `main` to run yet.
- `main.cpp` includes `tools.h`, so the **compiler** knows `PrintYourName` exists.
- But nobody compiled `tools.cpp`, so the **linker** has no machine code for it.
- `main` needs the **binary code** of `tools.cpp`, the file you get by compiling `tools.cpp`.

**Look inside** with `nm`, which lists the functions in a compiled file:

```bash
c++ -c main.cpp -o main.o  && nm -C main.o  | grep PrintYourName
#   U PrintYourName(...)     ← U = Undefined: "I use this, someone else must provide it"
c++ -c tools.cpp -o tools.o && nm -C tools.o | grep PrintYourName
#   T PrintYourName(...)     ← T = defined here (in the code "Text" section): "I provide it"
```

The linker's whole job is to match every **U** with a **T**. "undefined reference" means it found a U with no matching T.

### Solution: compile `tools.cpp` separately, then link it in

```bash
c++ -std=c++11 -c tools.cpp -o tools.o      # 1. compile tools.cpp into a binary object file
c++ -std=c++11 main.cpp tools.o -o main     # 2. pass the binary file in while building main
./main                                      # 3. run → Pavan
```

`-c` means "compile only, don't link": the result is an object file (`.o`), not a program. Ta-da!

### With many files: organise objects into a library

With many `.cpp` files you don't want to pass every `.o` file around. You pack them into a **library**:

```bash
# 1. compile every .cpp file individually into an object file (module)
c++ -std=c++11 -c tools.cpp -o tools.o
#    ... repeat for every other .cpp file

# 2. organise all modules into a static library:  ar rcs lib<name>.a module1.o module2.o ...
ar rcs libtools.a tools.o
ar t libtools.a                              # list what's inside → tools.o
#    (a static library is just a bundle of .o files)

# 3. link the library when building the program
c++ -std=c++11 main.cpp -L . -ltools -o main
#                       └─┬─┘ └──┬──┘
#     -L . = look for libraries in this folder
#   -ltools = link libtools.a (or libtools.so): "lib" and the extension are added automatically

# 4. run
./main                                       # → Pavan
```

The **shared** version of the same library (see [Libraries](#libraries-a-and-so) below):

```bash
c++ -std=c++11 -fPIC -shared tools.cpp -o libtools.so    # build a shared library
c++ -std=c++11 main.cpp -L . -ltools -o main             # same link command
./main
```
```
./main: error while loading shared libraries: libtools.so: cannot open shared object file
```
```bash
ldd ./main | grep tools                                   # libtools.so => not found
LD_LIBRARY_PATH=. ldd ./main | grep tools                 # libtools.so => ./libtools.so
LD_LIBRARY_PATH=. ./main                                  # tell the loader where to look → Pavan
```

A shared library is only **found at run time**. That's exactly what `source install/setup.bash` sets up for ROS packages (`LD_LIBRARY_PATH`).

### The middle step: a Makefile

Typing those commands every time is tedious and easy to get wrong. Worse, after changing one file you have to remember **which** commands to run again.

A **Makefile** solves that. It's a file that remembers:
1. **what** to build (targets)
2. **from what** (dependencies)
3. **how** (the commands)

`make` then runs **only the commands whose inputs changed**.

The same example as a Makefile:

```makefile
CXX = c++
CXXFLAGS = -std=c++11 -Wall

# target:   what it's made from
#     command to make it  (this line MUST start with a TAB, not spaces)

main: main.o libtools.a
	$(CXX) main.o -L . -ltools -o main

main.o: main.cpp tools.h
	$(CXX) $(CXXFLAGS) -c main.cpp -o main.o

libtools.a: tools.o
	ar rcs libtools.a tools.o

tools.o: tools.cpp tools.h
	$(CXX) $(CXXFLAGS) -c tools.cpp -o tools.o

clean:
	rm -f main *.o *.a
```

Read it as a recipe tree:

```
main ──needs──▶ main.o ──needs──▶ main.cpp, tools.h
     └─needs──▶ libtools.a ──needs──▶ tools.o ──needs──▶ tools.cpp, tools.h
```

### How to run the Makefile

Save the file as **`Makefile`** (exactly that name, no extension) in the same folder as the sources. Then, **in that folder**:

```bash
make            # build the FIRST target in the file (here: main), plus everything it needs
./main          # run the result → Pavan
```

`make` only builds things. Running the program is a separate step.

| Command | Does | Real output / use |
|---|---|---|
| `make` | Builds the first target (`main`) and whatever it needs | The 4 commands: compile, compile, `ar`, link |
| `make tools.o` | Builds just **one** target | `c++ -std=c++11 -Wall -c tools.cpp -o tools.o` |
| `make clean` | Runs the `clean` target: delete the build results | `rm -f main *.o *.a` |
| `make -n` | **Dry run:** prints the commands without running them | See what *would* happen |
| `make -B` | Rebuilds **everything**, even what's up to date | When you suspect a stale build |
| `make -j4` | Runs up to 4 commands **in parallel** | Faster on big projects |
| `make -C some/folder` | Runs `make` in another folder | `make: Entering directory '.../make_demo'` |
| `make -f other.mk` | Uses a file not called `Makefile` | Rarely needed |

Two errors you'll meet:

| Error | Meaning |
|---|---|
| `make: *** No targets specified and no makefile found.  Stop.` | You're in the wrong folder, or the file isn't named `Makefile` |
| `Makefile:5: *** missing separator.  Stop.` | A command line starts with **spaces** instead of a **TAB**. Many editors silently turn TABs into spaces. |

**How `make` decides:** it compares file **timestamps**. If a target is older than anything it needs, it's rebuilt; otherwise it's skipped.

| You run | `make` does (real output) |
|---|---|
| `make` (first time) | Everything: `c++ -c main.cpp`, `c++ -c tools.cpp`, `ar rcs libtools.a`, link `main` |
| `make` again, nothing changed | `make: 'main' is up to date.` Nothing to do. |
| Edit `main.cpp`, then `make` | Only `c++ -c main.cpp` + link. `tools.o` is still fresh, so it's skipped. |
| Edit `tools.h`, then `make` | Recompiles **both** `.cpp` files (both include it) and relinks |
| `make clean` | `rm -f main *.o *.a`: start from scratch |

On a big project, that's the difference between rebuilding 3 files and rebuilding 300.

**Why not write Makefiles by hand?**
- You must list every header dependency yourself. Forget `tools.h` in `main.o: main.cpp tools.h`, and a header change silently gives you a **stale build**.
- Every library needs its `-I`/`-L`/`-l` flags written out, and they differ between machines.
- There's no standard way to install the results or to tell other projects where they are.

### CMake writes the Makefile for us

That's the real role of CMake: **CMake doesn't compile anything itself. It generates the build files, and `make` does the compiling.**

```
CMakeLists.txt ──cmake ..──▶ Makefile (generated) ──make──▶ c++ / ar commands ──▶ main, libtools.a
  (you write)                 (you never edit it)    (runs only what changed)
```

For our tiny project, the generated Makefiles are **333 lines** (`build/Makefile` plus `build/CMakeFiles/main.dir/build.make`, …), versus 5 lines of `CMakeLists.txt`. CMake also:
- **scans `#include`s for you,** so header dependencies are never forgotten
- adds useful targets. `make help` lists them: `all`, `clean`, `main`, `tools`, …
- can generate other build files: `cmake -G Ninja ..` writes `build.ninja` for the faster **Ninja** tool instead of a Makefile

**Running CMake's Makefile** works exactly like running our hand-written one, just from the `build/` folder where CMake generated it:

```bash
cd build
make             # same as before: only rebuilds what changed
make clean       # same
make VERBOSE=1   # show the real c++ commands CMake's Makefile runs
```

`make VERBOSE=1` shows commands like `c++ -MD -MT … -c src/tools.cpp`. The `-MD` flag makes the compiler write down every header a `.cpp` includes, which is how CMake's Makefile **knows** to rebuild when `tools.h` changes, without you listing it.

**In ROS 2,** `colcon build` runs exactly this for every package: `cmake` (generate) → `make` (build) → `make install`. That's why `build/<pkg>/` contains a `Makefile` and `CMakeCache.txt`.

### The CMakeLists.txt for our example

We can't do this by hand when there are many files and many libraries. CMake links the binaries, libraries and executables for us. The whole library-creation-and-linking dance above, and the Makefile, become:

```cmake
cmake_minimum_required(VERSION 3.8)
project(tools_demo)

add_library(tools src/tools.cpp)        # name: tools, files: tools.cpp     → libtools.a
add_executable(main src/main.cpp)       # name: main,  files: main.cpp      → main
target_link_libraries(main tools)       # link the library "tools" into "main"
```

The **names** connect the lines: `tools` in `add_library` is the same `tools` in `target_link_libraries`.

`add_library` without `SHARED` builds a **static** library (`libtools.a`). Write `add_library(tools SHARED ...)` for `libtools.so`.

**By hand → CMake → ROS 2:**

| By hand | CMake | In a ROS 2 package |
|---|---|---|
| `c++ -c tools.cpp -o tools.o` + `ar rcs libtools.a tools.o` | `add_library(tools src/tools.cpp)` | same, usually `SHARED` |
| `c++ main.cpp -o main` | `add_executable(main src/main.cpp)` | same |
| `-L . -ltools` | `target_link_libraries(main tools)` | same, plus other packages: `rclcpp::rclcpp` |
| `-I src` | `target_include_directories(main PRIVATE src)` | same, usually `include/` |
| `-std=c++11` | `target_compile_features(main PUBLIC cxx_std_11)` | same (ROS 2 Jazzy uses C++17) |
| copy the results somewhere | `install(...)` | `install(...)` into `install/<pkg>/` |
| run the commands / write a Makefile | `cmake ..` (generates the Makefile) + `make` | `colcon build` (runs cmake + make for you) |

**What CMake gives you on top:**
- **Only rebuilds what changed.** Edit one `.cpp` and only that file is recompiled.
- **Parallel builds:** `make -j4` compiles 4 files at once.
- **Finds dependencies:** `find_package(rclcpp)` instead of hand-written `-I` and `-L` paths.
- **Works on another machine:** the recipe is the same everywhere; only the paths it finds differ.

### General project structure and the build process

```
cpp/
├── CMakeLists.txt       ← the recipe
├── src/
│   ├── main.cpp
│   ├── tools.h
│   └── tools.cpp
└── build/               ← contains all the files generated by the build
    ├── Makefile, CMakeCache.txt, CMakeFiles/ ...
    ├── main             ← the binary
    └── libtools.a       ← the library
```

Larger plain-CMake projects often configure output folders: `bin/` for all the binary files and `lib/` for all the libraries. In ROS, `install/<pkg>/lib/...` plays that role.

**The build process is now simple:**

```bash
mkdir build && cd build
cmake ..          # read ../CMakeLists.txt, generate the Makefiles here
make -j4          # compile; -j4 = 4 files in parallel
./main            # → Pavan
```
```
[ 50%] Linking CXX static library libtools.a
[ 50%] Built target tools
[100%] Linking CXX executable main
[100%] Built target main
```

**Building outside the source folder** (`build/`) keeps generated files away from your code, so cleaning up is just deleting one folder.

**If something goes wrong: clean the build and start from scratch.**

```bash
rm -rf build && mkdir build && cd build && cmake .. && make -j4
```

In ROS: `rm -rf build install log` in the workspace, then `colcon build`.

**Try it yourself** (5 minutes, in a throwaway folder):

```bash
mkdir -p /tmp/cmake_demo/src && cd /tmp/cmake_demo
printf '#pragma once\n#include <string>\nvoid PrintYourName(std::string name);\n' > src/tools.h
printf '#include <iostream>\n#include "tools.h"\nvoid PrintYourName(std::string name) { std::cout << name << std::endl; }\n' > src/tools.cpp
printf '#include "tools.h"\nint main() { PrintYourName("Pavan"); }\n' > src/main.cpp
printf 'cmake_minimum_required(VERSION 3.8)\nproject(tools_demo)\nadd_library(tools src/tools.cpp)\nadd_executable(main src/main.cpp)\ntarget_link_libraries(main tools)\n' > CMakeLists.txt
mkdir build && cd build && cmake .. && make && ./main
```

Then experiment:
- delete `target_link_libraries` and watch the linker error come back
- add `SHARED` to `add_library` and look for `libtools.so`
- edit only `main.cpp`, run `make` again, and see that only `main` is rebuilt

### Header-only in CMake

If `tools.h` contains the **full implementation** (no `tools.cpp`, see [Header-only code](#header-only-code) above), there's no library to build or link. CMake only needs:

```cmake
add_executable(main src/main.cpp)
```

That setup builds fine. `ST3215Driver` works this way: header-only itself, but it calls the servo SDK, which is a real library and still has to be linked.

### `#include "..."` vs `#include <...>`

| Form | The compiler searches | Typical use |
|---|---|---|
| `#include "tools.h"` | **First the folder of the file that includes it**, then the include paths | Your own headers next to your `.cpp` |
| `#include <tools.h>` | **Only the include paths** (system folders + what you add) | Libraries and other packages: `<rclcpp/rclcpp.hpp>`, `<scservo_sdk/SMS_STS.h>` |

To use `<...>` for your own headers, or to include them from another folder, add the folder to the include paths. Old style, for every target in the file:

```cmake
include_directories(${PROJECT_SOURCE_DIR}/src)          # path to the header files
```

Modern style, for one target:

```cmake
target_include_directories(main PRIVATE ${PROJECT_SOURCE_DIR}/src)
```

### From plain CMake to ROS 2

**`CMakeLists.txt` is the recipe:** what to build, from which files, with which dependencies, and where to put the results. Then:

```
CMakeLists.txt ──cmake──▶ Makefiles (in build/<pkg>/) ──make──▶ .o, .so, executables ──make install──▶ install/<pkg>/
```

- **CMake** turns the recipe into Makefiles. **make** runs the compiler, and only recompiles files that changed.
- **colcon** does this for **every package**, in dependency order (taken from `package.xml`).
- **ament_cmake** is ROS's set of CMake helpers: `ament_package()`, `ament_export_targets()`, …
- **ament_python** packages skip CMake: `setup.py` copies the files and creates the executables.

## Libraries: `.a` and `.so`

A **library** is compiled code packed up so several programs can use it, e.g. `rclcpp`, or the servo SDK. It has no `main()`, so it can't run by itself.

| | Static library | Shared (dynamic) library |
|---|---|---|
| File | `libname.a` | `libname.so` |
| Linked… | at **build** time: its code is **copied into** each executable | at **run** time: the executable only stores "I need `libname.so`" |
| Executable size | Bigger | Smaller |
| Fix a bug in the library | Rebuild **every** program that uses it | Rebuild the library only |
| Can be loaded while running (plugins) | ❌ | ✅ |
| Must be compiled with `-fPIC` | Usually not (so it can't go into a `.so`) | ✅ always |
| In ROS 2 | Rare | **Almost everything**: `librclcpp.so`, `libscservo_sdk.so`, your plugins |

**You already build shared libraries in this repo:** `my_robot_interfaces` has no `.cpp` files of your own, but `rosidl_generate_interfaces()` generates code for your messages and compiles it into libraries:

```
install/my_robot_interfaces/lib/
├── libmy_robot_interfaces__rosidl_typesupport_cpp.so            ← used by C++ nodes
├── libmy_robot_interfaces__rosidl_typesupport_c.so
├── libmy_robot_interfaces__rosidl_typesupport_fastrtps_cpp.so   ← (de)serialising for the DDS middleware
├── libmy_robot_interfaces__rosidl_typesupport_fastrtps_c.so
├── libmy_robot_interfaces__rosidl_typesupport_introspection_cpp.so
├── libmy_robot_interfaces__rosidl_typesupport_introspection_c.so
└── python3.12/site-packages/my_robot_interfaces/                 ← used by Python nodes
```

That's why a package that uses `HardwareStatus` must list `my_robot_interfaces` as a dependency: it links against these libraries.

### How a program finds its `.so` files at run time

When a program starts, the system's **loader** looks for every `.so` it needs: first in the system folders (`/usr/lib`, …), then in the folders listed in **`LD_LIBRARY_PATH`**. `source install/setup.bash` adds each package's `install/<pkg>/lib/` to that variable.

`ldd` shows what a program or library needs and where each one was found:

```bash
$ ldd install/my_robot_hardware/lib/libmy_robot_hardware.so
    libhardware_interface.so => /opt/ros/jazzy/lib/libhardware_interface.so
    libscservo_sdk.so        => /home/robot/ros2_ws/install/scservo_sdk/lib/libscservo_sdk.so
    librclcpp.so             => /opt/ros/jazzy/lib/librclcpp.so
    ...
```

If one line says `=> not found`, the program fails with "error while loading shared libraries". The usual fix is to source the workspace.

### Plugins: shared libraries loaded on demand

A **plugin** is a `.so` that a running program loads **by name**, without having been linked against it. That's how ros2_control uses your hardware interface:

```
URDF: <plugin>mobile_base_hardware/MobileBaseHardwareInterface</plugin>
   │
   ▼
pluginlib looks the name up in the plugin XMLs registered for "hardware_interface"
   │   (found through share/ament_index/resource_index/hardware_interface__pluginlib__plugin/)
   ▼
my_robot_hardware_interface.xml says: class is in library "my_robot_hardware"
   │
   ▼
loads install/my_robot_hardware/lib/libmy_robot_hardware.so, creates the class
```

`ros2_control_node` was compiled long before your plugin existed. That's why plugins **must** be shared libraries.

## Where everything goes after building

### The workspace

```
~/ros2_ws/
├── src/       your source code: the only folder you edit (and put in git)
├── build/     intermediate files: CMake cache, Makefiles, .o files (one folder per package)
├── install/   the finished result: what ROS actually uses
└── log/       colcon build logs
```

`build/`, `install/` and `log/` are generated. They're safe to delete for a clean rebuild (`rm -rf build install log`), and belong in `.gitignore`.

### Inside `install/<pkg>/`

The real result of building `my_robot_hardware` (a plugin library):

```
install/my_robot_hardware/
├── lib/
│   └── libmy_robot_hardware.so          ← the plugin (install(TARGETS ... LIBRARY DESTINATION lib))
├── include/my_robot_hardware/my_robot_hardware/
│   ├── mobile_base_hardware_interface.hpp   ← headers (install(DIRECTORY include/ ...))
│   └── st3215_driver.hpp
└── share/
    ├── my_robot_hardware/
    │   ├── package.xml                        ← always installed
    │   ├── my_robot_hardware_interface.xml    ← plugin XML (pluginlib_export_plugin_description_file)
    │   ├── cmake/my_robot_hardwareConfig.cmake ...   ← makes find_package(my_robot_hardware) work
    │   ├── environment/, hook/                ← snippets run by `source`: add lib/ to LD_LIBRARY_PATH, ...
    │   └── (launch/, config/, urdf/ ... if installed)
    └── ament_index/resource_index/
        ├── packages/my_robot_hardware                         ← "this package exists" (ros2 pkg list)
        └── hardware_interface__pluginlib__plugin/my_robot_hardware   ← "I have hardware_interface plugins"
```

A Python package from this repo, `my_py_pkg`, puts its entry-point executables in `lib/<pkg>/` and the code itself in `site-packages`:

```
install/my_py_pkg/lib/
├── my_py_pkg/
│   ├── first_node          ← small launcher scripts generated from setup.py entry_points
│   ├── my_publisher
│   └── ...
└── python3.12/site-packages/my_py_pkg/
    ├── first_node.py       ← your code: a COPY of src/ (or a link to it, with --symlink-install)
    └── ...
```

A C++ package with executables (like `st3215_servo`) also has them in `lib/<pkg>/`:

```
install/st3215_servo/lib/st3215_servo/
├── ping_servo          ← install(TARGETS ping_servo DESTINATION lib/${PROJECT_NAME})
├── test_motors
└── st3215_gui.py       ← install(PROGRAMS ...)
```

| Folder | Holds | Who looks there |
|---|---|---|
| `lib/<pkg>/` | Executables | `ros2 run <pkg> <exe>` |
| `lib/` | Libraries and plugins (`.so`) | The loader (via `LD_LIBRARY_PATH`), pluginlib |
| `include/<pkg>/` | Headers | Other packages' compilers |
| `share/<pkg>/` | `package.xml`, launch, config, URDF, CMake config | `ros2 launch`, `$(find-pkg-share)`, `find_package()` |
| `share/ament_index/` | Marker files | `ros2 pkg list`, pluginlib (how ROS **finds** packages and plugins) |

### What `source install/setup.bash` does

It sets environment variables so every tool can find what's in `install/`:

| Variable | Gets `install/...` added | So that… |
|---|---|---|
| `AMENT_PREFIX_PATH` | each package's folder | `ros2 run`, `ros2 launch`, pluginlib find packages |
| `CMAKE_PREFIX_PATH` | each package's folder | `find_package()` works for the **next** build |
| `LD_LIBRARY_PATH` | each package's `lib/` | programs find their `.so` files |
| `PATH` | `bin/` folders | plain commands work |
| `PYTHONPATH` | Python site-packages | `import my_pkg` works |

**Underlay and overlay:** `/opt/ros/jazzy` (sourced first) is the **underlay**, and your workspace is the **overlay** on top. A package in your workspace overrides one with the same name in the underlay.

```bash
echo $AMENT_PREFIX_PATH | tr ':' '\n'     # see which workspaces are active, overlay first
```

**After adding a new package, re-source** (or open a new terminal). The variables were set before it existed.

## The big picture

```
 src/<pkg>/                 colcon build                    install/<pkg>/                source               ros2 run / launch
 ├─ package.xml   ──▶  1. order packages (package.xml) ──▶  ├─ lib/<pkg>/   executables ──▶  install/setup.bash ──▶  finds executables,
 ├─ CMakeLists.txt     2. cmake: read the recipe            ├─ lib/         .so libraries    sets AMENT_PREFIX_PATH,  libraries, launch
 ├─ src/*.cpp          3. make: compile + link → build/     ├─ include/     headers          LD_LIBRARY_PATH, ...     files, plugins
 └─ include/*.hpp      4. make install ──────────────────▶  └─ share/<pkg>/ launch, URDF, ...
```

Every problem you'll hit sits in one of these four boxes:
- **Wrong recipe** (`package.xml` / `CMakeLists.txt`) → the build fails.
- **Not installed** → `ros2 run`/`ros2 launch` can't find it.
- **Not sourced** → nothing can find anything, or you get old versions.

---

---

## Next

[22_cmakelists_and_package_xml.md](22_cmakelists_and_package_xml.md): every line of `package.xml` and `CMakeLists.txt` explained · [12_creating_packages.md](12_creating_packages.md): templates per package type
