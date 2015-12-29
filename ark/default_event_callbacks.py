"""Default events for Arkon.

You can make your own file if you want more events.

Definition of arguments in event callbacks sorted by the event type constants in Events class:

E_CONNECT / E_DISCONNECT (player_list):
    List of all players online are stored in Storage.players_online if you need it elsewhere.
    DICT player_list. Key = steam_id, Value = Name

E_CHAT (steam_name, player_name, text, line):
    Parses name from line and separates them into variables.
    The difference between text and line is that line is unparsed includes the names as well.

E_NEW_ARK_VERSION ():
    No arguments.
    
E_NEW_PLAYER (steam_id, name):
    Useful for adding new players to the database or sending them a special welcome message.

E_CHAT_FROM_SERVER (text, line):
    Ark server will return the rcon commands "ServerChatTo" / "ServerChatToPlayer" in getchat.
    This has a seperate event because it should never trigger chat commands or similar events.
    
"""

from ark.chat_commands import ChatCommands
from ark.cli import *
from ark.database import Db
from ark.events import Events
from ark.rcon import Rcon

# noinspection PyUnusedLocal
class EventCallbacks(object):
    """
    Some events return more than one argument. Check *args for more info.
    
    """

    first_list_players = True

    @classmethod
    def init(cls):
        """Add your events here
        
        Function is called at end of script.
        """
        Events.registerEvent(Events.E_CONNECT,EventCallbacks.players_connected)
        Events.registerEvent(Events.E_DISCONNECT,EventCallbacks.players_disconnected)

        Events.registerEvent(Events.E_CONNECT,EventCallbacks.welcome_message)

        Events.registerEvent(Events.E_CHAT,EventCallbacks.output_chat)
        Events.registerEvent(Events.E_CHAT,EventCallbacks.store_chat)
        Events.registerEvent(Events.E_CHAT,EventCallbacks.parse_chat_command)
        
        Events.registerEvent(Events.E_NEW_ARK_VERSION,EventCallbacks.new_ark_version)
        Events.registerEvent(Events.E_NEW_PLAYER,EventCallbacks.add_player_to_database)

    @classmethod
    def welcome_message(cls,player_list):
        if cls.first_list_players: #Don't message people when rcon starts. Message when they log on.
            cls.first_list_players = False
            return

        response = 'Welcome to Clash.gg PVP Server.\nAvailable chat commands: !help, !lastseen, !online'

        for steam_id in player_list:
            rcon_cmd = 'ServerChatTo "{}" {}'.format(steam_id,response)
            Rcon.send(rcon_cmd,Rcon.none_response_callback)

    @classmethod
    def add_player_to_database(cls,steam_id,name):
        p, added = Db.create_player(steam_id,name)
        if added is True:
            debug_out('Adding player to database:',name,steam_id,level=1)
            out('We have a new player! {} ({})'.format(name,steam_id))
        else:
            debug_out('Player already in database:',name,steam_id,level=1)

    @classmethod
    def new_ark_version(cls):
        out('---------- SERVER UPDATE AVAILABLE! (Server on v{}) ---------------'.format(Storage.query_data['game_version']))

    @classmethod
    def output_chat_from_server(cls,text,line):
        out(line)

    @classmethod
    def parse_chat_command(cls,steam_name,player_name,text,line):
        ChatCommands.parse(steam_name,player_name,text)

    @classmethod
    def store_chat(cls,steam_name,player_name,text,line):
        player = Db.find_player(player_name=player_name)
        player_id = player.id if player is not None else None
        Db.create_chat_entry(player_id,player_name,text)

    @classmethod
    def output_chat(cls,steam_name,player_name,text,line):
        out(line)

    @classmethod
    def players_disconnected(cls,player_list):
        Db.update_last_seen(player_list.keys())
        if len(player_list) > 1:
            out("** Disconnected: [{} online]".format(len(player_list)))
            for steam_id in player_list:
                name = player_list[steam_id]
                out("\t{} ({})".format(name.ljust(25),steam_id))
        elif len(player_list) == 1:
            for steam_id in player_list:
                out("** Disconnected: {} ({})".format(player_list[steam_id],steam_id))

    @classmethod
    def players_connected(cls,player_list):
        Db.update_last_seen(player_list.keys())
        if len(player_list) > 1:
            out("** Connected: [{} online]".format(len(player_list)))
            for steam_id in player_list:
                name = player_list[steam_id]
                out("\t{} ({})".format(name.ljust(25),steam_id))
        elif len(player_list) == 1:
            for steam_id in player_list:
                out("** Connected: {} ({})".format(player_list[steam_id],steam_id))
        

EventCallbacks.init()
