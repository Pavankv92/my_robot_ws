Demonstration of how to include both python and cpp files in the same pkg. 
Files in this package can be used/imported in both python and cpp pkgs.

create pkg:
    ros2 pkg create --build_type ament_cmake my_robot_utils

add python nodes:
    create a folder same as pkg name : my_robot_utils
    create a empty my_robot_utils/__init__.py 

    create a python node:
        my_robot_utils/angle_conversion.py
            create a shabang : #!/usr/bin/env python3

    configure and install python nodes:
        CMakeLists.txt:
            find_package(ament_cmake_python REQUIRED)
            find_package(rclpy REQUIRED)
            find_package(my_robot_interfaces REQUIRED)

            ament_python_install_package(${PROJECT_NAME})

            install(PROGRAMS
            ${PROJECT_NAME}/angle_conversion_server.py
            DESTINATION lib/${PROJECT_NAME}
            )
        package.xml:
            <buildtool_depend>ament_cmake_python</buildtool_depend>
            <depend>rclpy</depend>
            <depend>my_robot_interfaces</depend>



install basic packages
    sudo apt install python3-transforms3d