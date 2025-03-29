naming convention:
    service:
    service name and service server node name is different!!!
        service name start with verb : "verb_" ex: "add_two_ints"
        callbacks name: callback_service_name : callback_add_two_ints 
client
    use call_async for non-blocking calls : always use call_async

cli :
    ros2 service list
    ros2 service type /service_name
    ros2 service find service_type 
    ros2 service call /service_name service_type "{data: 1}"

    rename:
        ros2 run pkg_name server_node_name --ros-args -r old_service_name:=new_service_name
        ros2 run pkg_name client_node_name --ros-args -r old_service_name:=new_service_name

        service has to be renamed both in server and client!!!

rqt :
    use service plugin