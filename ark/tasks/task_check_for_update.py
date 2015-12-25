from ark.scheduler import Scheduler
from ark.cli import *
from ark.server_control import ServerControl
from ark.events import Events

class Task_CheckForUpdates(Scheduler):
    @staticmethod
    def run():
        if ServerControl.new_version() is True:
            Events.triggerEvent(Events.E_NEW_ARK_VERSION)
        else:
            debug_out('No server update available',level=3)