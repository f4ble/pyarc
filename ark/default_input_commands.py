import datetime

from .cli import *
from .database import Db
from .input_handler import InputHandler, InputResponses
from .rcon import Rcon
from .server_control import ServerControl
import re

# noinspection PyUnusedLocal,PyUnusedLocal
class DefaultInputCommands(object):
    @classmethod
    def init(cls):
        InputHandler.register_command('stats',cls._cmd_stats)
        InputHandler.register_command('exit',cls._cmd_exit)
        InputHandler.register_command('check_version',cls._cmd_check_version)
        InputHandler.register_command('version',cls._cmd_version)
        InputHandler.register_command('saveworld',cls._cmd_saveworld)
        InputHandler.register_command('shutdown',cls._cmd_shutdown)
        InputHandler.register_command('exit',cls._cmd_exit)
        InputHandler.register_command('raw',cls._cmd_raw)
        InputHandler.register_command('online',cls._cmd_online)
        InputHandler.register_command('restart',cls._cmd_restart)
        InputHandler.register_command('repopulate',cls._cmd_repopulate_on_next_restart)
        InputHandler.register_command('server up',cls._cmd_server_running)

        #Debug commands
        InputHandler.register_command('debug queue', cls._debug_send_queue)
        InputHandler.register_command('debug last trans', cls._debug_last_trans)
        InputHandler.register_command('debug packet count', cls._debug_packet_count)
        InputHandler.register_command('debug all',cls._debug_all)


    @classmethod
    def _cmd_repopulate_on_next_restart(cls,text):
        Storage.repopulate_dinos_on_next_restart = True
        out('Server will repopulate wild dinos on next restart')

    @classmethod
    def _debug_all(cls,text):
        cls._debug_last_trans()
        cls._debug_send_queue()
        cls._debug_packet_count()

    @staticmethod
    def _debug_packet_count():
        Rcon.debug_compare_packet_count()

    @staticmethod
    def _debug_last_trans():
        str_time = datetime.datetime.fromtimestamp(int(Storage.last_sent_packet))
        out('Last sent packet was: ', str_time)
        out('Last sent packet body was: ', Storage.last_sent_packet_body)
        
        str_time = datetime.datetime.fromtimestamp(int(Storage.last_recv_packet))
        out('Last received packet was: ', str_time)
        out('Last received packet body was: ', Storage.last_recv_packet_body)
        
    @staticmethod
    def _debug_send_queue():
        out('Send queue length is currently: ', len(Rcon.outgoing_queue))
        
    @staticmethod
    def _cmd_server_running():
        result = ServerControl.is_server_running()
        if result is True:
            out('Server is running.')
        else:
            out('Server is NOT running.')
        
    @staticmethod
    def _cmd_restart(text):
        if text.lower().strip() == 'restart now':
            out('Issuing IMMEDIDATE server restart')
            Rcon.broadcast('Restarting the server!')
            ServerControl.restart_server()
            return

        regex = re.compile('restart (?P<minutes>[\d]+)',re.IGNORECASE)
        matches = regex.search(text)
        if matches is None:
            out('Please specify minutes 5,10,30,60 or NOW. Example: restart 60')
            return

        minutes = matches.group('minutes')

        result, err = Rcon.delayed_restart(minutes)
        if not result:
            out('ERROR: {}'.format(err))
            return

        out('Server set to restart in {} minutes'.format(minutes))
        return

        
    @staticmethod
    def _cmd_stats(text):
        out('Number of players in database: {} active this week and {} total'.format(Db.getPlayerCount(True),Db.getPlayerCount()))
        
        
    @staticmethod
    def _cmd_exit(text):
        Storage.terminate_application = True
    
    @staticmethod
    def _cmd_check_version(text):
        res = ServerControl.new_version()
        out('New version available' if res is True else 'No new version')

    @staticmethod
    def _cmd_version(text):
        out('Server is running game version:',Storage.query_data['game_version'])
        
    @staticmethod
    def _cmd_saveworld(text):
        Rcon.send('saveworld',InputResponses.default)
        
    @staticmethod
    def _cmd_shutdown():
        Rcon.send('doexit',InputResponses.default)
        
    @staticmethod
    def _cmd_raw(text):
        raw_cmd = text[len('raw '):]
        Rcon.send(raw_cmd,InputResponses.default)
        
    @staticmethod
    def _cmd_online(text):
        out('Players online: [{}]'.format(len(Storage.players_online)))
        for steam_id,name in Storage.players_online.items():
            out("\t{} ({})".format(name.ljust(25),steam_id))
            
            
DefaultInputCommands.init()