Params: runtime parameters for a node -->  Each node maintains its own set of parameters 
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


Node:
    declare_parameter()
    get_parameter()
    node.add_post_parameters_callback()


how do nodes keeps track of their parameters ?
    by adding a trace, with a callback --> node.add_post_parameters_callback()

ROS2 automatically add service server for params:
    /param_publisher/describe_parameters
    /param_publisher/get_parameter_types
    /param_publisher/get_parameters
    /param_publisher/get_type_description
    /param_publisher/list_parameters
    /param_publisher/set_parameters
    /param_publisher/set_parameters_atomically


yaml file:
/node_name:
    ros__parameters:
        number: 8
        timer_period: 0.5 

