import launch 
import launch.launch_description_sources
import launch_ros
from ament_index_python.packages import get_package_share_directory
import launch_ros.parameter_descriptions
import os
from launch.launch_description_sources import PythonLaunchDescriptionSource 

def generate_launch_description():
    #
    robot_name_in_model = "mybot"
    urdf_package_path = get_package_share_directory('mybot_description')
    default_urdf_path = os.path.join(urdf_package_path,'urdf','kr210_robot.urdf')
    #default_rviz_config_path = os.path.join(urdf_package_path,'config','display_robot_model.rviz')
    default_world_path = os.path.join(urdf_package_path,'world','empty.world')
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

    action_launch_gazebo = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            [get_package_share_directory('gazebo_ros'),'/launch','/gazebo.launch.py']),
            launch_arguments=[('world',default_world_path),('verbose','true')]
    )

    spawn_entity_node = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', '/robot_description',
                   '-entity',robot_name_in_model, ]
    )

    return launch.LaunchDescription(
        [
            action_declare_arg_mode_path,
            robot_state_publisher_node,
            action_launch_gazebo,
            spawn_entity_node

        ]
    )
