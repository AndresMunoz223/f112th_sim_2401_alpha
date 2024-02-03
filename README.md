## F1/12th Simulator
ros2 launch f112th_sim_2401_alpha rsp.launch.py use_sim_time:=true
add use_sim_time:=true to use gazebo
ros2 run joint_state_publisher_gui joint_state_publisher_gui
rviz2 -d src/f112th_sim_2401_alpha/description/description.rviz

*pdte robot_core.xacro Inertial stuff



This is a GitHub template. You can make your own copy by clicking the green "Use this template" button.

You need to change the Name Project according to Teams Name (`Alpha`), ensure you do a "Find all" using your IDE (or the built-in GitHub IDE by hitting the `.` key) and rename all instances of `f112th_sim_2401_alpha`.

This project was develop with resources available form:
Josh Newans (https://github.com/joshnewans)

And the work done by:

M. O’Kelly, H. Zheng, D. Karthik, and R. Mangharam, “F1tenth: An open-source evaluation environment for continuous control and reinforcement learning,” in NeurIPS 2019 Competition and Demonstration Track. PMLR, 2020,pp. 77–89
