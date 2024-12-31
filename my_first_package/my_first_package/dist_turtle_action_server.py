import rclpy as rp
from rclpy.action import ActionServer
from rclpy.node import Node
from my_first_package_msgs.action import DistTurtle
import time

class DistTurtleServer(Node):
    def __init__(self):
        super().__init__('dist_turtle_action_server')
        # 누군가가 이 액션 서버에게 request 요청을 한다면 execute_callback함수를 실행해라!
        self.action_server = ActionServer(self, DistTurtle, 'dist_turtle', self.execute_callback) # 액션 서버를 만드는 코드, DistTurtle-> Data definition, dist_turtle --> 내가 만들고자 하는 액션 서버의 이름
        
    def execute_callback(self, goal_handle): # goal_handle은 요청에서 받아오는 것 -> 액션 클라이언트가 요청한 것을 goal_handle인자로 빋이오는 것!
        feedback_msg = DistTurtle.Feedback()
        for n in range(0,10):
            feedback_msg.remained_dist = float(n)
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(0.5)
        
        goal_handle.succeed() # 약간 성공하면 200 실패하면 404 500 느낌이랑 비슷 그냥 성공했다고 클라이언트에게 알려주는 역할일 뿐
        result = DistTurtle.Result()
        
        return result
        
def main(args=None):
    rp.init(args=args)
    dist_turtle_action_server = DistTurtleServer()
    rp.spin(dist_turtle_action_server) # multi_spawn이라는 서비스 서버 객체를 실행
    # rp.shutdown()
    
if __name__ == "__main__":
    main()
    
            