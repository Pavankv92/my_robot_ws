ros2 services can:
    cancel the current execution
    provide feedback during the execution
    handle multiple requests
        replace the current request with new one 

Action Server: accept or reject the goal, feedback if accepted/rejected, feedback during the execution, publish goal status, respond to result Request
    Services : 3X
        accept or reject the goal, feedback if accepted/rejected
        cancel the goal 
        respond to result Request

    Topics : 2X
        publish feedback during the execution,
        publish goal status

Action Client: send a goal, if accepted, send result Request or optionally cancel Request
    Services : 3X
        send a goal
        send result Request 
        cancel Request
    Topics : 2X
        receive feedback
        receive goal status

cli:
    ros2 action list --> /action_name
    ros2 action list -t --> /action_name [interafce/action/type_name]

    ros2 action info /action_name

    by default actions topics/services will not be listed!
    ros2 topic list --include-hidden-topics
    ros2 sevice list --include-hidden-sevices

    ros2 action send_goal /action_name interafce/action/type_name " " --feedback


goal policies :
    goals can be run in parallel
    goal can be rejected while the current goal is being executed.
    Many possibilites! 
