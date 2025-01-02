from launch import LaunchDescription
from launch_ros.actions import Node

# 해당 launch 파일은 두개의 노드를 실행하라고 정의 한 것! 즉 하나의 launch파일로 두개의 노드를 실행시키는 것!
def generate_launch_description(): # LaunchDescription클래스를 빈환
    my_launch = LaunchDescription() # LaunchDescription를 인스턴스화 시켜주고 
    
    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        output='screen',
        parameters=[
            {"background_r": 255},
            {"background_g": 192},
            {"background_b": 203},
        ]
    )
    
    dist_turtle_action_node = Node(
        package='my_first_package',
        executable='dist_turtle_action_server', # 파이썬 파일 이름?
        output='screen',
    )
    
    my_launch.add_action(turtlesim_node)
    my_launch.add_action(dist_turtle_action_node)
    
    return my_launch