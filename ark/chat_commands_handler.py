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
