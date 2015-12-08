import re
import subprocess
from .config import Config

class ServerControl(object):
    """Control for Ark (Steam) Server
    
    Ideally do UDP query to server, get version and compare it with version from Steam web api.
    For now that seems impossible.
    
    So check local buildId in file, update, and check the file again :/
    
    Make sure you run update_server() and new_version() in a thread to avoid blocking script.
    """
    
    app_id = "346110" #String. To avoid type casting. Never have use for it as int.
    _update_available = False
    
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
       