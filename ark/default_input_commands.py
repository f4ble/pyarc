from .input_handler import InputHandler, InputResponses
from .cli import *
from .config import Config
from .storage import Storage
from .rcon import Rcon
from .database import Db

class DefaultInputCommands(object):
    @staticmethod
    def init():
        InputHandler.register_command('stats',DefaultInputCommands._cmd_stats)
        InputHandler.register_command('exit',DefaultInputCommands._cmd_exit)
        InputHandler.register_command('check_version',DefaultInputCommands._cmd_check_version)
        InputHandler.register_command('version',DefaultInputCommands._cmd_version)
        InputHandler.register_command('saveworld',DefaultInputCommands._cmd_saveworld)
        InputHandler.register_command('shutdown',DefaultInputCommands._cmd_shutdown)
        InputHandler.register_command('exit',DefaultInputCommands._cmd_exit)
        InputHandler.register_command('raw',DefaultInputCommands._cmd_raw)
        InputHandler.register_command('online',DefaultInputCommands._cmd_online)
        
    @staticmethod
    def _cmd_stats(text):
        out('Number of players in database: {} active this week and {} total'.format(Db.getPlayerCount(True),Db.getPlayerCount()))
        
        
    def _cmd_exit(text):
        Storage.terminate_application = True
    
    def _cmd_check_version(text):
        res = ServerControl.new_version()
        out('New version available' if res is True else 'No new version')

    def _cmd_version(text):
        out('Server is running game version:',Storage.query_data['game_version'])
        
    def _cmd_saveworld(text):
        Rcon.send_cmd('saveworld',InputResponses.default)
        
    def _cmd_shutdown(text):
        Rcon.send_cmd('doexit',InputResponses.default)
        
        
    def _cmd_raw(text):
        raw_cmd = text[len('raw '):]
        Rcon.send_cmd(raw_cmd,InputResponses.default)
        
    def _cmd_online(text):
        out('Players online: [{}]'.format(len(Storage.players_online)))
        for steam_id,name in Storage.players_online.items():
            out("\t{} ({})".format(name.ljust(25),steam_id))
            
            
DefaultInputCommands.init()