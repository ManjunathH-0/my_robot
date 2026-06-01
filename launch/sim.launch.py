import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Locate our package deployment share directory
    pkg_share = get_package_share_directory('my_robot')
    
    # 2. Define paths to our world file and model directory
    world_path = os.path.join(pkg_share, 'worlds', 'world.sdf')

    # We provide BOTH the Share directory and the explicit models directory path
    models_path = pkg_share + ":" + os.path.join(pkg_share,'models')

    #3. CRITICAL FOR GAZEBO HARMONIC: Tell Gazebo where to look for models.
    # This appends our models directory to the native Gazebo resource path.
    if 'GZ_SIM_RESOURCE_PATH' in os.environ:
        gz_resource_path = os.environ['GZ_SIM_RESOURCE_PATH'] + ':' + models_path
    else:
        gz_resource_path = models_path

    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=gz_resource_path
    )

    # 4. Include the native Gazebo Sim launch file
    # This brings up the Gazebo Harmonic server and client GUI
    gz_sim_share = get_package_share_directory('ros_gz_sim')
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world_path}'}.items()
    )

    # AUTOMATED BRIDGE NODE
    # Bridge /cmd_vel (inputs), /odom (odometry feedback), /scan (LIDAR rays), and /tf (frames)
    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/tf@tf2_msgs/msg/TFmessage[gz.msgs.Pose_V'
        ],
        output='screen'
    )

    # 5. Create and return the launch description
    return LaunchDescription([
        set_gz_resource_path,
        gz_sim,
        ros_gz_bridge
    ])