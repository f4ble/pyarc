"""ARK Survival RCON Interface. Connect, authenticate and transmit data to your favorite ARK Server.

by Torgrim "Fable" Ruud - torgrim.ruud@gmail.com

Class initialization requires host,port and password and will connect to the server unless specified.
Upon connecting commences authentication.

"""

from ark.steam.source_server_query import ArkSourceQuery
from ark.steam.steam_socket import SteamSocket
from .cli import *
from .thread_handler import ThreadHandler


class Rcon(SteamSocket):

    @classmethod
    def debug_compare_packet_count(cls):
        out("{} incoming packets and {} outgoing packets".format(len(Rcon.incoming_packets),len(Rcon.outgoing_packets)))
        
    @classmethod
    def init(cls,host,port,password,timeout=None):
        if host is None or port is None:
            raise TypeError("Please initialize the rcon module with host and port")
        if password is None:
            raise TypeError("Please provide rcon password")

        result, err = cls.socket_connect(host,port,password,timeout)
        if not result:
            cls.reconnect()
        ThreadHandler.create_thread(cls.loop_communication)

    @classmethod
    def default_response_callback(cls,packet):
        out(packet.decoded["body"])

    @staticmethod
    def query_server():
        Storage.query_data = ArkSourceQuery.query_info(Config.rcon_host,Config.query_port)
