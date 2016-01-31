from ark.steam.steam_socket import SteamSocket
from ark.cli import *

class RconCommands(SteamSocket):

    @classmethod
    def message_all(cls,message,callback,echo=True):
        if not callable(callback):
            callback = cls.response_callback_response_only

        rcon_cmd = 'serverchat {}'.format(message)

        if echo:
            out('ServerChat: {}'.format(message))

        cls.send(rcon_cmd, callback, priority=True)
        pass

    @classmethod
    def broadcast(cls,message,callback,echo=True):
        if not callable(callback):
            callback = cls.response_callback_response_only

        rcon_cmd = 'broadcast {}'.format(message)

        if echo:
            out('Broadcasting: {}'.format(message))

        cls.send(rcon_cmd, callback, priority=True)
        pass

    @classmethod
    def message_steam_name(cls, steam_name, message, callback=None, echo=True):
        if not callable(callback):
            callback = cls.response_callback_response_only

        rcon_cmd = 'ServerChatToPlayer "{}" {}'.format(steam_name, message)

        if echo:
            out('Messaging {}: {}'.format(steam_name,message))

        cls.send(rcon_cmd, callback, priority=True)
        pass

    @classmethod
    def message_steam_id(cls, steam_id, message, callback=None, echo=True):
        if not callable(callback):
            callback = cls.response_callback_response_only

        rcon_cmd = 'ServerChatTo "{}" {}'.format(steam_id, message)

        if echo:
            out('Messaging {}: {}'.format(steam_id,message))

        cls.send(rcon_cmd, callback, priority=True)
        pass