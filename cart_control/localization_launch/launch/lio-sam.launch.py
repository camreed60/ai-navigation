import launch
import launch_ros.actions
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

def generate_launch_description():
    # LIO-SAM Parameter File (Ensure this exists)
    lio_sam_config = "/dev_ws/src/LIO-SAM/config/lio_sam.yaml"

    # Declare arguments (optional, useful if you want to change parameters dynamically)
    declare_config_arg = DeclareLaunchArgument(
        "config_file",
        default_value=lio_sam_config,
        description="Path to LIO-SAM configuration file"
    )

    # Static Transform Publisher for LiDAR (Adjust transform if necessary)
    lidar_tf = Node(
        name="lidar_tf",
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=["1", "0", "1.9", "0", "0", "0", "1", "base_link", "velodyne"],
        output="screen"
    )

    # Static Transform Publisher for IMU
    imu_tf = Node(
        name="imu_tf",
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=["0", "0", "0", "0", "0", "0", "1", "base_link", "imu_link"],
        output="screen"
    )

    # LIO-SAM Node
    lio_sam = Node(
        package="lio_sam",  # Ensure this matches your package name
        executable="lio_sam_node",  # Ensure this is the correct executable
        name="lio_sam",
        parameters=[lio_sam_config],  # Directly passing the path
        remappings=[
            ("/velodyne_points", "/velodyne_points"),  # Ensure these match expected topics
            ("/imu/data", "/zed/zed_node/imu/data")
        ],
        output="screen",
        emulate_tty=True  # Enables color logs in the terminal
    )

    return LaunchDescription([
        declare_config_arg,
        lidar_tf,
        imu_tf,
        lio_sam
    ])
