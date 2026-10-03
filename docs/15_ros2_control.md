# ros2_control

## Main parts

| Part | Role |
|---|---|
| **Resource manager** | Talks to and manages the hardware. Provides the interfaces (API) to talk to it. |
| **Controller manager** | Works with the resource manager and loads the right controllers. |
| **Controllers** | A library of control algorithms. |

## Hardware

The hardware can be individual components or a whole system:
- **Sensor**
- **Actuator**
- **System**

## Interfaces

| Type | Purpose |
|---|---|
| **Command interface** | Pass commands to the hardware |
| **State interface** | Read the hardware's current state |

## Controller manager

Loads the controllers defined in the configuration, e.g. joint position controllers.

## Controllers

Implement the actual control logic, e.g. based on:
- position
- velocity
- effort

## Configuration

1. Connect ros2_control to Gazebo through a plugin.
2. Configure ros2_control itself: the system, resource manager and controller manager.
3. There are many parameters, so load them all at once from a YAML file.
