"""Default events for Arkon.

You can make your own file if you want more events.

Definition of arguments in event callbacks sorted by the event type constants in Events class:

E_CONNECT / E_DISCONNECT (player_list):
    List of all players online are stored in Storage.players_online if you need it elsewhere.
    DICT player_list. Key = steam_id, Value = Name

E_CHAT (name, line):
    Parses name from line and separates them into two variables.
    name: Name of player
    line: What was said

E_NEW_ARK_VERSION ():
    No arguments.
    
E_NEW_PLAYER (steam_id, name):
    New players are automatically added to database table players. 
    steam_id, name

"""

from ark.events import Events
from ark.storage import Storage
from ark.cli import *

class EventCallbacks(object):
    """
    Some events return more than one argument. Check *args for more info.
    
    """
    
    def new_ark_version():
        out('---------- SERVER UPDATE AVAILABLE! (Server on v{}) ---------------'.format(Storage.query_data['game_version']))
    
    def parse_chat_command(name,line):
        pass
        
    def output_chat(name,line):
        out(line)
        
    def players_disconnected(player_list):
        if len(player_list) > 1:
            out("** Disconnected: [{} online]".format(len(player_list)))
            for steam_id in player_list:
                name = player_list[steam_id]
                out("\t{} ({})".format(name.ljust(25),steam_id))
        elif len(player_list) == 1:
            for steam_id in player_list:
                out("** Disconnected: {} ({})".format(player_list[steam_id],steam_id))
                
    def players_connected(player_list):
        if len(player_list) > 1:
            out("** Connected: [{} online]".format(len(player_list)))
            for steam_id in player_list:
                name = player_list[steam_id]
                out("\t{} ({})".format(name.ljust(25),steam_id))
        elif len(player_list) == 1:
            for steam_id in player_list:
                out("** Connected: {} ({})".format(player_list[steam_id],steam_id))
        


Events.registerEvent(Events.E_CONNECT,EventCallbacks.players_connected)
Events.registerEvent(Events.E_DISCONNECT,EventCallbacks.players_disconnected)
Events.registerEvent(Events.E_CHAT,EventCallbacks.output_chat)
Events.registerEvent(Events.E_CHAT,EventCallbacks.parse_chat_command)
Events.registerEvent(Events.E_NEW_ARK_VERSION,EventCallbacks.new_ark_version)
