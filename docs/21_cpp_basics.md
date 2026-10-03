# C++ Basics (rclcpp)

Everything in this repo so far is Python (`rclpy`). C++ (`rclcpp`) is needed for performance-critical nodes, components with zero-copy, and **ros2_control hardware interfaces**, which must be C++.

## rclpy → rclcpp

| Python (rclpy) | C++ (rclcpp) |
|---|---|
| `rclpy.init()` | `rclcpp::init(argc, argv);` |
| `class MyNode(Node)` | `class MyNode : public rclcpp::Node` |
| `super().__init__('name')` | `MyNode() : Node("name") {}` |
| `self.create_publisher(Int64, 'topic', 10)` | `create_publisher<example_interfaces::msg::Int64>("topic", 10)` |
| `self.create_subscription(Int64, 'topic', cb, 10)` | `create_subscription<example_interfaces::msg::Int64>("topic", 10, cb)` |
| `self.create_timer(1.0, cb)` | `create_wall_timer(1s, cb)` |
| `self.get_logger().info('hi')` | `RCLCPP_INFO(get_logger(), "hi");` |
| `self.declare_parameter('rate', 1.0)` | `declare_parameter("rate", 1.0);` |
| `self.get_parameter('rate').value` | `get_parameter("rate").as_double()` |
| `rclpy.spin(node)` | `rclcpp::spin(node);` |
| `rclpy.shutdown()` | `rclcpp::shutdown();` |

## Minimal node: publisher + timer

```cpp
#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"

using namespace std::chrono_literals;

class NumberPublisher : public rclcpp::Node
{
public:
  NumberPublisher() : Node("number_publisher")
  {
    publisher_ = create_publisher<example_interfaces::msg::Int64>("number", 10);
    timer_ = create_wall_timer(1s, [this]() {
      example_interfaces::msg::Int64 msg;
      msg.data = 2;
      publisher_->publish(msg);
    });
    RCLCPP_INFO(get_logger(), "Number publisher started");
  }

private:
  rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<NumberPublisher>());
  rclcpp::shutdown();
  return 0;
}
```

Subscriber callback:

```cpp
subscriber_ = create_subscription<example_interfaces::msg::Int64>(
  "number", 10,
  [this](const example_interfaces::msg::Int64 & msg) {
    RCLCPP_INFO(get_logger(), "Got %ld", msg.data);
  });
```

## Build: package files

```bash
ros2 pkg create --build-type ament_cmake my_cpp_pkg --dependencies rclcpp example_interfaces
```

`CMakeLists.txt`, for each executable:

```cmake
add_executable(number_publisher src/number_publisher.cpp)
ament_target_dependencies(number_publisher rclcpp example_interfaces)

install(TARGETS number_publisher
  DESTINATION lib/${PROJECT_NAME}
)
```

`package.xml`:

```xml
<depend>rclcpp</depend>
<depend>example_interfaces</depend>
```

## Gotchas

- **Store everything you create** (publishers, subscribers, timers) in member variables. If a `SharedPtr` goes out of scope, the publisher/timer is destroyed, and silently stops working.
- Every new executable needs **both** `add_executable(...)` and an entry in `install(TARGETS ...)`, otherwise `ros2 run` can't find it.
- Unlike Python, `--symlink-install` doesn't help with C++. After every change, **rebuild**.
- Message headers are `snake_case.hpp` while types are `CamelCase`: `example_interfaces/msg/int64.hpp` → `example_interfaces::msg::Int64`.

## See also

[01_workspace_and_build.md](01_workspace_and_build.md) · [12_creating_packages.md](12_creating_packages.md)
