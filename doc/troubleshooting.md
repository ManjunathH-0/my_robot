# Troubleshooting & Debugging Log

This document records the critical technical hurdles overcome during the development of this AMR project.

## 1. Kinematic Chain Failures (URDF)
* **Issue:** `robot_state_publisher` failing with `XML_ERROR_MISMATCHED_ELEMENT`.
* **Resolution:** Performed recursive XML syntax validation using `check_urdf`. Cleaned up non-standard Gazebo tags and ensured correct link-joint inheritance.
* **Impact:** Restored the transformation tree, enabling the navigation stack to identify the robot's physical frame.

## 2. Odometry/TF Propagation Errors
* **Issue:** SLAM Toolbox failing with "Failed to compute odom pose" warnings.
* **Resolution:** Configured `gz::sim::systems::DiffDrive` in the URDF to explicitly set `<publish_odom_tf>true</publish_odom_tf>`.
* **Impact:** Established a reliable `/odom` to `/base_link` transform, essential for real-time localization.

## 3. High-Frequency Transform Flooding
* **Issue:** System CPU load spike (14.4) due to 10,000 Hz transform broadcast.
* **Resolution:** Clamped the `ros_gz_bridge` and Gazebo physics publish rate to a stable 20 Hz.
* **Impact:** Reduced CPU utilization by 70%, allowing Nav2 to operate without frame timeouts.
