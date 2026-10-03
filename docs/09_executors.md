# Executors

Code: [`src/executor_py`](../src/executor_py)

An executor decides **which callback runs when, and in which thread**.

## Main callbacks in ROS 2

1. Timers
2. Subscribers
3. Service servers
4. Action servers
5. Futures (in clients)

## Under the hood

1. `rclpy.init()`: initialises ROS communication for a given context.
2. `rclpy.shutdown()`: shuts down a previously initialised context. This also shuts down the global executor.
3. `rclpy.spin(node, executor)` (don't use this for multiple threads):
   1. Executes work and blocks until the context associated with the executor is shut down.
   2. Creates an executor, the default one if none is given.
   3. The executor runs the callbacks using `executor.spin_once()`, which executes a single callback. With multiple callbacks, they run **sequentially**.
   4. This function blocks.

`spin()` runs `spin_once()` in a loop:

```python
while some_condition:
    spin_once()
```

## Single-threaded executor

One callback at a time, **sequentially**. This is what `rclpy.spin(node)` uses.

See `single_threaded_executor.py`.

## Multi-threaded executor

Runs callbacks in several threads. **Callback groups** decide which callbacks may run at the same time.

| Callback group | Callbacks in the group… | Use for |
|---|---|---|
| `MutuallyExclusiveCallbackGroup` (the default) | run **one at a time**. A callback can't re-enter. | Callbacks that share state: no locks needed between them |
| `ReentrantCallbackGroup` | run **in parallel**, and the same callback can run several times at once | Independent work, e.g. an action server handling several goals. **Must be thread-safe.** |

Callbacks in **different** groups can always run in parallel with each other.

```python
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

group = MutuallyExclusiveCallbackGroup()
self.create_timer(1.0, self.callback, callback_group=group)

executor = MultiThreadedExecutor()
executor.add_node(node)
executor.spin()
```

See `multi_threaded_executor.py` and `multiple_nodes_in_multithreaded_executor.py`.

## When to use what?

| Situation | Use |
|---|---|
| Normal node, short callbacks | `rclpy.spin(node)` (single-threaded). Keep it simple. |
| A callback **waits** for something: a service response, a long computation, `time.sleep` | Multi-threaded executor, with the slow callback in its own group |
| Calling a service from inside a callback and waiting for the result | Multi-threaded executor, with the client in its own group. Or don't wait: use `call_async` + a done-callback. |
| Action server that should accept several goals at once | `ReentrantCallbackGroup` |
| Several nodes in one process | One executor, `executor.add_node()` for each (see [11_components.md](11_components.md)) |

## Gotchas

- **Deadlock:** waiting for a future (`spin_until_future_complete`, a blocking `call()`) **inside** a callback with a single-threaded executor never returns. The response can't be processed, because the only thread is busy waiting.
- **Starvation:** in a mutually exclusive group, only one callback runs at a time. If callbacks take longer than their timer period, one callback can keep winning and the others **never run**. That's what happens to `callback_3` in `multiple_nodes_in_multithreaded_executor.py` (2 s of work on a 1 s timer).
- **Python GIL:** Python threads take turns, so a multi-threaded executor helps with *waiting* (I/O, sleeps, service calls) but doesn't make CPU-heavy Python code faster.

## See also

[03_communication_overview.md](03_communication_overview.md) · [11_components.md](11_components.md)
