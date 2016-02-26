import os
import argparse
from factory import Factory

class ConfigBase(object):
    reconnect_wait = 10

    language_file = 'english'

    #Customize your tasks/events/input/etc by overriding and creating new files. Beware some of these contain core functionality.
    tasks_config = 'tasks_default'
    events_config = 'events_default'
    input_config = 'input_default'
    chatcmds_config = 'chatcmds_default'

    display_output = True
    debug_output_level = 0  # Integer describing level. Default level is 5. More important debug have lower integer. 0 disabled.
    show_settings = True

    debug_output_level_to_log = 0
    log_folder = None

    rcon_host = None
    rcon_password = None
    rcon_port = None
    rcon_socket_timeout = 1
    query_port = None

    # This is your base folder and it is used with steamcmd force-install-dir
    path_to_server = None

    #Needs to contain full path. To start in unblocking in windows use "start C:\path\file.exe"
    server_executable = None

    # Where you have steamcmd.exe
    path_to_steamcmd = None

    # The config folder for your server's ini files
    path_to_config = None

    # Tested on Windows 7. Used to determine whether server is running and does a regex for ShooterGameServer.exe
    os_process_list_cmd = "tasklist 2>NUL"

    # The parameters used to launch the Ark server. Must include "{repopulate}" in the string.
    # If repopulate flag is true this is replaced with ?ForceRespawnDinos
    shootergameserver_params = None

    # Map the server runs. This is to check integrity of save game. If a save is corrupted the game server starts a new
    # save game. Must be identical to the map name in .ark save file. Example: TheIsland
    map_name = 'TheIsland'

    """
    Database settings
    
    Args:
        database_connect_string:
            NB: Reccommend using mysql+pymysql:// - I had trouble with the default mysql driver
            
            Examples:
                mysql://scott:tiger@hostname/dbname
                http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html#database-urls
        
        database_connect_params (kwargs):
            Any params accepted by sqlalchemy.create_engine
            http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html#sqlalchemy.create_engine
            
        
    """
    database_connect_string = None
    test_database_connect_string = None

    database_connect_params = {"echo": False}
    active_player_timeframe = 604800  # Any player who has logged on within this timeframe is considered an active player. 604800 = 1 week


    @classmethod
    def create_log_folder(cls):
        if cls.log_folder and (
                        os.path.exists(cls.log_folder) is False or os.path.isdir(cls.log_folder) is False):
            print('Created log folder: ', cls.log_folder)
            os.mkdir(cls.log_folder)

    @classmethod
    def printSettings(cls):
        if not cls.display_output:
            return

        print('Settings:')
        print('\tReconnect delay {} seconds.'.format(cls.reconnect_wait))
        print('\tOutput enabled: ', cls.display_output)
        print('\tDebug Output level: ', cls.debug_output_level)
        print('\tPath to Server: ', cls.path_to_server)
        print('\tPath to steamcmd: ', cls.path_to_steamcmd)
        print('\tLog folder: {}'.format(cls.log_folder))
        print('')

    def configIntegrityCheck(Config):
        baseNames = dir(ConfigBase)
        failed = False
        names = []
        for name in dir(Config):
            if name not in baseNames:
                names.append(name)
                failed = True
        if failed:
            print('Config integrity check failed. You have config variables not matched with config_base.py:')
            print(', '.join(names))
            exit()

    def configRequiredCheck(Config):
        assert type(Config.log_folder) is str and not '', 'Config failure: log_folder not defined'
        assert type(Config.rcon_host) is str and not '', 'Config failure: rcon_host not defined'
        assert type(Config.rcon_password) is str and not '', 'Config failure: rcon_password not defined'
        assert type(Config.rcon_port) is int and not 0, 'Config failure: rcon_port not defined'
        assert type(Config.query_port) is int and not 0, 'Config failure: query_port not defined'
        assert type(Config.path_to_server) is str and not '', 'Config failure: path_to_server not defined'
        assert type(Config.server_executable) is str and not '', 'Config failure: server_executable not defined'
        assert type(Config.path_to_steamcmd) is str and not '', 'Config failure: path_to_steamcmd not defined'
        assert type(Config.path_to_config) is str and not '', 'Config failure: path_to_config not defined'
        assert type(Config.os_process_list_cmd) is str and not '', 'Config failure: os_process_list_cmd not defined'
        assert type(Config.shootergameserver_params) is str and not '', 'Config failure: shootergameserver_params not defined'
        assert type(Config.database_connect_string) is str and not '', 'Config failure: database_connect_string not defined'

    @classmethod
    def load_config(cls,verbose=True):
        parser = argparse.ArgumentParser()
        parser.add_argument('-c','--config')
        args = parser.parse_args()

        if not args.config:
            print('Missing -c[config file]')
            exit()

        file = args.config.replace('.py','')
        pathfile = 'configs/{}.py'.format(file)
        if not os.path.isfile(pathfile):
            exit('Config file "{}" does not exist'.format(pathfile))

        config_file = "configs.{}".format(file)

        if not config_file:
            exit('Please supply a config file. Example: python run.py my_config (without .py)\n')

        if verbose:
            print('Loading config: {}'.format(file))

        try:
            current_config = __import__(config_file,fromlist="Config")
        except ImportError:
            print('Unable to load config.')
            raise

        cls.configIntegrityCheck(current_config.Config)
        cls.configRequiredCheck(current_config.Config)

        Factory.set('Config',current_config.Config)
        if verbose:
            print('Config loaded')
