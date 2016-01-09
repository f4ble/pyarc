import time

from ark.rcon import Rcon
from ark.scheduler import Scheduler
from ark.server_control import ServerControl
from ark.storage import Storage


class Task_DailyRestart(Scheduler):
    """Broadcasts warnings start 10 minutes prior to update and restart.
    """
    @staticmethod
    def run():
        Rcon.delayed_restart(60,'\nThis is a maintenance restart that we do every day.')




class Task_DailyRestartRepopulate(Scheduler):
    """Broadcasts warnings start 10 minutes prior to update and restart.
    """
    @staticmethod
    def run():
        Storage.repopulate_dinos_on_next_restart = True
        Rcon.delayed_restart(60,'\nThis is a maintenance restart that we do every day. NB: This restart will repopulate wild dinos.')