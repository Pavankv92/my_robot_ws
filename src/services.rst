naming convention:
    service:
        service name start with verb : "verb_" ex: "add_two_ints"
        callbacks name: callback_service_name : callback_add_two_ints 
client
    use call_async for non-blocking calls : always use call_async

cli :
    ros2 service list
    ros2 service type /service_name
    ros2 service find pkg_name/srv/ServiceName
    ros2 service call /service_name pkg_name/srv/ServiceName "{data: 1}"