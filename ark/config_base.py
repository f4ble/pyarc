import os
from ark.cli import *


class ConfigBase(object):
    reconnect_wait = 10

    display_output = True
    debug_output_level = 0  # Integer describing level. Default level is 5. More important debug have lower integer. 0 disabled.
    show_settings = True

    debug_output_level_to_log = 0
    log_folder = None

    keep_alive_packets_output = True  # Visible notifaction that connection is alive
    show_keep_alive_after_idle = 600  # 1800 #Prevent keep alive from spamming output

    rcon_host = None
    rcon_password = None
    rcon_port = None
    rcon_socket_timeout = 120
    query_port = None

    # This is your base folder and it is used with steamcmd force-install-dir
    path_to_server = None

    # This is prefixed by path_to_server
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
            out('Created log folder: ', cls.log_folder)
            os.mkdir(cls.log_folder)

    @classmethod
    def printSettings(cls):
        if not cls.display_output:
            return

        print('Settings:')
        print('\tReconnect delay {} seconds.'.format(cls.reconnect_wait))
        print('\tDisplay Keep Alive Packets: {} if idle for {} seconds'.format(cls.keep_alive_packets_output,
                                                                               cls.show_keep_alive_after_idle))
        print('\tOutput enabled: ', cls.display_output)
        print('\tDebug Output level: ', cls.debug_output_level)
        print('\tPath to Server: ', cls.path_to_server)
        print('\tPath to steamcmd: ', cls.path_to_steamcmd)
        print('\tLog folder: {}'.format(cls.log_folder))
        print('')
