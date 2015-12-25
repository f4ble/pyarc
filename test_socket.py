import time

from ark.config import Config
from ark.steam_socket import SteamSocket
from ark.thread_handler import ThreadHandler


class TestSocket(SteamSocket):
    
        
    @classmethod
    def listen(cls):
        data, err = cls.socket_read()
        if data:
            print(data.decoded['body'])
        else:
            print(err)
        
    @classmethod
    def init(cls):
        print('Connecting:')
        result = cls.socket_connect(Config.rcon_host, Config.rcon_port, timeout=None)
        if result: print('OK')
        
        print('Authenticating:')
        result = cls.socket_auth(Config.rcon_password)
        if result: print('OK')
        
        print('Threading read:')
        ThreadHandler.create_thread(cls.listen)
        
        print('Threading send queue:')
        ThreadHandler.create_thread(cls.loop_process_send_queue)

        for x in range(1,100,1):
            cls.send('listplayers')
            cls.send('getchat')
        
        
            
            
        #packet.response_callback = response_callback
        #self.socket_send(packet)
        time.sleep(1)
        #packet = SteamPacket.pack('getchat',2)
        #packet.response_callback = response_callback
        #self.socket_send(packet)
        
        
        time.sleep(1000)
        
    
TestSocket.init()