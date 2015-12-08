"""
Config file for Arkon

Change name to config.py
"""

class Config(object):
    reconnect_attempts = 30
    reconnect_wait = 10
    
    display_output = True
    debug_output_level = 0    #Integer describing level. Default level is 5. More important debug have lower integer. 0 disabled.
    show_settings = True
    
    keep_alive_packets_output = True #Visible notifaction that connection is alive
    show_keep_alive_after_idle = 1800 #Prevent keep alive from spamming output

    rcon_host = "localhost"
    rcon_password = "Pwd"
    rcon_port = 27020
    query_port = 27016
    rcon_throttle_delay = 1
    
    steam_api_key = "KEY" #Clash.gg
    
    path_to_server = "C:\\ArkServer\\"
    path_to_steamcmd = "C:\\ArkServer\\Steam\\"
        
    
    
if Config.show_settings:    
    print('Settings:')
    print('\tReconnect attempts: {} and wait {} seconds between tries.'.format(Config.reconnect_attempts,Config.reconnect_wait))
    print('\tDisplay Keep Alive Packets: {} if idle for {} seconds'.format(Config.keep_alive_packets_output,Config.show_keep_alive_after_idle))
    print('\tOutput enabled: ',Config.display_output)
    print('\tDebug Output level: ',Config.debug_output_level)
    print('\tSend throttle delay: {} second'.format(Config.rcon_throttle_delay))
    print('\tPath to Server: ',Config.path_to_server)
    print('\tPath to steamcmd: ',Config.path_to_steamcmd)
    print('')