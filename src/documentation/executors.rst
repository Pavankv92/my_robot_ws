Main callbacks in ROS2:
    1. timers
    2. subscribers
    3. service servers
    4. action servers
    5. future (in clients)

under the hood:
    1. rclpy.init() --> Initialize ROS communications for a given context
    2. rclpy.shutdown() -- > Shutdown a previously initialized context. This will also shutdown the global executor
    3. rclpy.spin(node, executor): (don't use for multiple threads)
        a. Execute work and block until the context associated with the executor is shutdown.
        b. create a executor, defualt if not provided
        c. Provided executor will execute Callbacks 
            1. uses executor.spin_once() --> executes a single callback, and *sequentially* when there are multiple callbacks
        d. This function blocks.
            :param node: A node to add to the executor to check for work.
            :param executor: The executor to use, or the global executor if ``None``. 

spin(): run spin_once() in a while loop
    while some_conditions:
        spin_once()

single threaded executor:
    executor.spin() --> executes a single callback, and *sequentially* when there are multiple callbacks 
        see single_threaded_executor.py

multi threaded executor:  
    needs a callback_group --> defualt MutuallyExclusiveCallbackGroup if not provided
        1. each callback_group is executed in parallel, each callback_group can have multiple callbacks inside
        2. ReentrantCallbackGroup() : 
            execute all the callbacks in this group in parallel! 
            not only this, each callback can be executed multiple times (reenter) in parallel!
        3. MutuallyExclusiveCallbackGroup : 
            execute all the callbacks in this group sequentially only ONCE. cannot reenter
            just as running a single threaded but in a separate thread in parallel to other threads
            DON'T add multiple callbacks in this group!!! only one will be run

        see multi_threaded_executor.py

when to use what ? :
    