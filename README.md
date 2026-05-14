# 🤖 Roomba Robot Cleaner - Simulator

A Python-based visual simulator for an autonomous Roomba robot that cleans 3 rooms with obstacle avoidance, battery management, and intelligent pathfinding.

## 📋 Project Overview

This project demonstrates a **4-layer software architecture** for a mobile robot:
1. **Entry Point** (`main.py`) — initialization and main loop
2. **Decision Brain** (`controller.py`) — state machine and control logic
3. **Logic Helpers** (`scheduler.py`, `home_mapper.py`) — scheduling and spatial mapping
4. **Hardware Layer** (`hardware_simulator.py`) — motor and sensor simulation

The robot automatically cleans 3 rooms at a scheduled time, with real-time visualization showing:
- Room layout and obstacle placement
- Robot position and movement
- Battery level and charging cycles
- Dust bin status
- Cleaned floor percentage (accounting for unreachable areas)

## 🎮 Features

- **Visual Simulator** — tkinter GUI showing live cleaning animation
- **Obstacle System** — click to place/remove walls; robot skips unreachable areas
- **Intelligent Navigation** — A* pathfinding to navigate around obstacles
- **Battery Management** — robot returns to dock at 50% battery for charging
- **Reachability Analysis** — BFS flood-fill to identify physically accessible cells
- **Grid-Based Cleaning** — systematic 10x10 grid pattern through each room

## 🛠 Technologies Used

- **Python 3.x**
- **tkinter** — GUI visualization
- **heapq** — A* pathfinding algorithm
- **Collections** — BFS queue for reachability analysis

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/kaskus90/robot_project.git
cd robot_project
```

2. No external dependencies — uses only Python standard library.

## 🚀 How to Run

```bash
python -X utf8 src/visualizer.py
```

The `-X utf8` flag ensures emoji display works correctly on Windows.

## 🎯 How to Use

1. **Watch the simulation** — robot automatically starts cleaning at 14:00 (2 PM)
2. **Place obstacles** — click on any room cell to add a red wall (click again to remove)
3. **Monitor status** — right panel shows battery %, dust bin %, cleaned %, and robot state
4. **Battery charging** — when battery reaches 50%, robot returns to yellow dock station to recharge

## 📁 File Structure

```
src/
├── main.py              # Basic CLI version (non-visual)
├── visualizer.py        # Interactive GUI simulator
├── controller.py        # Robot control logic & state machine
├── hardware_simulator.py # Motor and sensor simulation
├── scheduler.py         # Cleaning schedule management
├── home_mapper.py       # Room layout and grid generation
└── pathfinder.py        # A* pathfinding algorithm
```

## 🏗 Architecture Details

**Controller State Machine:**
- `IDLE` → `CLEANING` → `MOVING_TO_ROOM` → `AVOIDING`/`DOCKED`

**Hardware Components:**
- Motors: LEFT, RIGHT (movement), BRUSH, VACUUM (cleaning)
- Sensors: Sonar (distance), Dust level

**Robot Behavior:**
1. Checks schedule → starts cleaning at 14:00
2. Navigates to each room in sequence
3. Cleans in 10x10 grid pattern
4. Skips obstacle cells using A* pathfinding
5. Returns to dock when battery < 50% or dust bin > 90%
6. Charges and empties bin before resuming

## 🧠 Algorithms

**A* Pathfinding** — finds shortest path around obstacle clusters to reach next cleanable cell

**BFS Reachability** — identifies all grid cells physically accessible from the robot's starting position (prevents cleaning inside walled areas)

## 📊 Visualization

- **Green cells** — successfully cleaned
- **White cells** — unreachable (inside walls)
- **Red cells** — obstacles
- **Orange circle** — robot position
- **Yellow square** — charging dock

## 🎓 Educational Value

This project demonstrates:
- Layered software architecture
- State machine design
- Pathfinding algorithms
- Sensor simulation
- Hardware abstraction
- Real-time visualization

## 👨‍💻 Author

Kuba K. (kaskus90)

## 📝 License

Open source for educational purposes.
