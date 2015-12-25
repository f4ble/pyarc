import time

from ark.rcon import Rcon
from ark.scheduler import Scheduler
from ark.server_control import ServerControl


class Task_DailyRestart(Scheduler):
    """Broadcasts warnings start 10 minutes prior to update and restart.
    """
    @staticmethod
    def run():
        Rcon.send('broadcast Restarting in 10 minutes')
        time.sleep(60*10)
        Rcon.send('broadcast Restarting in 60 seconds')
        time.sleep(60)
        ServerControl.restart_server()