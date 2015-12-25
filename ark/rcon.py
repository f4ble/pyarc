"""ARK Survival RCON Interface. Connect, authenticate and transmit data to your favorite ARK Server.

by Torgrim "Fable" Ruud - torgrim.ruud@gmail.com

Class initialization requires host,port and password and will connect to the server unless specified.
Upon connecting commences authentication.

"""

from .cli import *
from .source_server_query import ArkSourceQuery
from .steam_socket import SteamSocket
from .thread_handler import ThreadHandler


class Rcon(SteamSocket):

    @classmethod
    def debug_compare_packet_count(cls):
        out("{} incoming packets and {} outgoing packets".format(len(Rcon.incoming_packets),len(Rcon.outgoing_packets)))
        
    @classmethod
    def init(cls,host,port,password,timeout=None,connect=True):
        if host is None or port is None:
            raise TypeError("Please initialize the rcon module with host and port")
        if password is None:
            raise TypeError("Please provide rcon password")
        
        if connect:
            result, err = cls.socket_connect(host,port,password,timeout)
            if result is True:
                out("Connected")
                cls.auth()
                cls.active_threads()
            else:
                out("Failure to connect: ", err)

    @classmethod
    def default_response_callback(cls,packet):
        out(packet.decoded["body"])

    @classmethod
    def active_threads(cls):
        """Active listening and sending

        Crucial!
        Without this no data is sent or received
        """
        ThreadHandler.create_thread(cls.listen)
        ThreadHandler.create_thread(cls.loop_process_send_queue)

    @classmethod
    def auth(cls):
        out("Authenticating...")

        result, err = cls.socket_auth()
        if result:
            out('Auth successful.')
            #Server may disconnect due to restarts - safest way to ensure up to date data is to query after authentication

            cls.query_server()
            out('Server is running game version:', Storage.query_data['game_version'])
        else:
            out('Auth failed: ', err)
            
    @staticmethod
    def query_server():
        Storage.query_data = ArkSourceQuery.query_info(Config.rcon_host,Config.query_port)
        
    @classmethod    
    def listen(cls):
        packet, err = cls.socket_read()

        if err:
            out("Failure to listen to socket: ", err)
            return False


        debug_out('Packet received.\n\tSent: {}\n\tReceived: {}'.format(packet.data,packet.decoded['body']),level=4)

        Storage.last_recv_packet = time.time()
        Storage.last_recv_packet_body = packet.decoded['body']

        if packet.response_callback is not None:
            packet.response_callback(packet)
        elif packet.keep_alive_packet: #Variable set in steam_packet.py
            debug_out('Keep alive packet',level=2)
            if not Config.keep_alive_packets_output:
                pass
            else:
                if (time.time() - Storage.last_output_unix_time) > Config.show_keep_alive_after_idle:
                    out('[Server Keep Alive]')
        else:
            out("Unhandled response to command {} with messagebody: {}".format(packet.data,packet.decoded["body"]))

        return True
