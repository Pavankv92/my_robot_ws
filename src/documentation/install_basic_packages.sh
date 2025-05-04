#!/bin/bash

# Check if ROS2 distro is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <ros2-distro>"
  exit 1
fi

ROS_DISTRO=$1

# Update package list
sudo apt update

# Install ROS2 packages
sudo apt install -y ros-$ROS_DISTRO-xacro
sudo apt install -y python3-colcon-common-extensions
sudo apt install -y ros-$ROS_DISTRO-rqt
sudo apt install -y ros-$ROS_DISTRO-rviz2
sudo apt install -y ros-$ROS_DISTRO-diagnostics
sudo apt install -y ros-$ROS_DISTRO-tf-transformations


echo "Installation of ROS2 packages for $ROS_DISTRO completed."