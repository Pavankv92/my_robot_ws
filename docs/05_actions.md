# Actions

Code: [`src/actions_py`](../src/actions_py)

**When:** a task that takes time and where you want progress or the option to cancel, e.g. move the robot to a position, navigate, count to N.

Unlike services, actions can:
- cancel the current execution
- provide feedback during the execution
- handle multiple requests, e.g. replace the current request with a new one

## Action server

Accepts or rejects the goal, gives feedback during execution, publishes the goal status, and responds to the result request.

| Underlying | Count | Used for |
|---|---|---|
| Services | 3 | Accept or reject the goal · cancel the goal · respond to the result request |
| Topics | 2 | Publish feedback during execution · publish goal status |

## Action client

Sends a goal. If it's accepted, sends a result request, or optionally a cancel request.

| Underlying | Count | Used for |
|---|---|---|
| Services | 3 | Send a goal · send the result request · cancel request |
| Topics | 2 | Receive feedback · receive goal status |

## Command line

```bash
ros2 action list                 # /action_name
ros2 action list -t              # /action_name [interface/action/TypeName]
ros2 action info /action_name
ros2 action send_goal /action_name <interface/action/TypeName> "<goal>" --feedback
```

By default, an action's underlying topics and services are hidden:

```bash
ros2 topic list --include-hidden-topics
ros2 service list --include-hidden-services
```

## Goal policies

Many possibilities, for example:
- goals can run in parallel
- a new goal can be rejected while the current goal is still executing

To accept goals in parallel, the server's callbacks need a `ReentrantCallbackGroup` and a multi-threaded executor (see [09_executors.md](09_executors.md)).

## See also

[03_communication_overview.md](03_communication_overview.md) · [04_services.md](04_services.md) · [06_custom_interfaces.md](06_custom_interfaces.md)
