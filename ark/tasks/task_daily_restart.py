from ark.scheduler import Scheduler
from ark.cli import *
from ark.server_control import ServerControl
from ark.rcon import Rcon
import time

class Task_DailyRestart(Scheduler):
    """Broadcasts warnings start 10 minutes prior to update and restart.
    """
    def run(self):
        Rcon.send_cmd('broadcast Restarting in 10 minutes')
        time.sleep(60*10)
        Rcon.send_cmd('broadcast Restarting in 60 seconds')
        time.sleep(60)
        ServerControl.restart_server()