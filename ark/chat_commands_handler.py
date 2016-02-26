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

    cmds_regex = {}
    cmds = {}

    @classmethod
    def register_chat_command_regex(cls,pattern,callback):
        cls.cmds_regex[pattern] = callback

    @classmethod
    def register_chat_command(cls,text,callback):
        cls.cmds[text] = callback

    @classmethod
    def process_chat(cls,steam_name,player_name,text):
        callback = cls._match_cmd_regex(text)
        if callback:
            return callback(steam_name,player_name,text)

        callback = cls._match_cmd(text)
        if callback:
            return callback(steam_name,player_name,text)

    @classmethod
    def _match_cmd(cls,text):
        """ Search non-regex commands for text

        Returns callback or None
        """
        text = text.strip()
        for cmd,callback in cls.cmds.items():
            if text == cmd:
                return callback

    @classmethod
    def _match_cmd_regex(cls,text):
        """ Search regex commands for text

        Returns callback or None
        """
        text = text.strip()

        for pattern,callback in cls.cmds_regex.items():
            full_pattern = '^(?P<cmd>{})'.format(pattern)
            regex = re.compile(full_pattern,re.IGNORECASE)
            matches = regex.search(text)
            if matches:
                return callback
            print('Failed Match: {} - {}'.format(full_pattern,text))

"""



        elif cmd == 'admin_update_now':
            if not Rcon.is_admin(steam_name=steam_name):
                out(Lang.get('unauthorized'), cmd)
                return False
            res, live_version, steam_version = ServerControl.new_version()
            if res is True:
                ServerControl.update_and_restart_server()
                Rcon.message_steam_name(steam_name,Lang.get('update_restart'))
                Rcon.broadcast(Lang.get('update_restart'), Rcon.response_callback_response_only)
                return True
            else:
                Rcon.message_steam_name(steam_name,Lang.get('no_new_version'))
                return False
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
"""