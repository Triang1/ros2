import launch 
import launch_ros
from ament_index_python.packages import get_package_share_directory
import launch_ros.parameter_descriptions
import os

def generate_launch_description():
    #
    urdf_package_path = get_package_share_directory('mybot_description')
    default_urdf_path = os.path.join(urdf_package_path,'urdf','kr210_robot.urdf')
    default_rviz_config_path = os.path.join(urdf_package_path,'config','display_robot_model.rviz')
    #
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name='model', default_value=str(default_urdf_path),
        description='URDF的绝对路径')
    
    robot_description = launch_ros.parameter_descriptions.ParameterValue(
        launch.substitutions.Command(
            ['cat ', launch.substitutions.LaunchConfiguration('model')]),
        value_type=str)

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description':robot_description}]
        )

    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        )

    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d',default_rviz_config_path]
        )

    return launch.LaunchDescription(
        [
            action_declare_arg_mode_path,
            joint_state_publisher_node,
            robot_state_publisher_node,
            rviz_node
        ]
    )
