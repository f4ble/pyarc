import time, re
from .storage import Storage
from .rcon import Rcon
from .config import Config
from .cli import *
from .server_control import ServerControl


class Tasks(object):
    _timestamp_get_players = None
    _timestamp_get_chat = None
    
    @staticmethod
    def run_scheduled():
        """Fetch playerlist, chat, run scheduled commands
        
        The logic engine of fetching and storing data from the Ark Server.
        Must be run in a thread.
        
        """
        
        
        if Tasks._timestamp_get_players is None or (Tasks._timestamp_get_players + 30) < time.time():
            Tasks._timestamp_get_players = time.time()
            Rcon.send_cmd('ListPlayers',TaskResponses.list_players)
            time.sleep(0.2)
            
        if Tasks._timestamp_get_chat is None or (Tasks._timestamp_get_chat + 30) < time.time():
            Tasks._timestamp_get_chat = time.time()
            Rcon.send_cmd('GetChat',TaskResponses.get_chat)
            time.sleep(0.2)
        
    @staticmethod
    def run_version_check():
        time.sleep(1800)
        if ServerControl.new_version() is True:
            out('---------- SERVER UPDATE AVAILABLE! (Server on v{}) ---------------'.format(Storage.query_data['game_version']))
        else:
            debug_out('No server update available',level=3)
    
class TaskResponses(object):
    def list_players(packet):
        #Storage.players_online = {'test':'tests'} #Test disconnect
                
        if packet.decoded["body"].strip() == 'No Players Connected':
            player_list = {}
        else:
            body = packet.decoded["body"].split("\n")
            
            rx = re.compile('[\d]+\. (?P<name>[^,]+), (?P<steamid>[\d]+)', re.IGNORECASE)
            player_list = {}
        
            for line in body:
                match = rx.search(line)
                if match is None: #empty string
                    continue
                
                steam_id = match.group("steamid")
                name = match.group("name")
                
                player_list[steam_id] = name
            
        _TaskHelper.list_players_output(player_list)
        Storage.players_online = player_list
        return True
    
    def get_chat(packet):
        if packet.decoded['type'] == 0:
            debug_out("No new chat data.",level=3)
        else:
            latest_chat = packet.decoded['body'].split("\n")
            for line in latest_chat.items():
                line = line.strip()
                if len(line):
                    out(line)
    
    
class _TaskHelper(object):
    def list_players_output(player_list):
        """Output (dis)connected players.
        
        Server only gives us all players.
        With the help of Storage.players_online we can track when a player connects or disconnects
        
        Args:
            dict player_list: k=steam_id v=name
        """
        connected = set(player_list.keys()) - set(Storage.players_online.keys())
        disconnected = set(Storage.players_online.keys()) - set(player_list.keys())
        
        if len(connected) > 1:
            out("** Connected: [{} online]".format(len(player_list)))
            for steam_id in connected:
                name = player_list[steam_id]
                out("\t{} ({})".format(name.ljust(25),steam_id))
        elif len(connected) == 1:
            for steam_id in connected:
                out("** Connected: {} ({})".format(player_list[steam_id],steam_id))
            
        
        if len(disconnected) > 1:
            out("** Disconnected: [{} online]".format(len(player_list)))
            for steam_id in disconnected:
                out("\t{} ({})".format(Storage.players_online[steam_id],steam_id))
        elif len(disconnected) == 1:
            for steam_id in disconnected:
                out("** Disconnected: {} ({})".format(Storage.players_online[steam_id],steam_id))
                
        return True
        
