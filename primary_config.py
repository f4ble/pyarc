from config_base import ConfigBase

class Config(ConfigBase):
    debug_output_level = 0

    log_folder = "D:\\ArkServer\\Arkon\\logs\\"
    rcon_host = "192.168.1.110"
    rcon_password = "Sint"
    rcon_port = 27020
    rcon_socket_timeout = 120
    query_port = 27016

    #This is your base folder and it is used with steamcmd force-install-dir
    path_to_server = "D:\\ArkServer\\"

    #This is prefixed by path_to_server
    server_executable = "\\ShooterGame\\Binaries\\Win64 && start ShooterGameServer.exe"

    #Where you have steamcmd.exe
    path_to_steamcmd = "D:\\ArkServer\\Steam\\"

    #The config folder for your server's ini files
    path_to_config = "D:\\ArkServer\\ShooterGame\\Saved\\Config\\WindowsServer\\"


    # Tested on Windows 7. Used to determine whether server is running and does a regex for ShooterGameServer.exe
    os_process_list_cmd = "tasklist 2>NUL"

    # The parameters used to launch the Ark server. Must include "{repopulate}" in the string.
    # If repopulate flag is true this is replaced with ?ForceRespawnDinos
    shootergameserver_params = '-MapModId=504122600?MaxPlayers=50?QueryPort=27016?Port=27015?GameModIds=536970545,520953653,514701120,509597223,520879363,590665112,600015460{repopulate}?listen -server -log'

    database_connect_string = "mysql+pymysql://fable:asmE23m1yZ9@ssh.fable.no/ark?charset=utf8"
    test_database_connect_string = "mysql+pymysql://fable:asmE23m1yZ9@ssh.fable.no/ark_test?charset=utf8"
