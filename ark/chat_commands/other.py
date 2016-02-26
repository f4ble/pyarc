from ark.storage import Storage
from factory import Factory
from ark.rcon import Rcon
from ark.database import Db
from ark.cli import *
import time
import re

Config = Factory.get('Config')
Lang = Factory.get('Translation')

class CmdsOther(object):
    @staticmethod
    def list_online(steam_name,player_name,text):
        players = {}
        for steam_id, p_steam_name in Storage.players_online_steam_name.items():
            if steam_id in Storage.players_online_player_name and Storage.players_online_player_name[steam_id]:
                players[steam_id] = Storage.players_online_player_name[steam_id]
            else:
                players[steam_id] = p_steam_name


        player_list = ", ".join(players.values())
        response = Lang.get('chat_players_online').format(len(Storage.players_online_steam_name), player_list)
        Rcon.message_steam_name(steam_name,response)

    @staticmethod
    def last_seen(steam_name,player_name,text):
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

        Rcon.message_steam_name(steam_name,response)


    @staticmethod
    def next_restart(steam_name,player_name,text):
        seconds_left, str_countdown = Rcon.get_next_restart_string()
        response = 'Next restart: {}'.format(str_countdown)
        Rcon.message_steam_name(steam_name,response)

    @staticmethod
    def help(steam_name,player_name,text):
        Rcon.message_steam_name(steam_name,Lang.get('chat_help'))

    @staticmethod
    def quote(steam_name,player_name,text):
        regex =  re.compile('!quote (?P<id>[0-9]+)',re.IGNORECASE)
        matches = regex.search(text)
        if matches is None:
            Rcon.message_steam_name(steam_name,Lang.get('quote_error'))
            return False
        quote = matches.group('id')
        result = Db.find_quote(quote)
        if result is not None:
            msg = Lang.get('quote_ok').format(quote,result.created,result.name,result.data)
            Rcon.broadcast(msg, Rcon.response_callback_response_only)
            return True
        else:
            Rcon.message_steam_name(steam_name,Lang.get('quote_not_found').format(quote))
            return False
