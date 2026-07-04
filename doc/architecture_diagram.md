# System Architecture & Data Flow

## High-Level Pipeline
The system operates as a closed-loop navigation pipeline:
1. **Sensors**: LiDAR and Wheel Encoders generate raw physical data.
2. **Bridge**: `ros_gz_bridge` synchronizes simulation data into ROS 2 topics.
3. **Estimation**: `robot_localization` (EKF) fuses data into a stable `odom` frame.
4. **SLAM/Nav**: `slam_toolbox` generates the map, while `nav2` handles path planning.

## Transform Tree (TF2)
```mermaid
graph TD
    map -->|slam_toolbox| odom
    odom -->|ekf_node| base_link
    base_link --> chassis
    chassis --> wheel_left
    chassis --> wheel_right
    chassis --> lidar_link
    chassis --> camera_link

Component       |  Function                  | Frequency

sim.launch.py   | Unified Launch Controller  | On Start
nav2_params.yaml| Planner/Controller Settings| Init
ros_gz_bridge   | Gazebo-to-ROS Interface    | Continuous
slam_toolbox    | Active Mapping Engine      | 10Hz

