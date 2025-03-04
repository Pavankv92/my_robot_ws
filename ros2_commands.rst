SOURCE :
    underlay : source /opt/ros/<distro>/setup.bash
    overlay : source install/setup.bash 

URDF :
    visualize a URDF model : 
        install : sudo apt install ros-<distro>-urdf-tutorial
        ros2 launch urdf_tutorial display.launch.py model:=my_robot.urdf
    create a URDF Tree :
        install : sudo apt install ros-<distro>-tf2-tools
        while running tf topic, ros2 run tf2_tools view_frames 