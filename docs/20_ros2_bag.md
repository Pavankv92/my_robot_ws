# ros2 bag

Record topics to a file and replay them later, so you can debug or develop without the robot (or simulator) running.

## When

- Capture a bug once, then replay it as often as you need.
- Develop a node (e.g. a filter or detector) against real recorded sensor data.
- Compare runs before and after a change.

## Record

```bash
ros2 bag record /topic_1 /topic_2         # selected topics
ros2 bag record -a                        # all topics
ros2 bag record -o my_run /topic_1        # choose the bag name (a folder)
```

Stop with Ctrl+C. A bag is a **folder** containing the data file (MCAP format, the Jazzy default) and `metadata.yaml`.

## Inspect

```bash
ros2 bag info my_run                      # duration, topics, message counts
```

## Play

```bash
ros2 bag play my_run
ros2 bag play my_run --loop               # repeat forever
ros2 bag play my_run --rate 0.5           # half speed
ros2 bag play my_run --topics /topic_1    # only some topics
ros2 bag play my_run --clock              # also publish /clock from the bag
```

## Gotchas

- When replaying with `--clock`, start your nodes with `use_sim_time:=true`. Otherwise their timestamps won't match the recorded data (see [19_simulation_time.md](19_simulation_time.md)).
- Don't run the real source and the bag at the same time on the same topics, or two publishers mix their messages.
- `record -a` on a robot with cameras fills the disk quickly. Record only what you need.

## See also

[19_simulation_time.md](19_simulation_time.md) · [17_debugging.md](17_debugging.md)
