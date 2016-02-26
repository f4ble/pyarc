import re

from ark.cli import *
from ark.database import Db
from ark.rcon import Rcon
from ark.storage import Storage
from ark.server_control import ServerControl
from factory import Factory

Lang = Factory.get('Translation')

# noinspection PyUnusedLocal
class ChatCommands(object):
    test_mode = False #Output response to player instead of Rcon.send_cmd
    
    @staticmethod
    def parse(steam_name,player_name,text):
        #recipient = Db.find_player(player_name=player_name)
        cmd = ChatCommands._find_cmd(text)
        if cmd is False:
            debug_out(Lang.get('not_a_command').format(text),level=1)
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
                out(Lang.get('unauthorized'), cmd)
                return False

            if text.lower().strip() == '!admin_restart now':
                Rcon.message_steam_name(steam_name,Lang.get('issue_restart_now'))
                Rcon.broadcast(Lang.get('restarting'))
                ServerControl.restart_server()
                return True

            regex = re.compile('!admin_restart (?P<minutes>[\d]+)',re.IGNORECASE)
            matches = regex.search(text)
            if matches is None:
                Rcon.message_steam_name(steam_name,Lang.get('admin_restart_failed'))
                return False

            minutes = matches.group('minutes')

            result, err = Rcon.delayed_restart(minutes)
            if not result:
                Rcon.message_steam_name(steam_name,'ERROR: {}'.format(err))
                return False

            Rcon.message_steam_name(steam_name,Lang.get('issue_restart'))
            return True
        elif cmd == 'next_restart':
            seconds_left, str_countdown = Rcon.get_next_restart_string()
            response = 'Next restart: {}'.format(str_countdown)
            Rcon.message_steam_name(steam_name,response)
            return True
        elif cmd == 'help':
            Rcon.message_steam_name(steam_name,Lang.get('chat_help'))
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
        players = {}
        for steam_id, steam_name in Storage.players_online_steam_name.items():
            if steam_id in Storage.players_online_player_name and Storage.players_online_player_name[steam_id]:
                players[steam_id] = Storage.players_online_player_name[steam_id]
            else:
                players[steam_id] = steam_name


        player_list = ", ".join(players.values())
        response = Lang.get('chat_players_online').format(len(Storage.players_online_steam_name), player_list)
        Rcon.message_steam_name(recipient,response)

    @staticmethod
    def last_seen(recipient,text):
        cmdlen = len("!lastseen ")
        name = text[cmdlen:]
        player = Db.find_player_wildcard(name)
        if player is None:
            response = Lang.get('chat_last_seen_error').format(name)
        else:
            date = player.last_seen
            seconds_ago = int(time.time() - date.timestamp())
            ago = time_ago(date.timestamp())
            response = Lang.get('chat_last_seen').format(name,ago,date)

        Rcon.message_steam_name(recipient,response)