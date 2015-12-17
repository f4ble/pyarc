from ark.scheduler import Scheduler
from ark.cli import *
from ark.rcon import Rcon
from ark.database import Db
from ark.events import Events
from ark.storage import Storage

import re

class Task_GetChat(Scheduler):
    def run(self):
        if len(Storage.players_online):
            Rcon.send_cmd('GetChat',Task_GetChat.parse)
        
    @staticmethod
    def parse(packet):
        """Returns parsed chat data from packet.
        
        Triggers Events.E_CHAT for each line. Arguments: steam_name, player_name, text, line
        
        Syntax per line is: Steam Name (Ingame Name): Text
        
        The return of this function is useful for unit tests.
        
        Returns:
            List: Items are one dictionary per line with keys:
                steam_name, player_name, text, line
                
        """
        results = []
        
        #if packet.decoded['type'] == 0:
        if packet.decoded['body'].lower().strip() == 'server received, but no response!!':
            debug_out("No new chat data.",level=3)
        else:
            latest_chat = packet.decoded['body'].split("\n")
            for line in latest_chat:
                line = line.strip()
                if len(line):
                    regex_server_msg = re.compile('^SERVER: (?P<line>[^\n]+)', re.IGNORECASE)
                    regex_player_msg = re.compile('^(?P<steam_name>.+) \((?P<player_name>[^:]+)\): (?P<line>[^\n]+)')
                    
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