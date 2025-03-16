Run:
    ros2 run pkg_name node_name
    ros2 run pkg_name node_name --ros-args  

Node:
    ros2 node list
    ros2 node info /node_name
    launch same node with different name, runtime rename: --remap or -r both works
        ros2 run pkg_name node_name --ros-args --remap __node:=new_node_name

Topics:
    ros2 topic list
    ros2 topic echo /topic_name
    ros2 topic pub /topic_name msg_type data
    ros2 topic info /topic_name
    ros2 hz /topic_name
    remaping : --remap or -r both works
        ros2 run pkg_name node_name --ros-args --r topic_name:=new_topic_name

Rename : Node(publisher/subscriber) and topic both at the runtime, --remap or -r both works
    ros2 run pkg_name node_name --ros-args -r __node:=new_node_name -r topic_name:=new_topic_name


rqt: 
    rqt_graph

Debugging:
    problems can be frustrating sometimes, especially with multiple ROS2 nodes.
    debugging steps
        topic list, node list, info, echo, pub, 
        remappings, rename nodes, Topics
        interface show, 
        rqt_graph