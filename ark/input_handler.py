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

from .cli import *
from .thread_handler import ThreadHandler


class InputHandler(object):
    
    """
    _commands_callbacks is where register_command adds the callback for a certain command.
    The structure is a dictionary with key=command and value is a list to support multiple callbacks per command.
    """
    _commands_callbacks = {} 

    @classmethod
    def register_command(cls,command,callback):
        """Register a callback function when console input "command" is issued.
        
        Command is matched with the beginning of the input string. Forced lowercase.
        
        Example: To create a command called "message":
            Input string to trigger: message "Fable" Hi there.
            Command: message
        
        Args:
            command: String to recognize. Used as dictionary key.
            callback: Function(String: Untouched input from console)
        """
        if command not in cls._commands_callbacks.keys():
            cls._commands_callbacks[command] = []
        cls._commands_callbacks[command].append(callback)
    
    @classmethod
    def init(cls):
        ThreadHandler.create_thread(InputHandler._listen)

    @classmethod
    def _listen(cls):
        command = input()
        if command.strip() == "":
            return
        
        if cls.parse_command(command) is False:
            out('Unknown command:',command)
            
            cmdlist = ', '.join(cls._commands_callbacks.keys())
            out('Try using one of these:\n\t', cmdlist)

    @classmethod
    def parse_command(cls,text):
        for command in cls._commands_callbacks.keys():
            length = len(command)
            if text[0:length].lower() == command:
                cls._run_all_cmds(command,text)
                return True
        return False                

    @classmethod
    def _run_all_cmds(cls,command,text):
        for callback in cls._commands_callbacks[command]:
            callback(text)

class InputResponses(object):
    @staticmethod
    def default(packet):
        out(packet.decoded['body'])
        