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
from .database import Db

class InputHandler(object):
    
    """
    _commands_callbacks is where register_command adds the callback for a certain command.
    The structure is a dictionary with key=command and value is a list to support multiple callbacks per command.
    """
    _commands_callbacks = {} 
    
    def register_command(command,callback):
        """Register a callback function when console input "command" is issued.
        
        Command is matched with the beginning of the input string. Forced lowercase.
        
        Example: To create a command called "message":
            Input string to trigger: message "Fable" Hi there.
            Command: message
        
        Args:
            String: Command to recognize. Used as dictionary key. 
            Function: Callback(String: Untouched input from console)
        """
        if command not in InputHandler._commands_callbacks.keys():
            InputHandler._commands_callbacks[command] = []
        InputHandler._commands_callbacks[command].append(callback)
    
    @staticmethod
    def init():
        th = ThreadHandler.create_thread(InputHandler._listen)
    
    def _listen():
        command = input()
        if command.strip() == "":
            return
        
        if InputHandler.parse_command(command) is False:
            out('Unknown command:',command)
            
            cmdlist = ', '.join(InputHandler._commands_callbacks.keys())
            out('Try using one of these:\n\t', cmdlist)
        
    def parse_command(text):
        for command in InputHandler._commands_callbacks.keys():
            length = len(command)
            if text[0:length].lower() == command:
                InputHandler._run_all_cmds(command,text)
                return True
        return False                
        
    def _run_all_cmds(command,text):
        for callback in InputHandler._commands_callbacks[command]:
            callback(text)

class InputResponses(object):
    @staticmethod
    def default(packet):
        out(packet.decoded['body'])
        