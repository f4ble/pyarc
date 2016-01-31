from collections import OrderedDict


class Storage(object):
    players_online_steam_name = {}
    players_online_player_name = {}
    
    terminate_application = False  # Threads monitor this variable. Allows graceful exit of application

    last_output_unix_time = 0
    socket_reconnecting = False

    query_data = OrderedDict()

    last_sent_packet = 0
    last_sent_packet_body = None

    last_recv_packet = 0
    last_recv_packet_body = None

    log_file_handle = None
    debug_log_file_handle = None

    repopulate_dinos_on_next_restart = False

    restart_timestamp = None
