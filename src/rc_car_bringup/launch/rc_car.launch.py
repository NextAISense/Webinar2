from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, PythonExpression
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition
import os

def generate_launch_description():

    # ---------------- Launch configurations ----------------
    use_slam = LaunchConfiguration('use_slam')
    use_sim_time = LaunchConfiguration('use_sim_time')
    slam_mode = LaunchConfiguration('slam_mode')
    slam_sync = LaunchConfiguration('slam_sync')
    param_file = LaunchConfiguration('param_file')
    map_file = LaunchConfiguration('map_file')

    # ---------------- Declare arguments ----------------
    declare_use_slam = DeclareLaunchArgument(
        'use_slam',
        default_value='true',
        description='Enable SLAM Toolbox'
    )
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time'
    )
    declare_slam_mode = DeclareLaunchArgument(
        'slam_mode',
        default_value='mapping',
        description='SLAM mode: mapping or localization'
    )
    declare_slam_sync = DeclareLaunchArgument(
        'slam_sync',
        default_value='true',
        description='Enable SLAM synchronization'
    )
    declare_param_file = DeclareLaunchArgument(
        'param_file',
        default_value='',
        description='Path to the SLAM parameters file'
    )
    declare_map_file = DeclareLaunchArgument(
        'map_file',
        default_value='',
        description='Map yaml file (used in localization mode)'
    )

    gz_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('rc_car_simulation'),
                'launch',
                'gz_sim.launch.py'
            ])
        ),
        launch_arguments={
            'use_sim_time': use_sim_time
        }.items()
    )

    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('rc_car_bringup'),
                'launch',
                'rviz.launch.py'
            ])
        )
    )

    rsp_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('rc_car_description'),
                'launch',
                'rsp.launch.py'
            ])
        ),
        launch_arguments={
            'use_sim_time': use_sim_time
        }.items()
    )

    ekf_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('rc_car_localization'),
                'launch',
                'localization.launch.py'
            ])
        ),
        launch_arguments={
            'use_sim_time': use_sim_time
        }.items()
    )

    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('rc_car_slam'),
                'launch',
                'slam.launch.py'
            ])
        ),
        condition=IfCondition(use_slam),
        launch_arguments={
            'slam_mode': slam_mode,
            'slam_sync': slam_sync,
            'use_sim_time': use_sim_time,
            'param_file': param_file,
            'map_file': map_file
        }.items()
    )

    return LaunchDescription([

        declare_use_slam,
        declare_use_sim_time,
        declare_slam_mode,
        declare_slam_sync,
        declare_param_file,
        declare_map_file,

        # Gazebo simulation
        gz_sim_launch,

        # Robot state publisher
        rsp_launch,

        #  EKF localization
        ekf_launch,

        # RViz2
        rviz_launch,

        # SLAM
        slam_launch

    ])
