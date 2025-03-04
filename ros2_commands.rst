SOURCE:
    underlay : source /opt/ros/<distro>/setup.bash
    overlay : source my_robot/install/setup.bash 

BUID: 
    always build from the _ws directory
    colcon build

PKG:
    ros2 pkg create --build-type ament_python robot_descripton

passing arguments at cli :
    any argument : --ros-args 
    param as an argument : --ros-args -p 

INSTALL DIR: whenever a directory is created under a pkg. It needs to be installed in "/opt/ros/jazzy/share", so that it can be found.
    install(
        DIRECTORY urdf launch
        DESTINATION share/${PROJECT_NAME}/
    )

launch : invoke only those packages that are installed in share
