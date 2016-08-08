from ark.storage import Storage
from factory import Factory
from tkinter import *

from ark.cli import *

class Control(object):
    @classmethod
    def process_input(cls,event):
        GUI = Factory.get('GUI')
        from ark.input_handler import InputHandler
        if InputHandler.handle_input(GUI.command.get()):
            GUI.command.delete(0,END)


    @classmethod
    def set_last_serverresponse(cls):
        GUI = Factory.get('GUI')
        GUI.last_serverresponse['text'] = time_str()

    @classmethod
    def set_last_keepalive(cls):
        GUI = Factory.get('GUI')
        GUI.last_keepalive['text'] = time_str()

    @classmethod
    def set_config(cls,file):
        GUI = Factory.get('GUI')
        GUI.config['text'] = file

    @classmethod
    def set_server_version(cls,version):
        GUI = Factory.get('GUI')
        GUI.server_version['text'] = version

    @classmethod
    def update_playerlist(cls):
        GUI = Factory.get('GUI')
        GUI.last_player_activity['text'] = time_str()
        GUI.player_list.delete(0,END)
        for steam_id, name in Storage.players_online_steam_name.items():
            GUI.player_list.insert(END,"{} [{}]".format(name,steam_id))
