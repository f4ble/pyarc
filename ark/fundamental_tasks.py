import time, re
from .storage import Storage
from .rcon import Rcon
from .config import Config
from .cli import *
from .server_control import ServerControl
from .events import Events

class Tasks(object):
    """
    Reponses to these tasks will trigger events.
    Use Events.registerEvent(type,callback) if you plan to add more logic to responses.
    """
    
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
            Events._triggerEvent(E_NEW_ARK_VERSION)
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
            
        connected_ids = set(player_list.keys()) - set(Storage.players_online.keys())
        connected = {}
        for id in connected_ids:
            connected[id] = player_list[id]
        
        disconnected_ids = set(Storage.players_online.keys()) - set(player_list.keys())    
        disconnected = {}
        for id in disconnected_ids:
            disconnected[id] = Storage.players_online[id]
        
        Storage.players_online = player_list
        
        if len(connected):
            Events._triggerEvent(Events.E_CONNECT,connected)
            
        if len(disconnected):
            Events._triggerEvent(Events.E_DISCONNECT,disconnected)
            
            
        return connected,disconnected,Storage.players_online
    
    def get_chat(packet):
        """Returns parsed chat data from packet.
        
        Triggers Events.E_CHAT for each line. Arguments: steam_name, player_name, text, line
        
        The return of this function is useful for unit tests.
        
        Returns:
            List: Items are one dictionary per line with keys:
                steam_name, player_name, text, line
                
        """
        results = []
        if packet.decoded['type'] == 0:
            debug_out("No new chat data.",level=3)
        else:
            latest_chat = packet.decoded['body'].split("\n")
            for line in latest_chat:
                line = line.strip()
                if len(line):
                    regex_server_msg = re.compile('^SERVER: (?P<line>[^\n]+)', re.IGNORECASE)
                    regex_player_msg = re.compile('^(?P<steam_name>[^ ]+) \((?P<player_name>[^ ]+)\): (?P<line>[^\n]+)')
                    
                    server = regex_server_msg.search(line)
                    player = regex_player_msg.search(line)
                    
                    if server is not None:
                        steam_name = 'SERVER'
                        player_name = 'SERVER'
                        text = server.group('line')
                        Events._triggerEvent(Events.E_CHAT_FROM_SERVER,text,line)
                    elif player is not None:
                        steam_name = player.group('steam_name')
                        player_name = player.group('player_name')
                        text = player.group('line')
                        Events._triggerEvent(Events.E_CHAT,steam_name,player_name,text,line)
                    else:
                        out('Unable to parse chat line: ', line)
                        continue
                
                    
                    result = {
                        'steam_name': steam_name,
                        'player_name': player_name,
                        'text': text,
                        'line': line,
                    }
                    results.append(result)
        return results
    