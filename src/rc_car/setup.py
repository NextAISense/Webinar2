from setuptools import find_packages, setup
# import os
# from glob import glob

package_name = 'rc_car'

data_files = [
    ('share/ament_index/resource_index/packages',
        ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
]

# Install all launch files
# data_files.append(
#     (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py'))
# )

# Recursively include all models (with meshes, textures, model.config, model.sdf, etc.)
# for path in glob('models/**', recursive=True):
#     if os.path.isfile(path):
#         data_files.append(
#             (os.path.join('share', package_name, os.path.dirname(path)), [path])
#         )

# Recursively include all worlds
# for path in glob('worlds/**', recursive=True):
#     if os.path.isfile(path):
#         data_files.append(
#             (os.path.join('share', package_name, os.path.dirname(path)), [path])
#         )

# Include rviz config files
# data_files.append(
#     (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz'))
# )

# Include URDF files
# data_files.append(
#     (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf'))
# )
# Include config files
# data_files.append(
#     (os.path.join('share', package_name, 'config'), glob('config/*.yaml'))
# )

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ashish',
    maintainer_email='ashish@nextaisense.com',
    description='ROS_GAZEBO Integrated Project',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'teleop_publisher = rc_car.teleop_publisher:main',
            'odom_listener    = rc_car.odom_listener:main',
            'parameter_demo   = rc_car.parameter_demo:main',
            'max_speed_server = rc_car.max_speed_server:main',
            'drive_distance_server = rc_car.drive_distance_server:main',
            'wheel_speed_publisher = rc_car.wheel_speed_publisher:main',
            'set_speed_client    = rc_car.set_speed_client:main',
            'drive_action_client = rc_car.drive_action_client:main',
            'circular_path = rc_car.circular_path:main',
            'cmd_vel_listener = rc_car.cmd_vel_listener:main',
        ],
    },
)
