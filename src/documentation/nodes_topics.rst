Run:
    ros2 run pkg_name node_name
    ros2 run pkg_name node_name --ros-args  

Node:
    ros2 node list
    ros2 node info /node_name
    launch same node with different name, runtime rename: --remap or -r both works
        ros2 run pkg_name node_name --ros-args --remap __node:=new_node_name
        ros2 run pkg_name node_name --ros-args --remap __ns:=/new_name_space


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

leading_slash :
    if you ADD a leading slah to to topic name in the node: 
        self.create_publisher(String, '/my_topic', 10)
        node's snamespace will NOT be added.
    if you DONT ADD a leading slah to to topic name in the node: 
        self.create_publisher(String, 'my_topic', 10)
        leading slash will be automatically added 
        node's snamespace WILL be added.
    recommendation:
        It is recommended NOT to add a leading slash to the topic name in the node.
        This ensures that the namespace is automatically added, making the topic name
        more flexible and consistent with the node's namespace.