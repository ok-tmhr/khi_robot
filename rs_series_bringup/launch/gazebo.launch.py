import os

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    pkg_description = get_package_share_directory("rs_series_bringup")

    robot_description = xacro.process_file(
        os.path.join(pkg_description, "urdf", "rs007l.gz.urdf.xacro")
    ).toxml()

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}, {"use_sim_time": True}],
        output="screen",
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py"
            )
        ),
        launch_arguments={"gz_args": "empty.sdf"}.items(),
    )

    spawn = Node(
        package="ros_gz_sim",
        executable="create",
        parameters=[{"topic": "/robot_description"}],
        output="screen",
    )

    return LaunchDescription([robot_state_publisher, gazebo, spawn])
