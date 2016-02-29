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
    
    @staticmethod
    def survey(steam_name,player_name,text):
        regex =  re.compile('!survey (?P<id>[0-9]+)',re.IGNORECASE)
        matches = regex.search(text)
        if matches is not None:
            result=Db.find_survey(matches.group('id'))
        else:
            result=Db.find_survey(None)
        if result is not None:
            options = Db.find_options(result.id)
            if options is not None:
                msg=Lang.get('survey_show').format(result.id,result.question,options,result.id,result.id)
            else:
                msg=Lang.get('survey_show_no_options').format(result.id,result.question)
            Rcon.broadcast(msg,Rcon.response_callback_response_only)
            return True
        else:
            msg=Lang.get('survey_no_found')
            Rcon.message_steam_name(steam_name,msg)
            return False
    
    @staticmethod
    def vote(steam_name,player_name,text):
        regex = re.compile('!vote (?P<id>[0-9]+) (?P<opt>[0-9]+)',re.IGNORECASE)
        matches = regex.search(text)
        if matches is not None:
            res=Db.find_survey(matches.group('id'))
            if res is not None:
                survey_id=res.id
            else:
                survey_id=None
            option = matches.group('opt')
            if Db.option_exists(survey_id,option) is True:
                choice=matches.group('opt')
                player=Db.find_player(steam_name=steam_name)
                steam_id=player.steam_id if player is not None else None
                player_name=player.name if player is not None else None
                if steam_id is not None:
                    result=Db.vote(survey_id,choice,steam_id,player_name)
                    if result is True:
                        msg=Lang.get('survey_vote_ok')
                        result=True
                    else:
                        msg=Lang.get('survey_vote_error')
                        result= False
                else:
                    msg=Lang.get('survey_vote_no_steamid')
                    result= False
            else:
                msg=Lang.get('survey_vote_option_not_found').format(matches.group('opt'))
                result= False
        else:
            msg=Lang.get('survey_vote_syntax_error')
            result= False
        Rcon.message_steam_name(steam_name,msg)
        return result
