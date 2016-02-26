"""ARK Survival RCON Interface. Connect, authenticate and transmit data to your favorite ARK Server.

by Torgrim "Fable" Ruud - torgrim.ruud@gmail.com

Class initialization requires host,port and password and will connect to the server unless specified.
Upon connecting commences authentication.

Through class inheritance you will not need to change core code (steam_socket, steam_socket_core class).
You can just add same name function to this class and use super().function()
This way you can alter without fearing breaking the core functionality.

For easy reading of code all transmittable RCON commands are in class RconCommands
The RCON class is simply just a collection of helper functions and a wrapper for core code.
"""

from ark.rcon_commands import RconCommands
from ark.steam.source_server_query import ArkSourceQuery
from .cli import *
from .thread_handler import ThreadHandler
from ark.storage import Storage
from ark.event_handler import EventHandler
from ark.database import Db
import time
from ark.server_control import ServerControl

from factory import Factory
Config = Factory.get('Config')
Lang = Factory.get('Translation')

class Rcon(RconCommands):

    @classmethod
    def callback_restart(cls,*args):
        """ Callback for broadcast on immediate restarts

        Broadcast does not happen if you restart immedietly
        """
        out('Issuing IMMEDIDATE server restart')
        ServerControl.restart_server()

    @classmethod
    def delayed_restart(cls,minutes, message=""):
        """Delayed restart of the server

        Will restart the server after 5,10,30,60 minutes.
        Notifies the server with broadcast on all these intervals and on 60 seconds

        Args:
            minutes: 5,10,30,60 minutes.

        Returns:
            Result: Bool
            Err: String / None
        """

        minutes = int(minutes)

        if minutes not in [5,10,30,60]:
            err = 'Unable to do delayed restart. Valid waiting times: 5, 10, 30, 60'
            out(err)
            return False, err


        def delayed_message(minutes,message=""):
            if minutes == 60:
                cls.broadcast(Lang.get('restart_default').format('60 minutes',message), cls.response_callback_response_only)
                time.sleep(30*60)
                minutes = 30

            if minutes == 30:
                cls.broadcast(Lang.get('restart_default').format('30 minutes',message), cls.response_callback_response_only)
                time.sleep(20*60)
                minutes = 10

            if minutes == 10:
                cls.broadcast(Lang.get('restart_default').format('10 minutes',message), cls.response_callback_response_only)
                time.sleep(5*60)

            cls.broadcast(Lang.get('restart_default').format('5 minutes',message), cls.response_callback_response_only)
            time.sleep(4*60)

            cls.broadcast(Lang.get('restart_default').format('60 seconds',message), cls.response_callback_response_only)
            time.sleep(50)

            cls.broadcast(Lang.get('restart_default').format('10 seconds',message), cls.response_callback_response_only)
            time.sleep(10)

            Storage.restart_timestamp = None
            ServerControl.restart_server()


        Storage.restart_timestamp = floor(time.time() + (minutes*60))
        callback = lambda:delayed_message(minutes,message)
        ThreadHandler.create_thread(callback,looping=False)
        return True, None

    @classmethod
    def set_next_restart_time(cls,timestamp):
        if timestamp < Storage.restart_timestamp:
            Storage.restart_timestamp = timestamp

    @classmethod
    def get_next_restart_string(cls):
        """Returns SecondsLeft or None, String Formatted Time
        """
        if not Storage.restart_timestamp:
            return None, 'No restart within the next 60 minutes'

        seconds_left = Storage.restart_timestamp - time.time()
        return seconds_left, time_countdown(seconds_left)

    @staticmethod
    def is_admin(steam_id=None, steam_name=None):
        player = Db.find_player(steam_id=steam_id, steam_name=steam_name)
        if not player:
            return False

        if player.admin:
            return True
        return False

    @classmethod
    def reconnect(cls):
        EventHandler.triggerEvent(EventHandler.E_DISCONNECT, Storage.players_online_steam_name)
        Storage.players_online_steam_name = {}
        super().reconnect()

    @staticmethod
    def find_online_steam_id(steam_name=None):
        for steam_id, name in Storage.players_online_steam_name.items():
            if steam_name == name:
                return steam_id
        return None

    @classmethod
    def debug_compare_packet_count(cls):
        out("{} incoming packets and {} outgoing packets".format(len(Rcon.incoming_packets),len(Rcon.outgoing_packets)))
        
    @classmethod
    def init(cls,host,port,query_port,password,timeout=None):
        if host is None or port is None:
            raise TypeError("Please initialize the rcon module with host and port")
        if password is None:
            raise TypeError("Please provide rcon password")

        result, err = cls.socket_connect(host,port,query_port,password,timeout)
        if not result:
            cls.reconnect()

        ThreadHandler.create_thread(cls.listen)
        ThreadHandler.create_thread(cls.loop_communication)

    @classmethod
    def response_callback_default(cls, packet):
        out('> {}\n[Response]: {}'.format(packet.outgoing_command,packet.decoded["body"].strip()))

    @classmethod
    def response_callback_response_only(cls,packet):
        out('[Response]: {}'.format(packet.decoded["body"].strip()))

    @classmethod
    def none_response_callback(cls,packet):
        pass

    @staticmethod
    def query_server():
        Storage.query_data = ArkSourceQuery.query_info(Config.rcon_host,Config.query_port)
        return Storage.query_data
