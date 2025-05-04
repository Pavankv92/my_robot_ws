What are Lifecycle Nodes in ROS 2?
=================================

in short :
    1. nodes have different states that it can switch to (unconfigured, inactive, active, finalized i.e lifecycle) -- state machine!
    2. lifecycle allows provided easy interfaces to switch/transition between these sates. 

Extra: 
    Lifecycle nodes in ROS 2 provide a managed way to control the state of a node. 
    They are particularly useful in systems where nodes need to be initialized, started, paused, or shut down in a predictable and controlled manner. 
    Below are some key reasons to use lifecycle nodes:

1. **State Management**:
    Lifecycle nodes follow a well-defined state machine, allowing developers to manage the node's behavior during different stages of its lifecycle (e.g., unconfigured, inactive, active, finalized).

2. **Resource Management**:
    By transitioning between states, you can control when resources (e.g., hardware, memory) are allocated and released, improving system efficiency.

3. **Predictable Behavior**:
    Lifecycle nodes provide callbacks for each state transition, enabling predictable and consistent behavior during initialization, activation, and shutdown.

4. **Improved Debugging**:
    The explicit state transitions make it easier to debug and understand the node's behavior, especially in complex systems.

5. **System Integration**:
    Lifecycle nodes are ideal for systems where nodes need to be coordinated, such as in robotics applications where sensors and actuators must be activated in a specific order.

6. **Flexibility**:
    They allow nodes to be paused and resumed without restarting the entire system, which is useful in scenarios like maintenance or dynamic reconfiguration.

Why/When to use Lifecycle Nodes in ROS 2?
=========================================

1. Hardware communication
2. If sw/hw that needs to be initialised in a specific order 
3. Allocate resoruces and memory first
4. Synchronize the initialization between several nodes 


Files :
    1. number_publisher.py 
    2. number_publisher_lifecycle.py 

Code :
    use:
    1. LifecycleNode
    2. create_lifecycle_publisher : Not gonna publish until the LifecycleNode is in active state
    3. **Any callbacks are optional**. Override them only if you want them to.
    
cli :
    1. ros2 lifecycle
        a. toptions : get, list, nodes, set 
    2. ros2 lifecycle nodes --> lists all /lifecycle_node
    3. ros2 lifecycle get /lifecycle_node --> gets the state of the /lifecycle_node
    4. ros2 lifecycle list /lifecycle_node --> lists all the possible states of this node
    5. ros2 lifecycle set /lifecycle_node configure --> sets the configure state to /lifecycle_node
    6. ros2 service list -- > lists the services offered by all the /lifecycle_node

lifecycle manager : A ros2 service manager to manage lifecycle state for a/multiple nodes
    1. change_state
    2. get_state



