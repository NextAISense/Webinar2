from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'rc_car_bringup'

data_files=[
    ('share/ament_index/resource_index/packages',
        ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
]
data_files.append(
    (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz'))
)
data_files.append(
    (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py'))
)

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zahid',
    maintainer_email='zahid@nextaisense.com',
    description='Bringup package for rc_car simulation and autonomy stack',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
