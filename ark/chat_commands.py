import re

from ark.cli import *
from ark.database import Db
from ark.rcon import Rcon
from ark.storage import Storage
from ark.server_control import ServerControl

# noinspection PyUnusedLocal
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
        elif cmd == 'admin_restart':
            if not Rcon.is_admin(steam_name=steam_name):
                out('UNAUTHORIZED ACCESS TO CHAT COMMAND: ', cmd)
                return False

            Rcon.message_steam_name(steam_name,'Issuing server restart')
            ServerControl.restart_server()
            return True
        elif cmd == 'help':
            Rcon.message_steam_name(steam_name,'Supported commands are: !online, !lastseen')
            return True
        return False

    @staticmethod
    def _find_cmd(text):
        regex = re.compile('^!(?P<cmd>[a-z_]+)',re.IGNORECASE)
        matches = regex.search(text)

        if matches is None:
            return False

        return matches.group('cmd')

    @staticmethod
    def list_online(recipient):
        player_list = ", ".join(Storage.players_online.values())
        response = '{} players online. ({})'.format(len(Storage.players_online),player_list)
        Rcon.message_steam_name(recipient,response)

    @staticmethod
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

        Rcon.message_steam_name(recipient,response)