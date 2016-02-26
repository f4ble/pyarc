from ark.storage import Storage
from factory import Factory
from ark.rcon import Rcon
from ark.database import Db
from ark.cli import *
from ark.server_control import ServerControl
import time
import re

Config = Factory.get('Config')
Lang = Factory.get('Translation')

class CmdsAdmin(object):


    @staticmethod
    def admin_restart(steam_name,player_name,text):
        if not Rcon.is_admin(steam_name=steam_name):
            out(Lang.get('unauthorized'), cmd)
            return False
        if text.lower().strip() == '!admin_restart now':
            Rcon.message_steam_name(steam_name,Lang.get('issue_restart_now'))
            Rcon.broadcast(Lang.get('restarting'),Rcon.callback_restart())
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

    @staticmethod
    def admin_filter_add(steam_name,player_name,text):
        if not Rcon.is_admin(steam_name=steam_name):
            out(Lang.get('unauthorized'), text)
            return False
        regex =  re.compile('!admin_filter_add (?P<words>[a-z ]+)',re.IGNORECASE)
        matches = regex.search(text)
        if matches is None:
            Rcon.message_steam_name(steam_name,Lang.get('chat_filter_add_no_word'))
            return False
        words = matches.group('words')
        words = words.split()
        result=None
        for word in words:
            res = Db.add_word(word)
            if res is False:
                res = Lang.get('chat_filter_add_word_exists').format(word)
            else:
                res = Lang.get('chat_filter_add_ok').format(word)
            if result is None:
                result = Lang.get('chat_filter_add_result').format(res)
            else:
                result = "{}, {}".format(result,res)
        Rcon.message_steam_name(steam_name,result)

    @staticmethod
    def admin_filter_remove(steam_name,player_name,text):
        if not Rcon.is_admin(steam_name=steam_name):
            out(Lang.get('unauthorized'), text)
            return False
        regex =  re.compile('!admin_filter_remove (?P<words>[a-z ]+)',re.IGNORECASE)
        matches = regex.search(text)
        if matches is None:
            Rcon.message_steam_name(steam_name,Lang.get('chat_filter_remove_no_word'))
            return False
        words = matches.group('words')
        words = words.split()
        result=None
        for word in words:
            res = Db.remove_word(word)
            if res is False:
                res = Lang.get('chat_filter_remove_word_does_not_exists').format(word)
            else:
                res = Lang.get('unauthorized').format(word)
            if result is None:
                result = Lang.get('chat_filter_result').format(res)
            else:
                result = "{}, {}".format(result,res)
        Rcon.message_steam_name(steam_name,result)

    @staticmethod
    def admin_check_version(steam_name,player_name,text):
        if not Rcon.is_admin(steam_name=steam_name):
            out(Lang.get('unauthorized'), text)
            return False
        res, live_version, steam_version = ServerControl.new_version()
        if res is True:
            Rcon.message_steam_name(steam_name,Lang.get('new_version'))
            return True
        else:
            Rcon.message_steam_name(steam_name,Lang.get('no_new_version'))
            return False

    @staticmethod
    def admin_update_now(steam_name,player_name,text):
        if not Rcon.is_admin(steam_name=steam_name):
            out(Lang.get('unauthorized'), text)
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