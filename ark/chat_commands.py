from ark.cli import *
from ark.database import Db
from ark.orm_models import *
from ark.rcon import Rcon
from ark.storage import Storage
import re
import time, datetime

class ChatCommands(object):
    test_mode = False #Output response to player instead of Rcon.send_cmd
    
    @staticmethod
    def parse(steam_name,player_name,text):
        #recipient = Db.find_player(player_name=player_name)
        cmd = ChatCommands._find_cmd(text)
        if cmd is False:
            debug_out("Not a chat command: {}".format(text),level=1)
            return False
        
        cmd = cmd.lower()
        debug_out('Processing chat command: ',cmd,level=1)
        if cmd == 'lastseen':
            ChatCommands.last_seen(steam_name,text)
            return True
        elif cmd == 'online':
            ChatCommands.list_online(steam_name)
            return True
        
        return False

    @staticmethod
    def _respond_to_player(steam_name,response):
        """ServerChatToPlayer uses Steam Name - NOT player name!
        
        """ 
        rcon_cmd = 'ServerChatToPlayer "{}" {}'.format(steam_name,response)
        if ChatCommands.test_mode is True:
            print(rcon_cmd)
        else:
            Rcon.send_cmd(rcon_cmd,priority=True)
    
    @staticmethod
    def _find_cmd(text):
        regex = re.compile('^\!(?P<cmd>[a-z]+)',re.IGNORECASE)
        matches = regex.search(text)
        
        if matches is None:
            return False
        
        return matches.group('cmd')
    
    def list_online(recipient):
        player_list = ", ".join(Storage.players_online.values())
        response = '{} players online. ({})'.format(len(Storage.players_online),player_list)
        ChatCommands._respond_to_player(recipient,response)
    
    def last_seen(recipient,text):
        cmdlen = len("!lastseen ")
        name = text[cmdlen:]
        player = Db.find_player_wildcard(name)
        if player is None:
            response = 'Unable to find name: {}'.format(name)
        else:
            date = player.last_seen
            seconds_ago = int(time.time() - date.timestamp())
            ago = time_ago(date.timestamp())
            response = '{} was last seen on the server {} ago ({})'.format(name,ago,date)
            
        ChatCommands._respond_to_player(recipient,response)