"""List of useful ARK Server commands

ListPlayers

GetChat
Broadcast <MessageText>
ServerChat <MessageText>
ServerChatTo <SteamID> <MessageText>
ServerChatToPlayer <PlayerName> <MessageText>

ShowMessageOfTheDay
KickPlayer <steam_id>
DestroyWildDinos


SaveWorld
DoExit
"""

from .thread_handler import ThreadHandler
from .cli import *
from .rcon import Rcon
from .config import Config
from .storage import Storage
from .server_control import ServerControl
class InputHandler(object):
    @staticmethod
    def init():
        th = ThreadHandler.create_thread(InputHandler._listen)
    
    def _listen():
        command = input()
        InputHandler.parse_command(command)
        
    def parse_command(text):
        words = text.strip().split(' ')
        cmd = words[0].lower()
        
        if cmd == "":
            return
        elif cmd == 'exit':
            Storage.terminate_application = True
        elif cmd == 'check_version':
            res = ServerControl.new_version()
            out('New version available' if res is True else 'No new version')
        elif cmd == 'version':
            out('Server is running game version:',Storage.query_data['game_version'])
        elif cmd == 'saveworld':
            Rcon.send_cmd('saveworld',InputResponses._default)
        elif cmd == 'shutdown':
            Rcon.send_cmd('doexit',InputResponses._default)
        elif cmd == 'raw':
            words.remove(cmd)
            raw_cmd = ' '.join(words)
            Rcon.send_cmd(raw_cmd,InputResponses._default)
        elif cmd == 'listplayers':
            out('Players online: [{}]'.format(len(Storage.players_online)))
            for steam_id,name in Storage.players_online.items():
                out("\t{} ({})".format(name.ljust(25),steam_id))
        else:
            out('Unknown command:',cmd)

class InputResponses(object):
    @staticmethod
    def _default(packet):
        out(packet.decoded['body'])
        