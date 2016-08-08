from ark.storage import Storage
from factory import Factory
from tkinter import *
GUI = Factory.get('GUI')
from ark.cli import *

class Control(object):

    @classmethod
    def set_last_serverresponse(cls):
        GUI.last_serverresponse['text'] = time_str()

    @classmethod
    def set_last_keepalive(cls):
        GUI.last_keepalive['text'] = time_str()

    @classmethod
    def set_config(cls,file):
        GUI.config['text'] = file

    @classmethod
    def set_server_version(cls,version):
        GUI.server_version['text'] = version

    @classmethod
    def update_playerlist(cls):
        GUI.last_player_activity['text'] = time_str()
        GUI.player_list_value.delete(0,END)
        for steam_id, name in Storage.players_online_steam_name.items():
            GUI.player_list.insert(END,"{} [{}]".format(name,steam_id))
