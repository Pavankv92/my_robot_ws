Params: Each node maintains its own set of parameters.
    ros2 param list
    ros2 param get node_name param_name
    ros2 param set node_name param_name value
    
    dump all params of a node on a screen:
        ros2 param dump node_name
    to a file:
        ros2 param dump node_name > file_name.yaml
        ros2 param load node_name file_name.yaml

    pass param while launching a node:
        ros2 run pkg_name node_name --ros-args -p param_name:=value
    load param file while launching a node:
        ros2 run pkg_name node_name --ros-args --params-file file_name.yaml