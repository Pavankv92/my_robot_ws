rqt:
    install : sudo apt install '~nros-jazzy-rqt*'

rqt_console:
    ros2 run rqt_console rqt_console
    ros2 run package_name node_name --ros-args --log-level WARN