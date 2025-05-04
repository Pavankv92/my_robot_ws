Sourcing:
    underlay : source /opt/ros/<distro>/setup.bash
    overlay : source my_robot/install/setup.bash 
    smylink : source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash

Pkg:
    ros2 pkg create --build-type ament_python robot_descripton

Build: Build will install the executables in the install directory defined in setup.cfg file
    always build from the _ws directory
    colcon build
    colcon build --packages-select <pkg_name>
    colcon build --symlink-install

names : keep the same name for filenname, nodename, executable name.

passing arguments at cli :
    any argument : --ros-args 
    param as an argument : --ros-args -p 


