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
    use_sim_time = LaunchConfiguration('use_sim_time')

    # ---------------- Declare arguments ----------------
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time'
    )

    gz_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('rc_car_simulation'),
                'launch',
                'gz_sim.launch.py'
            ])
        )
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

    return LaunchDescription([

        declare_use_sim_time,

        # Gazebo simulation
        gz_sim_launch,

        # Robot state publisher
        rsp_launch,

        # RViz2
        rviz_launch,

    ])
