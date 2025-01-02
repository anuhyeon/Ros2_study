from launch import LaunchDescription
from launch_ros.actions import Node

# 해당 launch 파일은 두개의 노드를 실행하라고 정의 한 것! 즉 하나의 launch파일로 두개의 노드를 실행시키는 것!
def generate_launch_description(): # LaunchDescription클래스를 빈환
    return LaunchDescription( # 해당 클래스안에는 Node를 구성할 수 있음.
        [
            Node( # package='turtlesim 패키지 안에 있는 executable='turtlesim_node' turtlesim_node라는 친구를 namespace= "turtlesim" turtlesim이라는 이름으로 실행해라
                namespace= "turtlesim", package='turtlesim',
                executable='turtlesim_node', output='screen'),
            Node( # my_first_package라는 패키지에 있는 my_publisher 노드를 pub_cmd_vel이라는 이름으로 실행시켜라.
                namespace= "pub_cmd_vel", package='my_first_package',
                executable='my_publisher', output='screen'),
                
        ]
    )