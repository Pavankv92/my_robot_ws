ros2_control:
    There are 3 main parts of the ros2_control 
        1.  resource manager : talks/manages the HW, provides INTERFACE/api to talk to HW. 
        2.  controller manager : Interacts with resource manager, ros2_control library, loads the appropriate controllers
        3.  controllers : library of different controllers(algorithms)

    HW: can be each individual components / a system 
        Sensor
        Actuator
        System
    
    INTERFACE: of 2 types
        Command interface: to pass commands to HW
        State interface: read current state of the HW
    
    CONTROLLER manager:
        loads different controllers defined in CONTROLLERS --> joint/position controllers etc
    
    CONTROLLER: implements the actual control logics
        position
        velocity
        effort

ros2_control configuration :
    1. connect ros2_control to gazebo via a plugin. 
    2. configure the ros2_control itself (System, resource manager, controller manager)
    3. since there are many params to load, use yaml file to load up params at once