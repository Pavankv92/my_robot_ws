Topics : Pubslishes/Subscriber --> data streams

Services : client/Server --> for quick computations or actions

Actions: client/Server --> for longer actions, with cancel, feedback etc.

publisher:
    publish a msg of some_type, under the some_topic_name at some_frequency.
        some_frequency : needs some form of time control --> create_timer(period, callback)
        callback : publishes everytime its called

Subscriber:
    always listen to some_topic_name and receive the msg of type some_type as and when they come
        always : no timer needed
        as and when they come --> callback to catch msg object

Service Server:
    offer a service to do something --> clients see this offer and sends request.
    process clients request as and when they come --> need a callback

Service Client :
    create a request, send the request and wait for the server to process and receive the response in the future. 
        wait for the server to process --> some form of waiting mechanism 
        receive the response --> set up a callback  
        response in the future --> use future object


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
