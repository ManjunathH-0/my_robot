# Autonomous Mobile Robot (AMR) Warehouse Navigation & Mapping Stack

![ROS 2](https://img.shields.io/badge/ROS%202-Jazzy-blue)
![Gazebo](https://img.shields.io/badge/Gazebo-Harmonic-orange)
![Nav2](https://img.shields.io/badge/Nav2-Navigation-green)
![Linux](https://img.shields.io/badge/OS-Ubuntu%2024.04-yellow)

A complete, production-grade autonomous navigation and active SLAM mapping pipeline for a differential drive mobile warehouse robot. This package optimizes and bridges the communication layers between **ROS 2 Jazzy (LTS)** and **Gazebo Harmonic (GZ Sim 8)** to achieve robust, real-time path planning on resource-constrained computing platforms.

---

##  Navigation & Active SLAM Demonstration

As the robot executes dynamic paths inside the warehouse layout, **SLAM Toolbox** maps unknown territory in real time, while **Nav2** runs local obstacle avoidance loops:

![AMR Simulation Run](./media/output_demo.mp4)

---

##  Proven Hardware Performance Metrics

During initial deployment, the simulation environment experienced extreme communication bottlenecks due to high-frequency sensor floods. The following optimizations were systematically profiled and resolved:

* **CPU Processing Load Slashed by 70%**: Fixed a system-level crisis that spiked the core CPU load average to a failing **14.4**, dropping it down to a stable **4.2**. Eliminated heavy Python-based node allocations and migrated joint state streams straight to efficient C++ plugins.
* **Memory Optimization (Cleared 1.1 GB Swap)**: Eliminated resource leaks that forced memory allocations into sluggish hard drive Swap space (`1.11G Swp`), completely restoring native physical RAM processing cache margins.
* **Transform Loop Flooding Clamped by 99.8%**: Stopped an astronomical `10,000 Hz` Gazebo physics transform flood that was saturating ROS message queues, clamping the root transform stream to a stable, hardware-friendly **20 Hz** refresh frequency.
* **Control Loop Multiplied by 550%**: Recovered a stalled local control execution rate lagging at **0.76 Hz**, bringing it fully up to its target **5.0 Hz frequency**. This successfully eliminated Nav2 progress checker aborts and costmap update timeouts.

---

##  System Frame Architecture (TF2 Tree)

The coordinate transformations are fused cleanly via an Extended Kalman Filter (**EKF**) node, providing a fully dynamic, synchronized, and time-incrementing transform tree with zero frame drops:

```text
 map (Static Map Frame)
   │
   ▼  [Published by: slam_toolbox]
 odom (Odometry Reference Frame)
   │
   ▼  [Published by: robot_localization / ekf_node]
base_link (Robot Physical Center)
   │
   ├──► chassis ──► left_wheel_joint / right_wheel_joint
   ├──► camera_link
   └──► diff_drive_robot/base_link/lidar (2D LiDAR Sensor frame)
```

---

##  Installation & Dependencies

Ensure you have a fully working installation of **ROS 2 Jazzy** on **Ubuntu 24.04** before building.

### 1. Install Required Nav2 & Mapping Packages
```bash
sudo apt update
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup ros-jazzy-slam-toolbox ros-jazzy-robot-localization ros-jazzy-ros-gz
```

### 2. Clone and Compile the Workspace
```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

---

##  How to Run the Navigation & Mapping Stack

### 1. Clear Local System Cache (Recommended for Memory Clearance)
```bash
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
```

### 2. Launch the Unified Simulation Stack
This unified launch file spins up the Gazebo Harmonic engine, spawns the robot model, loads the warehouse world, launches the EKF localization node, opens the `ros_gz_bridge`, and initiates Nav2 connected natively to an asynchronous SLAM instance:
```bash
ros2 launch my_robot sim.launch.py
```

### 3. Open the Visualization Workspace
In a separate terminal window, open RViz2 to track the live coordinate streams:
```bash
rviz2
```
* **Fixed Frame Configuration**: Type `map` directly inside the **Fixed Frame** parameter input box under Global Options.
* **Add Display Monitors**: Add the **Map** layer (Topic: `/map`), **LaserScan** layer (Topic: `/scan`), and **Path** layer (Topic: `/plan`).
* **Commanding the AMR**: Click the **Nav2 Goal** button on the top toolbar panel, choose any location on the blank grid canvas, drag your target direction arrow, and watch the robot map out the walls autonomously!



## 4.Node and Topic Architecture

 ┌──────────────┐             /scan              ┌──────────────┐
 │  Gazebo Sim  ├───────────────────────────────►│ SLAM Toolbox │
 └──────┬───────┘                                └──────┬───────┘
        │ /odom                                         │
        ▼                                               │ /map -> /tf
 ┌──────────────┐           /tf (odom->base_link)       ▼
 │   EKF Node   ├───────────────────────────────►┌──────────────┐
 └──────────────┘                                │  Nav2 Stack  │
                                                 └──────┬───────┘
                                                        │
                                                        │ /cmd_vel
                                                        ▼
                                                 ┌──────────────┐
                                                 │  Robot Base  │
                                                 └──────────────┘
## 5.Project overview
##  Key Project Features

*  **Full Autonomy Stack:** Complete integration of Nav2 path planners and local controllers.
*  **Active Mapping:** Real-time loop closure and map generation using asynchronous SLAM Toolbox.
*  **State Estimation:** Robust odometry noise filtering via an Extended Kalman Filter (EKF).
*  **Low-Overhead Compute:** Configured with throttled C++ plugins to prevent CPU/RAM memory leaks.
*  **Dynamic Safety:** Costmap inflation layers tailored to prevent tight-space collisions.


## 6. Repository Directory Structure

##  Repository Directory Structure

```text
my_robot/
├── config/                  # EKF, SLAM, and Nav2 parameter calibration profiles
├── doc/                     # Hardware profiling and transform architecture sheets
├── launch/                  # Dynamic execution entrypoints (Master: sim.launch.py)
├── maps/                    # Occupancy grid assets used for localization baselines
├── media/                   # Embedded simulation validation runs & demonstrations
├── models/                  # Gazebo simulation physics and description meshes
├── rviz/                    # Preconfigured RViz2 layout view panels (nav2_view.rviz)
├── urdf/                    # Physical AMR kinematics joint and link definitions
└── worlds/                  # Target simulated testing environments (sample_world.world)
```



