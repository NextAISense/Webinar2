from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    SetEnvironmentVariable,
    UnsetEnvironmentVariable
)
from launch.substitutions import TextSubstitution, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    sim_pkg_share = get_package_share_directory('rc_car_simulation')

    model_dir = PathJoinSubstitution([
        FindPackageShare('rc_car_simulation'),
        'models'
    ])

    world_dir = PathJoinSubstitution([
        FindPackageShare('rc_car_simulation'),
        'worlds'
    ])

    gz_resource_path = [
        model_dir,
        TextSubstitution(text=':'),
        world_dir
    ]

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time'
    )

    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='parameter_bridge',
        parameters=[{
            'config_file': PathJoinSubstitution([
                FindPackageShare('rc_car_simulation'),
                'config',
                'ros_gz_bridge.yaml'
            ])
        }],
        output='screen'
    )

    return LaunchDescription([

        declare_use_sim_time,

        # Clean environment to avoid Gazebo conflicts
        UnsetEnvironmentVariable(name='GZ_SIM_RESOURCE_PATH'),

        # Set only the paths we want
        SetEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=gz_resource_path
        ),

        # Launch Gazebo Harmonic with your world
        ExecuteProcess(
            cmd=[
                'gz', 'sim',
                PathJoinSubstitution([sim_pkg_share, 'worlds', 'world_demo.sdf'])
            ],
            output='screen'
        ),

        # Launch the bridge node
        bridge_node
    ])
