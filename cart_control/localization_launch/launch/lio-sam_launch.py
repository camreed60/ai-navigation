import os

import launch
import launch.actions
import launch.events

import launch_ros
import launch_ros.actions
import launch_ros.events

from launch import LaunchDescription
from launch_ros.actions import LifecycleNode
from launch_ros.actions import Node

import lifecycle_msgs.msg

from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    ld = launch.LaunchDescription()

    # Static transform publishers (if needed)
    lidar_tf = launch_ros.actions.Node(
        name="lidar_tf",
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=["1", "0", "1.9", "0", "0", "0", "1", "base_link", "velodyne"],
    )

    imu_tf = launch_ros.actions.Node(
        name="imu_tf",
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=["0", "0", "0", "0", "0", "0", "1", "base_link", "imu_link"],
    )

    # LIO-SAM Node
    lio_sam = launch_ros.actions.Node(
        name="lio_sam",
        package="LIO-SAM",  # Adjust if the package name is different
        executable="lio_sam_node",  # Use the correct executable name
        parameters=[LaunchConfiguration('config_file', default='/dev_ws/src/LIO-SAM/config/lio_sam.yaml')],
        remappings=[
            ('/velodyne_points', '/velodyne_points'),
            ('/imu/data', '/zed/zed_node/imu/data')
        ],
        output='screen'
    )

    # Set the default path directly to the specific YAML file location
    localization_param_dir = LaunchConfiguration(
        "localization_param_dir",
        default="/home/jacart2/dev_ws/src/ai-navigation/cart_control/localization_launch/param/localization.yaml",
    )

    lidar_localization = launch_ros.actions.LifecycleNode(
        name="lidar_localization",
        namespace="",
        package="lidar_localization_ros2",
        executable="lidar_localization_node",
        parameters=[localization_param_dir],
        remappings=[
            ("/odom", "/zed_front/zed_node_0/odom"),
            ("/imu/data", "/zed/zed_node/imu/data"),
        ],
        output="screen",
    )

    return launch.LaunchDescription([
        lidar_tf,
        imu_tf,
        lio_sam
    ])
