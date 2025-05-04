debugging tools:
    rqt_graph and many plugins 
    log messages : rqt_colsole
    ros2 
        ros2 doctor : 
            while no nodes are running, it checks the ros2 system itself
            while nodes are running, it checks the nodes and the system
        ros2 doctor --report : generates a report
        ros2 doctor --report --output-file file_name : saves the report to a file
        ros2 doctor --report --output-file file_name --format markdown : saves the report in markdown format
        ros2 doctor --report --output-file file_name --format markdown --verbose : saves the report in markdown format with verbose output