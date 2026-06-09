import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, SetEnvironmentVariable, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import SetParameter

def generate_launch_description():
    pkg_share = get_package_share_directory('my_robot')
    world_path = '/home/manju/ros2_ws/src/my_robot/worlds/world.sdf'
    urdf_file = '/home/manju/ros2_ws/src/my_robot/urdf/robot.urdf'
    ekf_config = os.path.join(pkg_share, 'config', 'ekf.yaml')


    with open(urdf_file, 'r') as infp:
        robot_description_content = infp.read()
    
    # Define Nodes
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {'robot_description': robot_description_content},
            {'use_sim_time': True}  # Force it here
        ],
        # Add this to ensure it picks up the global parameter
        arguments=['--ros-args', '-p', 'use_sim_time:=true'] 
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        parameters=[{'use_sim_time': True}]
    )

    
        
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        SetParameter(name='use_sim_time', value=True),
        
        # 1. Gazebo Server
        ExecuteProcess(cmd=['gz', 'sim', '-r', world_path], output='screen'),

        # 2. State Publishers (Start these early!)
        robot_state_publisher_node,
        joint_state_publisher_node,

        # 3. Bridge (Essential to pass /tf and /scan)
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            parameters=[{'use_sim_time': True}],
            arguments=[
                '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
                '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                '/model/diff_drive_robot/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V'
            ],
            remappings=[('/model/diff_drive_robot/tf', '/tf')],
            output='screen'
        ),

        # 4. EKF Node (Only ONE instance)
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            parameters=[ekf_config, {'use_sim_time': True}],
            output='screen'
        ),

        

        # 5. Spawner (Last)
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-topic', '/robot_description', '-name', 'diff_drive_robot'],
            output='screen'
        )
    ])