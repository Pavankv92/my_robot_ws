







CMakeLists.txt :
    INSTALL DIR: whenever a directory is created under a pkg. It needs to be installed in "share", so that it can be found.
        install(
            DIRECTORY urdf launch
            DESTINATION share/${PROJECT_NAME}/
        )

    launch : invoke only those packages that are installed in share

package.xml:
    <exec_depend>ros2launch</exec_depend>


