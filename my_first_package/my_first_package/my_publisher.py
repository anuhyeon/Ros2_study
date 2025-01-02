import rclpy as rp
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class TurtlesimPublisher(Node):
    def __init__(self):
        super().__init__('turtlesim_publisher')
        # self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.publisher = self.create_publisher(Twist, '/turtlesim/turtle1/cmd_vel', 10) # launch 파일에서 namespace를 수정햿을경우 토픽이름을 살짝 수정해줘야함.  
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 2.0
        self.publisher.publish(msg)

def main():
    rp.init()
    
    turtlesim_publisher = TurtlesimPublisher()
    rp.spin(turtlesim_publisher)

    turtlesim_publisher.destroy_node()
    rp.shutdown()

if __name__ == "__main__":
    main()