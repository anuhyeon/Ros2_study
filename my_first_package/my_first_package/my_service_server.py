from my_first_package_msgs.srv import MultiSpawn
from turtlesim.srv import TeleportAbsolute
import rclpy as rp
from rclpy.node import Node

class MultiSpawning(Node):
    def __init__(self):
        super().__init__('multi_spawn')
        self.server = self.create_service(MultiSpawn, 'multi_spawn', self.callback_service) # 우리는 서비스 서버를 만들거다! 거기서 어떤 데이터 타입을 쓸 것이며, 해당 서비스 이름이 뭔지 설정
        # 서버에 또 다른 서버에게 요청을 보낼 클라이언트를 생성한 것!
        self.teleport = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute') # 서비스 클라이언트를 생성 -> 데이터 타입은 TeleportAbsolute이고 서비스 이름은 '/turtle1/teleport_absolute'이다! 해당 클라이언트는 /turtle1/teleport_absolute를 서비스 서버로 하는 노드에게 요청을 보낼 클라이언트라고 생각하면 됨.
        self.req_teleport = TeleportAbsolute.Request()
        
    def callback_service(self, request, response):
        # print('Request :', request)
        
        # response.x = [1., 2., 3.]
        # response.y = [10., 20.]
        # response.theta = [100., 200., 300.]
        self.req_teleport.x = 1.
        self.teleport.call_async(self.req_teleport) # async(비동기) 내가 요청을 보내고 응답이 올때 까지 기다리지 않고 다른 작업을 할 수 있음!
         
        return response # return 값은 클라이언트에게 전달됨.
    
def main(args=None):
    rp.init(args=args)
    multi_spawn = MultiSpawning()
    rp.spin(multi_spawn) # multi_spawn이라는 서비스 서버 객체를 실행
    rp.shutdown()
    
if __name__ == "__main__":
    main()
    
            
            
    