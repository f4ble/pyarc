import re
import subprocess
from urllib import request

import ark.rcon
from .cli import *
from ark.config import Config

# noinspection PyUnusedLocal
class ServerControl(object):
    """Control for Ark (Steam) Server
    
    Ideally do UDP query to server, get version and compare it with version from Steam web api.
    For now that seems impossible.
    
    So check local buildId in file, update, and check the file again :/
    
    Make sure you run update_server() and new_version() in a thread to avoid blocking script.
    """
    
    app_id = "376030" #String. To avoid type casting. Never have use for it as int.
    _update_available = False

    @classmethod
    def get_config(cls,clearPasswords=True):
        result = {}

        path = "{}Game.ini".format(Config.path_to_config)
        f = open(path,'rb')
        data = f.read()
        result['Game.ini'] = data.decode('utf-8')
        f.close()

        path = "{}GameUserSettings.ini".format(Config.path_to_config)
        f = open(path,'rb')
        data = f.read().decode('UTF-8')

        if clearPasswords:
            lines = data.split('\n')
            regex = re.compile('passw',re.IGNORECASE)

            for v in lines:
                match = regex.search(v)
                if match:
                    lines.remove(v)
            data = "\n".join(lines)


        result['GameUserSettings.ini'] = data
        f.close()


        return result

    @classmethod
    def wait_for_server_ready(cls):
        if cls.is_update_running() is True:
            out('Waiting for server update....')
            while cls.is_update_running() is True:
                time.sleep(1)
            out('Server updated.')

        if cls.is_server_running() is False:
            out('Waiting for server to start.')
            while cls.is_server_running() is False:
                time.sleep(1)
            out('Server started. Waiting for it to load...')
            time.sleep(Config.ark_server_loading_time)

    @staticmethod
    def is_server_running():
        result = subprocess.run(Config.os_process_list_cmd, shell=True, stdout=subprocess.PIPE, check=False)
        tasks = result.stdout.decode('utf-8')
        regex = re.compile('^ShooterGameServer\.exe',re.IGNORECASE | re.MULTILINE)
        match = regex.search(tasks)
        if match is None:
            return False
        return True
    
    @staticmethod
    def is_update_running():
        result = subprocess.run(Config.os_process_list_cmd, shell=True, stdout=subprocess.PIPE, check=False)
        tasks = result.stdout.decode('utf-8')
        regex = re.compile('^Steamcmd\.exe',re.IGNORECASE | re.MULTILINE)
        match = regex.search(tasks)
        if match is None:
            return False
        return True
    
    @classmethod
    def restart_server(cls):
        out('Restart issued.')
        ark.rcon.Rcon.send('saveworld',cls._restart_shutdown,priority=True)
        #Chains into _restart_chain_shutdown() and then start_server()
        
    @classmethod
    def _restart_shutdown(cls,packet):
        out('Restart: Save world complete.')
        ark.rcon.Rcon.send('doExit',cls.update_and_start_server,priority=True)
        #Chains into start_server() from _restart_chain_shutdown()
    
    @classmethod
    def update_and_start_server(cls,packet):
        cls.update_server()
        cls.start_server()
        
    @staticmethod
    def start_server():
        out('Starting server...')

        repopulate = ''
        if Storage.repopulate_dinos_on_next_restart:
            repopulate = '?ForceRespawnDinos'
            Storage.repopulate_dinos_on_next_restart = False
            out('Server restart flag: Repopulating wild dinos')

        params = Config.shootergameserver_params.format(repopulate=repopulate)
        cmd = "cd {ark_path}{server_executable} {params}".format(ark_path=Config.path_to_server, server_executable=Config.server_executable, params=params)
        subprocess.call(cmd,shell=True,stdout=False)
        
    @classmethod
    def update_server(cls):
        """Update ARK Server
        
        Will lock while running process.
        """
        out('Updating server...')
        cmd = "start {steamcmd_path}steamcmd.exe +login anonymous +force_install_dir {server_basepath} +app_update {app_id} +quit".format(steamcmd_path=Config.path_to_steamcmd, server_basepath=Config.path_to_server, app_id=cls.app_id)
        result = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE)


    #http://arkdedicated.com/version

    @classmethod
    def new_version(cls):
        """Check if update is needed

        Ark Developers have provided url with plain text version number:
        http://arkdedicated.com/version

        Returns
            bool New version?
            string live_version
            string steam_version
        """

        live_version = None
        steam_version = None

        version_url = 'http://arkdedicated.com/version'

        live_data = ark.Rcon.query_server()
        if live_data and 'game_version' in live_data.keys():
                live_version = live_data['game_version']

        data = request.urlopen(version_url)
        if data:
            steam_version = data.read().decode('utf-8')

        if steam_version != live_version:
            return True, live_version, steam_version

        return False, live_version, steam_version

