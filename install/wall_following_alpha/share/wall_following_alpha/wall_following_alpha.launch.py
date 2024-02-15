import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    package_name = 'wall_following_alpha'

    mux_params = os.path.join(get_package_share_directory(package_name), 'config.yaml')

    twist_mux_wall = Node(
        name='twist_mux_wall',
        package='twist_mux',
        executable='twist_mux',
        parameters=[mux_params],
        remappings=[('/cmd_vel_out', '/diff_cont/cmd_vel_unstamped')] #Remap into Gazebo
    )
    return LaunchDescription([twist_mux_wall])

# Resource that we used : https://github.com/robofoundry/twist_mux_example

