URDF : physical description of a robot
    origin in the visual tag represents, CSys of the CG of its own body. 
    origin in the join tag represents TF between 2 links : base_link_TF_second_link
        First set visual tag to zeros --> adjust the joints/TF --> go back adjust the visual
    
    visualize a URDF model : ros2 solution
        install : sudo apt install ros-<distro>-urdf-tutorial
        ros2 launch urdf_tutorial display.launch.py model:=my_robot.urdf
    create a URDF Tree with PDF :
        install : sudo apt install ros-<distro>-tf2-tools
        while running /tf topic, ros2 run tf2_tools view_frames 

TF : relative transforms of various joints in a robot.

Nodes :
    robot_state_publisher node: 
        takes as input: 
            1. urdf as /robot_description
            2. current joint values : /joint_states 
                option 1: comes from a encoder/simulation.
                option 2: Gazebo simulation. 
                option3 : fake it.
                    install : sudo apt install ros-<distro>-joint-state-publisher-gui
                    Run : ros2 run joint_state_publisher_gui joint_state_publisher_gui 
                    this node will listen to /robot_description and provides a gui to control joints, 
                    publishes --> /joint_states 
        publishes: /tf 

    rviz node:
        visualizes the /tf /robot_description