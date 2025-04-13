xml:
    <node pkg='pkg_name' exec='executable_name' name='remapping_name'>
        <remap from='old_topic_name' to='new_topic_name' />
        <param name='' value=/>

    </node>

    with a new namespace:
    <node pkg='pkg_name' exec='executable_name' name='remapping_name' namespace='/new_name_space'>
        <remap from='old_topic_name' to='new_topic_name' />
        <param name='' value=/>

    </node>

python:
    complicated! TODO : check which launch files are common in ROS2 --> Python launch files are used all over!
    ramappings= [('old_topic_name', 'new_topic_name')] --> [()] 
    parameters= [{'param_name' : value}] --> [{}]
    parameters= ['path_to_config_file'] 
    namespace='/new_name_space'


params/config:
    create yaml file

namespaces:
    /new_name_space

declaring launch argument to pass cmd arguements while launching launch files
    turtlesim_ns_launch_arg = DeclareLaunchArgument(
        'turtlesim_ns',
        default_value='turtlesim1'
    )

    turtlesim_node = Node(
        package='turtlesim',
        namespace=turtlesim_ns,
        executable='turtlesim_node',
        name='sim'
    )

    cmd : 
        check : os2 launch launch_tutorial example_substitutions_launch.py --show-args

            Arguments (pass arguments as '<name>:=<value>'):

            'turtlesim_ns':
                no description given
                (default: 'turtlesim1')


        launch : ros2 launch launch_tutorial example_substitutions_launch.py turtlesim_ns:='turtlesim3' 
        use LaunchConfiguration('turtlesim_ns') to access the config value that was declared

CMakeLists.txt :
    INSTALL DIR: whenever a directory is created under a pkg. It needs to be installed in "share", so that it can be found.
        install(
            DIRECTORY urdf launch
            DESTINATION share/${PROJECT_NAME}/
        )

    launch : invoke only those packages that are installed in share

package.xml:
    <exec_depend>ros2launch</exec_depend>


