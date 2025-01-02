import rclpy as rp
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from turtlesim.msg import Pose # 터틀심이 발행하는 pose 토픽을 구독하려면 알아야하는 데이터 타입거북이의 x,y 위치를 나타내는 데이터 타입
from geometry_msgs.msg import Twist # cmd_vel 토픽이 사용하는 데이터 타입을 의미
from my_first_package_msgs.action import DistTurtle # 우리가 만들려고 했던 액션 서버가 사용하는 데이터 타입임.
from my_first_package.my_subscriber import TurtlesimSubscriber # 단지 pose를 구독해서 print하는 친구임.
import time
import math

class Turtlesub_Action(TurtlesimSubscriber): # Pose토픽을 구독해서 callback함수로 해당 pose를 출력하는 클래스를 상속받음-> 필드에는 self.subscriber밖에 없음.
    def __init__(self,ac_server): # Turtlesub_Actiond의 인자로 ac_server(DistTurtleServer인스턴스)를 받음 -> DistTurtleServer인스턴스의 필드값을 업데이트 시키기기 위함. 이 작업이 없으면 해당 클래스DistTurtleServer에서 Pose를 구독해서 current_pose를 업데이트 시키는 코드를 추가해줘야함.
        super().__init__() # TurtlesimSubscriber 의 생성자를 상속 받음. 아마, self.subscriber밖에 없을 듯. -> 따라서 이 코드는 /turtle1/pose를 subscribe하는 코드라고 보면됨.
        self.ac_server = ac_server # TurtlesimSubscriber클래스 필드에서 상속받은 거 + 인자로 전달받은 DistTurtleServer인스턴스를 저장하는 변수를 필드에 추가
        
    def callback(self, msg): # 상속받은 self.subscriber = self.create_subscription(Pose, '/turtle1/pose', self.callback,10)에서 실행할 callback함수 오버라이딩
        self.ac_server.current_pose = msg # 이 코드를 거치면 터틀심이 움직일 때마다 ac_server.current_pose속성이 계속 업데이트 되는 것임.
        
class DistTurtleServer(Node):
    def __init__(self):
        super().__init__('dist_turtle_action_server')
        self.total_dist = 0 # 초기값 설정 
        self.is_fisrt_time = True # -> 처음 계산을 할지 말지 플래그 역할을 해주는 친구라고 보면 됨.
        self.current_pose = Pose() # 해당 속성을 다른 인스턴스에서 업데이트 시키기 위해서 Turtlesub_Action클래스에서 했던 작업을 했다고 보면됨.
        self.previous_pose = Pose() # 이전 위치와 다음 위치의 차이를 통해서 움직인 거리를 계산 할 수 있음
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10) # 이 친구를 통해서 거북이가 어떤 각속도와 어떤 선속도로 움직이게 할 수 있음.
         # 누군가가 이 액션 서버에게 request 요청을 한다면 execute_callback함수를 실행해라!
        self.action_server = ActionServer(self, DistTurtle, 'dist_turtle', self.execute_callback) # 액션 서버를 만드는 코드, DistTurtle-> Data definition, dist_turtle --> 내가 만들고자 하는 액션 서버의 이름 , dist_turtlet이름이라는 액션서버로 DistTurtle의 요청이 들어오면 execute_callback함수를 실행
        
    def calc_diff_pose(self):
        if self.is_fisrt_time:
            self.previous_pose.x = self.current_pose.x
            self.previous_pose.y = self.current_pose.y
            self.is_fisrt_time = False
        
        diff_dist = math.sqrt((self.current_pose.x - self.previous_pose.x)**2 + (self.current_pose.y - self.previous_pose.y)**2) # 두 위치간 유클리디안(L2놈)거리 구함.
        self.previous_pose = self.current_pose # 이제 현재 위치는 다음에는 예전 위치가 되니깐 현재 위치를 예전 위치로 저장 시킴.
        
        return diff_dist
        
    def execute_callback(self, goal_handle): # goal_handle은 요청에서 받아오는 것 -> 액션 클라이언트가 요청한 것을 goal_handle인자로 빋이오는 것!
        feedback_msg = DistTurtle.Feedback() # 액션 타입(DistTurtle.action)에서 Feedback 부분을 가져옴.
        
        msg = Twist() # cmd_vel 값
        msg.linear.x = goal_handle.request.linear_x # 사용자가 요청한 선속도(거북이를 이 속도로 움직여주세요)를 cmd_vel 메세지에 업데이트 -> 나중에 이걸 publish하면 사용자 요청대로 거북이가 움직이겠지?
        msg.angular.x = goal_handle.request.angular_z
        
        while True: # 0.01초마다 publish, feedbacl 힘.
            self.total_dist += self.calc_diff_pose() # 지금까지 거북이가 음직인 거리 계산
            feedback_msg.remained_dist = goal_handle.request.dist - self.total_dist
            goal_handle.publish_feedback(feedback_msg) # 이 코드는 클라이언트에게 feedback_msg를 publish 하는 코드임.
            self.publisher.publish(msg) # 실제로 터틀심 거북이에게 클라이언트가 요청한 대로 거북이가 움직이도록 cmd_vel토픽으로 publish 함.
            time.sleep(0.01)
            
            if feedback_msg.remained_dist < 0.2:
                break
        
        goal_handle.succeed()
        result = DistTurtle.Result()
        
        result.pos_x = self.current_pose.x
        result.pos_y = self.current_pose.y
        result.pos_thera = self.current_pose.theta
        result.result_dist = self.total_dist # 총 움직인 거리
        
        # 아래는 다음을 위한 초기화 하는 코드
        self.total_dist = 0
        self.is_fisrt_time = True
        
        # for n in range(0,10):
        #     feedback_msg.remained_dist = float(n)
        #     goal_handle.publish_feedback(feedback_msg)
        #     time.sleep(0.5)
        
        # goal_handle.succeed() # 약간 성공하면 200 실패하면 404 500 느낌이랑 비슷 그냥 성공했다고 클라이언트에게 알려주는 역할일 뿐
        # result = DistTurtle.Result()
        
        return result
        
def main(args=None):
    rp.init(args=args)
    
    executor = MultiThreadedExecutor() # 멀티 스레딩 하기 위해서
    
    dist_turtle_action_server = DistTurtleServer() # dist_turtle_action_server해당 클래스를 TurtlesimSubscriber을 상속받은 클래스에서서 인자로 주면서 특정 dist_turtle_action_server의 필드 값을 업데이트 시키려고!
    sub = Turtlesub_Action(ac_server = dist_turtle_action_server) # 인자로 액션서버 인스턴스를 받아 해당 TurtlesimSubscriber를 상속받은 클래스에서 사용하기 위함.
    
    executor.add_node(dist_turtle_action_server)
    executor.add_node(sub)
    
    try:
        executor.spin()
        #rp.spin(dist_turtle_action_server) # multi_spawn이라는 서비스 서버 객체를 실행
        # rp.shutdown()
    finally:
        executor.shutdown()
        sub.destroy_node()
        dist_turtle_action_server.destroy_node()
        rp.shutdown()
    
if __name__ == "__main__":
    main()
    
            