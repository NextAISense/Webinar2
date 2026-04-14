from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():

    bridge_config = PathJoinSubstitution([
        FindPackageShare('rc_car_simulation'),
        'config',
        'ros_gz_bridge.yaml'
    ])

    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[bridge_config],
        output='screen'
    )

    return LaunchDescription([
        bridge_node
    ])
