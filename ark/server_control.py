import re
import subprocess
from .config import Config
import ark.rcon 
from .cli import *

class ServerControl(object):
    """Control for Ark (Steam) Server
    
    Ideally do UDP query to server, get version and compare it with version from Steam web api.
    For now that seems impossible.
    
    So check local buildId in file, update, and check the file again :/
    
    Make sure you run update_server() and new_version() in a thread to avoid blocking script.
    """
    
    app_id = "346110" #String. To avoid type casting. Never have use for it as int.
    _update_available = False
    
    def wait_for_server_ready():
        if ServerControl.is_update_running() is True:
            out('Waiting for server update....')
            while ServerControl.is_update_running() is True:
                time.sleep(1)
            out('Server updated.')
            
        if ServerControl.is_server_running() is False:
            out('Waiting for server to start.')
            while ServerControl.is_server_running() is False:
                time.sleep(1)
            out('Server started. Waiting for it to load...')
            time.sleep(Config.ark_server_loading_time)
            
    def is_server_running():
        result = subprocess.run(Config.os_process_list_cmd, shell=True, stdout=subprocess.PIPE, check=False);
        tasks = result.stdout.decode('utf-8')
        regex = re.compile('^ShooterGameServer\.exe',re.IGNORECASE | re.MULTILINE)
        match = regex.search(tasks)
        if match is None:
            return False
        return True
    
    def is_update_running():
        result = subprocess.run(Config.os_process_list_cmd, shell=True, stdout=subprocess.PIPE, check=False);
        tasks = result.stdout.decode('utf-8')
        regex = re.compile('^Steamcmd\.exe',re.IGNORECASE | re.MULTILINE)
        match = regex.search(tasks)
        if match is None:
            return False
        return True
    
    def restart_server():
        out('Restart issued.')
        ark.rcon.Rcon.send_cmd('saveworld',ServerControl._restart_shutdown,priority=True)
        #Chains into _restart_chain_shutdown() and then start_server()
        
    @staticmethod
    def _restart_shutdown(packet):
        out('Restart: Save world complete.')
        ark.rcon.Rcon.send_cmd('doExit',ServerControl.update_and_start_server,priority=True)
        #Chains into start_server() from _restart_chain_shutdown()
    
    @staticmethod
    def update_and_start_server(packet):
        ServerControl.update_server()
        ServerControl.start_server()
        
    @staticmethod
    def start_server():
        out('Starting server...')
        #ark_start = "cd C:\ArkServer\ShooterGame\Binaries\Win64 && start ShooterGameServer.exe TheIsland?Port=27015?QueryPort=27016?MaxPlayers=30"
        cmd = "cd {ark_path}\\ShooterGame\\Binaries\\Win64 && start ShooterGameServer.exe {params}".format(ark_path=Config.path_to_server,params=Config.shootergameserver_params)
        subprocess.call(cmd,shell=True,stdout=False)
        
    @staticmethod
    def update_server():
        """Update ARK Server
        
        Will lock while running process.
        """
        cmd = Config.path_to_steamcmd + "steamcmd.exe +login anonymous +force_install_dir \"C:\ArkServer\" +app_update " + ServerControl.app_id + " +quit"
        result = subprocess.call(cmd,shell=True,stdout=False)
                
    @staticmethod
    def new_version():
        """Check if update is needed
        
        Warning: May take a long while due to server update.
        Will lock while running process.
        """
        
        if ServerControl._update_available is True:
            return True
        
        old_build = ServerControl._get_local_build()
        ServerControl.update_server()
        new_build = ServerControl._get_local_build()
        
        if old_build != new_build:
            ServerControl._update_available = True
            return True
        return False
        
    @staticmethod
    def _get_local_build():
        """Check local file for build id
        
        """
        filename = Config.path_to_server + "steamapps\\appmanifest_" + ServerControl.app_id + ".acf"
        f = open(filename,"r")
        data = f.read()
        regex = re.compile("buildid[^\d]+(?P<buildid>[\d]+)", re.MULTILINE | re.IGNORECASE)
        return regex.search(data).group('buildid')
       