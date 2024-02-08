## F1/12th Simulator
ros2 launch f112th_sim_2401_alpha rsp.launch.py use_sim_time:=true
add use_sim_time:=true to use gazebo
ros2 run joint_state_publisher_gui joint_state_publisher_gui
rviz2 -d src/f112th_sim_2401_alpha/description/description.rviz

*pdte robot_core.xacro Inertial stuff


ros2 launch f112th_sim_2401_alpha launch_sim.launch.py world:=~/ros2_ws/src/f112th_sim_2401_alpha/worlds/BigRoom.world
ros2 run teleop_twist_keyboard teleop_twist_keyboard
rviz2 -d src/f112th_sim_2401_alpha/description/rviz_model.rviz

ros2 launch f112th_sim_2401_alpha launch_sim.launch.py world:=~/ros2_ws/src/f112th_sim_2401_alpha/worlds/BigRoom.world
ros2 launch f112th_sim_2401_alpha joystick.launch.py
rviz2 -d src/f112th_sim_2401_alpha/description/rviz_model.rviz





















his project was develop with resources available form:
Josh Newans (https://github.com/joshnewans)

And the work done by:

M. O’Kelly, H. Zheng, D. Karthik, and R. Mangharam, “F1tenth: An open-source evaluation environment for continuous control and reinforcement learning,” in NeurIPS 2019 Competition and Demonstration Track. PMLR, 2020,pp. 77–89
