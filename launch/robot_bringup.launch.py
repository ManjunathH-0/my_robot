from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. State Publisher (Reads your URDF)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': open('/home/manju/ros2_ws/src/my_robot/urdf/robot.urdf').read()}],
        ),

        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            parameters=[{'robot_description': open('/home/manju/ros2_ws/src/my_robot/urdf/robot.urdf').read()}]
        ),
        # 2. Odom -> Base_link Bridge (The 'Static' fix)
        #Node(
        #   package='tf2_ros',
        #   executable='static_transform_publisher',
        #    arguments=['0', '0', '0.1', '0', '0', '0', 'odom', 'base_link']
        #)
    ])