import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():

    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!
    package_name='f112th_sim_2401_alpha'

    joy_params = os.path.join(get_package_share_directory(package_name),'config','joystick.yaml')

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    joy_node = Node(package='joy', 
                    executable='joy_node',
                    parameters=[joy_params],
    )


    teleop_node = Node(package='teleop_twist_joy', 
                    executable='teleop_node',
                    name="teleop_node",
                    parameters=[joy_params],
                    remappings=[('/cmd_vel','/cmd_vel_out')]
    )
    
    # joystick = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory(package_name),'launch','joystick.launch.py'
    #             )]), launch_arguments={'use_sim_time': 'true'}.items()
    # )


    # twist_mux_params = os.path.join(get_package_share_directory(package_name),'config','twist_mux.yaml')
    
    # twist_mux_node = Node(package='twist_mux', 
    #                 executable='twist_mux',
    #                 parameters=[twist_mux_params,{'use_sim_time': True}],
    #                 remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')]
    # )

 #Launch them all!
    return LaunchDescription([
        joy_node,
        teleop_node
        # rsp.launch.py,
        # joystick,
        # twist_mux_node,
         #Lgazebo,
         #Lspawn_entity,
         #Ldiff_drive_spawner,
         #Ljoint_broad_spawner
        ])




