from my_first_package_msgs.srv import MultiSpawn
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import Spawn
import rclpy as rp
from rclpy.node import Node
import numpy as np
import time

class MultiSpawning(Node):
    def __init__(self):
        super().__init__('multi_spawn')
        self.server = self.create_service(MultiSpawn, 'multi_spawn', self.callback_service) # 우리는 서비스 서버(spawn 서비스를 활용하는 약간 중계 서버같은 느낌)를 만들거다! 거기서 어떤 데이터 타입을 쓸 것이며, 해당 서비스 이름이 뭔지 설정
        # 서버에 또 다른 서버에게 요청을 보낼 클라이언트를 생성한 것!
        self.teleport = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute') # 서비스 클라이언트를 생성 -> 데이터 타입은 TeleportAbsolute이고 서비스 이름은 '/turtle1/teleport_absolute'이다! 해당 클라이언트는 /turtle1/teleport_absolute를 서비스 서버로 하는 노드에게 요청을 보낼 클라이언트라고 생각하면 됨.
        self.spawn = self.create_client(Spawn,'/spawn') # Spawn이라는 데이터 타입을 쓰고 있는 '/spawn'이란 서비스 서버(실제 거북이를 원하는 위치로 순간이동 시킴)에 대한 클라이언트를 만들겠다!
        self.req_teleport = TeleportAbsolute.Request()
        self.req_spawn = Spawn.Request()
        
        self.center_x = 5.54
        self.center_y = 5.54
        
    def calc_position(self, n, r): # n: 거북이 개수 r: 반지름
        gap_theta = 2*np.pi / n
        theta = [gap_theta*n for n in range(n)]
        x = [r*np.cos(th) for th in theta]
        y = [r*np.sin(th) for th in theta]
        
        return x, y, theta

        
    def callback_service(self, request, response):
            x, y, theta = self.calc_position(request.num, 3)
            for n in range(len(theta)):
                self.req_spawn.x = x[n] + self.center_x
                self.req_spawn.y = y[n] + self.center_y
                self.req_spawn.theta = theta[n]
                self.spawn.call_async(self.req_spawn)
                time.sleep(0.1)
            
            response.x = x
            response.y = y
            response.theta = theta
            
            # return response

                
        # response.x = [1., 2., 3.]
        # response.y = [10., 20.]
        # response.theta = [100., 200., 300.]
        # self.req_teleport.x = 1.
        # self.teleport.call_async(self.req_teleport) # async(비동기) 내가 요청을 보내고 응답이 올때 까지 기다리지 않고 다른 작업을 할 수 있음!
         
            return response # return 값은 클라이언트에게 전달됨.
    
    
    
def main(args=None):
    rp.init(args=args)
    multi_spawn = MultiSpawning()
    rp.spin(multi_spawn) # multi_spawn이라는 서비스 서버 객체를 실행
    rp.shutdown()
    
if __name__ == "__main__":
    main()
    
            
            
    