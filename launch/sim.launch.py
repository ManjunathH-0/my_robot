import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import SetParameter

def generate_launch_description():
    pkg_share = get_package_share_directory('my_robot')
    
    # Point directly to your custom world file
    world_path = '/home/manju/ros2_ws/src/my_robot/worlds/sample_world.world'
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

            {'use_sim_time': True},
            {'publish_frequency': 20.0},

            {'use_sim_time': True}
        ],
        arguments=['--ros-args', '-p', 'use_sim_time:=true'] 
    )

    # joint_state_publisher_node = Node(
    #     package='joint_state_publisher',
    #     executable='joint_state_publisher',
    #     parameters=[{'use_sim_time': True}]
    # )

    # Official ros_gz_sim launcher - handles world loading correctly alone
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={
            'gz_args': f'-r {world_path}' 
        }.items()
    )

        # Locate the official Nav2 bringup directory
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    
    # Declare the nested Nav2 launch execution block
    nav2_navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
        ]),
        launch_arguments={
            'use_sim_time': 'true',
            'autostart': 'true',
            # Route straight to your saved static warehouse map asset
            'map': '/home/manju/ros2_ws/src/my_robot/maps/my_gazebo_map.yaml',
            # Route straight to your custom, optimized parameter tuning file
            'params_file': '/home/manju/ros2_ws/src/my_robot/config/nav2_params.yaml'
        }.items()
    )

        
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        SetParameter(name='use_sim_time', value=True),
        
        # 1. State Publishers 
        robot_state_publisher_node,
       #joint_stste_publisher_node, 
  
        
        # 2. Gazebo (ONLY launch this official wrapper instance!)
        gazebo,

        nav2_navigation,

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

               # '/model/diff_drive_robot/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
                '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
                '/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo',
                '/joint_states@sensor_msgs/msg/JointState[gz.msgs.ModelV', 
                '/model/diff_drive_robot/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
                '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
                '/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo'

            ],
            remappings=[('/model/diff_drive_robot/tf', '/tf')],
            output='screen'
        ),

        # 4. EKF Node
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
