"""
Config file for PyArc

Recommend changing name to whatever.py
Launch pyarc with: python run.py -cwhatever.py

Be aware: There are integrity checks. Do not make any new variables that are not in ConfigBase

There are many more settings in the config_base.py file that you can override here,
but these are tweaked for maximum performance.
"""

from configs.config_base import ConfigBase

class Config(ConfigBase):
    log_folder = "D:\\PyArc\\logs\\"

    rcon_host = "localhost"
    rcon_password = "MyRconPassword"
    rcon_port = 27020
    query_port = 27016

    #This is your base folder and it is used with steamcmd force-install-dir
    path_to_server = "D:\\ArkServer\\"

    #Needs to contain full path. To start in unblocking in windows use "start C:\path\file.exe"
    server_executable = "start D:\\ArkServer\\ShooterGame\\Binaries\\Win64\\ShooterGameServer.exe"

    #Where you have steamcmd.exe
    path_to_steamcmd = "D:\\ArkServer\\Steam\\"

    #The config folder for your server's ini files
    path_to_config = "D:\\ArkServer\\ShooterGame\\Saved\\Config\\WindowsServer\\"

    # Tested on Windows 7. Used to determine whether server is running and does a regex for ShooterGameServer.exe
    os_process_list_cmd = "tasklist 2>NUL"

    # The parameters used to launch the Ark server. Must include "{repopulate}" in the string.
    # If repopulate flag is true this is replaced with ?ForceRespawnDinos
    shootergameserver_params = 'TheIsland?MaxPlayers=50?QueryPort=27016?Port=27015{repopulate}?listen -server -log'

    database_connect_string = "mysql+pymysql://user:pwd@mysql.host.com/ark?charset=utf8"
