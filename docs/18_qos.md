# Quality of Service (QoS)

QoS settings decide **how** messages are delivered: guaranteed or not, how many are kept, whether late subscribers get old messages.

**The #1 reason for "my subscriber receives nothing"** is incompatible QoS between publisher and subscriber.

## The settings that matter

| Setting | Options | Meaning |
|---|---|---|
| **Reliability** | `RELIABLE` / `BEST_EFFORT` | Retry until delivered / send once, drop if lost |
| **History + depth** | `KEEP_LAST` + depth N / `KEEP_ALL` | Queue size for messages not yet processed |
| **Durability** | `VOLATILE` / `TRANSIENT_LOCAL` | New subscribers get nothing old / get the last message(s) ("latched") |

The `10` in `create_publisher(String, 'topic', 10)` is shorthand for: `KEEP_LAST`, depth 10, `RELIABLE`, `VOLATILE`.

## Compatibility: publisher vs. subscriber

| Publisher | Subscriber | Works? |
|---|---|---|
| RELIABLE | RELIABLE | ✅ |
| RELIABLE | BEST_EFFORT | ✅ |
| BEST_EFFORT | BEST_EFFORT | ✅ |
| BEST_EFFORT | **RELIABLE** | ❌ no messages |
| TRANSIENT_LOCAL | VOLATILE | ✅ (but no old messages) |
| VOLATILE | **TRANSIENT_LOCAL** | ❌ no messages |

**Rule of thumb:** the subscriber can't ask for more than the publisher offers.

## Typical choices

| Data | QoS |
|---|---|
| Commands, state, most topics | Default (reliable, depth 10) |
| High-rate sensors (camera, lidar, IMU) | `qos_profile_sensor_data` (best effort, small depth). The newest data matters more than every message. |
| "Publish once, everyone must get it" (`/robot_description`, `/tf_static`, maps) | `TRANSIENT_LOCAL` + reliable, so late subscribers still get it |

## In code

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy, qos_profile_sensor_data

qos = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    depth=5,
    durability=DurabilityPolicy.VOLATILE,
)
self.create_subscription(LaserScan, 'scan', self.callback, qos)
self.create_subscription(Image, 'camera/image', self.callback, qos_profile_sensor_data)
```

## Command line

```bash
ros2 topic info -v /topic_name                           # QoS of every publisher and subscriber
ros2 topic echo --qos-reliability best_effort /scan      # echo a best-effort topic
ros2 topic echo --qos-durability transient_local /robot_description
```

## Gotchas

- An incompatible QoS doesn't raise an error in your code. It only logs a warning ("incompatible QoS"), and **no data flows**. Check with `ros2 topic info -v`.
- `ros2 topic echo` on a best-effort sensor topic can show nothing unless you pass `--qos-reliability best_effort`.
- A subscriber to `/robot_description` that starts late gets nothing unless it uses `TRANSIENT_LOCAL`.

## See also

[02_nodes_and_topics.md](02_nodes_and_topics.md)
