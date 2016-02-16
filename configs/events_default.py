"""Events for PyArc.

You can make your own files if you want more events.

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

E_RCON_CONNECTED ():
    PyArc is connected to server and authentication is successful.

"""

from ark.event_handler import EventHandler
from ark.events.event_playerlist import EventsPlayerlist
from ark.events.event_chat import EventChat
from ark.events.event_other import EventOther

def init():
    # event_playerlist.py
    EventHandler.registerEvent(EventHandler.E_CONNECT,EventsPlayerlist.players_connected)
    EventHandler.registerEvent(EventHandler.E_CONNECT,EventsPlayerlist.welcome_message)
    EventHandler.registerEvent(EventHandler.E_CONNECT,EventsPlayerlist.notify_player_sever_restart)

    EventHandler.registerEvent(EventHandler.E_DISCONNECT,EventsPlayerlist.upload_to_web_players_online)
    EventHandler.registerEvent(EventHandler.E_CONNECT,EventsPlayerlist.upload_to_web_players_online)

    EventHandler.registerEvent(EventHandler.E_DISCONNECT,EventsPlayerlist.players_disconnected)

    # event_chat.py
    EventHandler.registerEvent(EventHandler.E_CHAT,EventChat.output_chat)
    #EventHandler.registerEvent(EventHandler.E_CHAT,EventChat.store_chat)
    EventHandler.registerEvent(EventHandler.E_CHAT,EventChat.update_player_name)
    EventHandler.registerEvent(EventHandler.E_CHAT,EventChat.parse_chat_command)


    # event_other.py
    EventHandler.registerEvent(EventHandler.E_RCON_CONNECTED,EventOther.get_version)
    EventHandler.registerEvent(EventHandler.E_RCON_CONNECTED,EventOther.store_settings_to_db)
    EventHandler.registerEvent(EventHandler.E_RCON_CONNECTED,EventOther.check_savegame_integrity)

    EventHandler.registerEvent(EventHandler.E_NEW_ARK_VERSION,EventOther.new_ark_version)
    EventHandler.registerEvent(EventHandler.E_NEW_PLAYER,EventOther.add_player_to_database)