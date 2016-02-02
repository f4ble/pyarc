from ark.storage import Storage
from ark.cli import *
from ark.database import Db
from ark.rcon import Rcon
from ark.server_control import ServerControl


class EventOther(object):

    @classmethod
    def store_settings_to_db(cls):
        config = ServerControl.get_config()
        Db.website_data_set('Game.ini',config['Game.ini'])
        Db.website_data_set('GameUserSettings.ini',config['GameUserSettings.ini'])
        data = Rcon.query_server()
        Db.website_data_set('game_version',data['game_version'])
        out('Settings uploaded to database.')


    @classmethod
    def get_version(cls):
        data = Rcon.query_server()
        if data:
            out('Server is running game version: ', data['game_version'])
        else:
            out('Unable to retrieve server game version')


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
    def new_ark_version(cls):
        out('---------- SERVER UPDATE AVAILABLE! (Server on v{}) ---------------'.format(Storage.query_data['game_version']))
