from ark.scheduler import Scheduler
from ark.cli import *
from ark.server_control import ServerControl
from ark.event_handler import EventHandler

class Task_CheckForUpdates(Scheduler):
    @staticmethod
    def run():
        if ServerControl.new_version() is True:
            EventHandler.triggerEvent(EventHandler.E_NEW_ARK_VERSION)
        else:
            debug_out('No server update available',level=3)