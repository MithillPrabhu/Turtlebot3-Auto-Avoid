# TurtleBot3 Auto Avoid & Mapping

![ROS 2](https://img.shields.io/badge/ROS%202-rclpy-22314E?logo=ros)
![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

A ROS 2 Python package for TurtleBot3 that drives the robot autonomously around obstacles using its LiDAR, and saves the map built during SLAM so it can be reused for navigation.

## Features

- **Reactive obstacle avoidance** (`auto_avoid`): reads `/scan`, checks the front, left and right sectors, and publishes velocity commands on `/cmd_vel`
- **SLAM mapping**: run alongside Cartographer while the robot explores
- **One-command map saving** (`map_saver`): calls the Nav2 map saver service to write the map as `.pgm` + `.yaml`

## How it works

### `auto_avoid`

On every LiDAR scan the node:

1. Splits the scan into three sectors: **front** (about ±10 readings around 0°), **left** (around 90°) and **right** (around −90°).
2. Takes the closest distance in each sector.
3. If an obstacle is closer than **0.5 m** in front, it stops and turns on the spot (0.5 rad/s) toward whichever side has more free space.
4. Otherwise, it drives straight ahead at **0.2 m/s**.

Distances and the command it sends are logged on every scan for easy debugging.

| Topic | Type | Direction |
|---|---|---|
| `/scan` | `sensor_msgs/LaserScan` | subscribed |
| `/cmd_vel` | `geometry_msgs/Twist` | published |

### `map_saver`

Waits for the `/map_saver/save_map` service (`nav2_msgs/SaveMap`), then saves the `/map` topic as `my_saved_map.pgm` and `my_saved_map.yaml` (free threshold 0.25, occupied threshold 0.65).

## Repository structure

```text
turtlebot3_auto_avoid/
├── turtlebot3_auto_avoid/
│   ├── auto_avoid.py     # LiDAR obstacle-avoidance node
│   └── map_saver.py      # calls the Nav2 map saver service
├── test/                 # ament copyright, flake8 and pep257 checks
├── package.xml
├── setup.py
└── setup.cfg
```

## Requirements

- ROS 2 with `rclpy`
- TurtleBot3 packages (real robot or simulation) publishing `/scan` and listening on `/cmd_vel`
- Cartographer, to build the map
- Nav2 map server (`nav2_map_server`), to provide the `/map_saver/save_map` service

## Build

```bash
mkdir -p ~/tb3_ws/src && cd ~/tb3_ws/src
git clone https://github.com/MithillPrabhu/Turtlebot3-Auto-Avoid.git
cd ~/tb3_ws
colcon build --packages-select turtlebot3_auto_avoid
source install/setup.bash
```

## Usage

With the TurtleBot3 (or its simulation) and Cartographer running:

```bash
# Terminal 1: drive autonomously and avoid obstacles
ros2 run turtlebot3_auto_avoid auto_avoid

# Terminal 2: once the map looks complete, save it
ros2 run turtlebot3_auto_avoid map_saver
```

The map is written to the directory where `map_saver` is run.

## License

Released under the Apache License 2.0. See [LICENSE](LICENSE).

## Author

**Mithill Prabhu**, Robotics & Automation Engineer
[Portfolio](https://mithillprabhu.github.io) · [LinkedIn](https://www.linkedin.com/in/mithill-prabhu/) · psmithill27@gmail.com
