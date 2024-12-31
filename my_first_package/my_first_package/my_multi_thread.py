import rclpy as rp
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from my_first_package.my_publisher import TurtlesimPublisher # cmd_vel 토픽을 발행하는 친구 -> 거북이 뱅글 뱅글 돌게 했던 친구
from my_first_package.my_subscriber import TurtlesimSubscriber # pose 토픽을 구독해서 프린트하는 친구였음.

def main(args=None):
    rp.init()
    
    sub = TurtlesimSubscriber()
    pub = TurtlesimPublisher()
    
    executor = MultiThreadedExecutor()
    
    executor.add_node(sub)
    executor.add_node(pub)
    
    try:
        executor.spin() 
    finally:
        executor.shutdown()
        pub.destroy_node()
        sub.destroy_node()
        rp.shutdown()

if __name__ == "__main__":
    main()
