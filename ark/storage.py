from collections import OrderedDict

class Storage(object):
    players_online = {}
    terminate_application = False #Threads monitor this variable. Allows graceful exit of application
    
    last_output_unix_time = 0
    socket_reconnecting = False
    
    query_data = OrderedDict()