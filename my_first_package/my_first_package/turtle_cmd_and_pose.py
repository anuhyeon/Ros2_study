import rclpy as rp
from rclpy.node import Node
from turtlesim.msg import Pose
from my_first_package_msgs.msg import CmdAndPoseVel # 내가 정의한 메세지
from geometry_msgs.msg import Twist


class CmdAndPose(Node):
    def __init__(self):
        super().__init__('turtle_cmd_pose') #turtle_cmd_pose 이름의 노드를 만들겠따!
        self.sub_pose = self.create_subscription(Pose, '/turtle1/pose', self.callback_pose, 10) # Pose 메세지가 callback함수의 인자로 들어감
        self.sub_cmvel = self.create_subscription(Twist, '/turtle1/cmd_vel', self.callback_cmd, 10)
        self.timer_period = 1.0
        self.publisher = self.create_publisher(CmdAndPoseVel,'/cmd_and_pose', 10)
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        self.cmd_pose = CmdAndPoseVel()

    
    def callback_pose(self, msg):
        # print(msg)
        self.cmd_pose.pose_x = msg.x
        self.cmd_pose.pose_y = msg.y
        self.cmd_pose.linear_vel = msg.linear_velocity
        self.cmd_pose.angular_vel = msg.angular_velocity
        print(self.cmd_pose)
    
    def callback_cmd(self, msg):
        self.cmd_pose.cmd_vel_linear = msg.linear.x 
        self.cmd_pose.cmd_vel_angular = msg.angular.z
        
    def timer_callback(self):
        self.publisher.publish(self.cmd_pose)
        
        

def main(args=None):
    rp.init(args=args)
    
    turtle_cmd_pose_node = CmdAndPose()
    rp.spin(turtle_cmd_pose_node)
    
    turtle_cmd_pose_node.destroy_node()
    rp.shutdown()
    

if __name__ == "__main__":
    main()