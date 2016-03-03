from ark.storage import Storage
from ark.cli import *
from ark.rcon import Rcon
from ark.server_control import ServerControl
from factory import Factory
from pathlib import Path
import os

Config = Factory.get('Config')
Db = Factory.get('Database')

class EventOther(object):

    """ Ark Server savegame integrity filesize check

    Occasionally the savegame is corrupted and a new save is started.
    This is easily detected as the backup savegames are much larger in size.
    Compare size and terminate application if the check fails.
    """
    @classmethod
    def check_savegame_integrity(cls):
        path = os.path.join(Config.path_to_server,'ShooterGame','Saved','SavedArks')

        p = Path(path)
        if not p.is_dir():
            out('EVENT ERROR - Save Game Integrity Check: Unable to locate path: ', path)
            return

        biggest_filesize = 0
        for entry in p.iterdir():
            if not entry.is_file():
                continue
            if str(entry)[-4:] != '.ark':
                continue

            stats = entry.stat()
            if stats.st_size > biggest_filesize:
                biggest_filesize = stats.st_size

        current_save_file = os.path.join(path,'{}.ark'.format(Config.map_name))
        csf = Path(current_save_file)
        if not csf.exists():
            out('EVENT ERROR - Save Game Integrity Check: Unable to find current savegame in path: \n\t{path}\n\tThis may be because of wrong map name in the config variable "map_name" ? It is set to {map}\n'.format(path=current_save_file,map=Config.map_name))
            return

        csf_size = csf.stat().st_size

        threshold_multiplier = 0.9

        if csf_size < (biggest_filesize * threshold_multiplier):
            out('MAJOR PROBLEM: Current savegame filesize is less than 90% of biggest backup. This indicates savegame corruption! Please investigate.')
            Storage.terminate_application = True
            exit()


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
