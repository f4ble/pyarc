import time

from ark.rcon import Rcon
from ark.scheduler import Scheduler
from ark.server_control import ServerControl
from ark.storage import Storage
from factory import Factory
Lang = Factory.get('Translation')

class Task_DailyRestart(Scheduler):
    """Broadcasts warnings start 10 minutes prior to update and restart.
    """
    @staticmethod
    def run():
        Rcon.delayed_restart(60,Lang.get('event_restart'))




class Task_DailyRestartRepopulate(Scheduler):
    """Broadcasts warnings start 10 minutes prior to update and restart.
    """
    @staticmethod
    def run():
        Storage.repopulate_dinos_on_next_restart = True
        Rcon.delayed_restart(60,Lang.get('event_restart_repopulate'))