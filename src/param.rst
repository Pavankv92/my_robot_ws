Params:
    ros2 param list
    ros2 param get node_name param_name
    ros2 param set node_name param_name value
    pass param while launching a node:
        ros2 run pkg_name node_name --ros-args -p param_name:=value