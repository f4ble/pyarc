from ark.cli import *
from ark.rcon import Rcon
from ark.storage import Storage

from factory import Factory
Db = Factory.get('Database')

class EventsPlayerlist(object):
    first_list_players = True

    @classmethod
    def upload_to_web_players_online(cls,player_list):
        Db.website_data_set('players_online', len(Storage.players_online_steam_name))


    @classmethod
    def notify_player_sever_restart(cls,player_list):
        seconds_left, str_countdown = Rcon.get_next_restart_string()
        if seconds_left is None:
            return

        for steam_id in player_list:
            Rcon.message_steam_id(steam_id,'A restart is scheduled in {}'.format(str_countdown),Rcon.none_response_callback)


    @classmethod
    def welcome_message(cls,player_list):
        if cls.first_list_players: #Don't message people when rcon starts. Message when they log on.
            cls.first_list_players = False
            return

        response = 'Welcome to Clash.gg PVP Server.\nAvailable chat commands: !help, !lastseen, !online, !next_restart'
        response_admin = 'Hello admin!'

        for steam_id in player_list:
            if Rcon.is_admin(steam_id=steam_id):
                Rcon.message_steam_id(steam_id,response_admin,Rcon.none_response_callback,echo=False)
            else:
                Rcon.message_steam_id(steam_id,response,Rcon.none_response_callback,echo=False)


    @classmethod
    def add_player_to_database(cls, steam_id, steam_name):
        p, added = Db.create_player(steam_id=steam_id, steam_name=steam_name)
        if added is True:
            debug_out('Adding player to database:', steam_name, steam_id, level=1)
            out('We have a new player! {} ({})'.format(steam_name, steam_id))
        else:
            Db.update_player(steam_id=steam_id,steam_name=steam_name)
            debug_out('Player already in database:', steam_name, steam_id, level=1)


    @classmethod
    def players_disconnected(cls,player_list):
        Db.update_last_seen(player_list.keys())
        if len(player_list) > 1:
            out("** Disconnected: [{} online]".format(len(player_list)))
            for steam_id, name in player_list.items():
                if Rcon.is_admin(steam_id=steam_id):
                    out("\t{} ({}) ADMIN".format(name.ljust(25),steam_id))
                else:
                    out("\t{} ({})".format(name.ljust(25),steam_id))
        elif len(player_list) == 1:
            for steam_id,name in player_list.items():
                if Rcon.is_admin(steam_id=steam_id):
                    out("** Disconnected: {} ({}) ADMIN".format(name,steam_id))
                else:
                    out("** Disconnected: {} ({})".format(name,steam_id))

    @classmethod
    def players_connected(cls,player_list):
        Db.update_last_seen(player_list.keys())
        if len(player_list) > 1:
            out("** Connected: [{} online]".format(len(player_list)))
            for steam_id,name in player_list.items():
                player_name = Storage.players_online_player_name[steam_id]

                if Rcon.is_admin(steam_id=steam_id):
                    out("\t{} {} ({}) ADMIN".format(name.ljust(30), player_name.ljust(30), steam_id))
                else:
                    out("\t{} {} ({})".format(name.ljust(30), player_name.ljust(30), steam_id))
        elif len(player_list) == 1:
            for steam_id in player_list:
                player_name = Storage.players_online_player_name[steam_id]
                if Rcon.is_admin(steam_id=steam_id):
                    out("** Connected: {} {} ({}) ADMIN".format(player_list[steam_id], player_name.ljust(30), steam_id))
                else:
                    out("** Connected: {} {} ({})".format(player_list[steam_id], player_name.ljust(30), steam_id))
