Interfaces : 
    ros2 interface list
    ros2 interface show std_msgs/msg/String
    ros2 interface show pkg_name/srv/CustomService
    ros2 interface show pkg_name/action/CustomAction


to create custom interfaces:
    naming conventions : CamelCase.msg


to build custom interfaces: 
    package.xml : add
        <buildtool_depend>rosidl_default_generators</buildtool_depend>
        <exec_depend>rosidl_default_runtime</exec_depend>
        <member_of_group>rosidl_interface_packages</member_of_group>

    REMOVE : IF THERE ARE ERRORS
        <test_depend>ament_lint_auto</test_depend>
        <test_depend>ament_lint_common</test_depend>

    CmakeLists.txt : add
        find_package(rosidl_default_generators REQUIRED)
        rosidl_generate_interfaces(${PROJECT_NAME}
            "msg/Num.msg"
            "msg/Sphere.msg"
            "srv/AddThreeInts.srv"
            DEPENDENCIES geometry_msgs # Add packages that above messages depend on
        )
        ament_export_dependencies(rosidl_default_runtime)


to use custom interfaces:
    add package dependencies 
    
