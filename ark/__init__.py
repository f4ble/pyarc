"""Multithreaded RCON system

Author: Torgrim "Fable" Ruud - torgrim.ruud@gmail.com

RCON that can act both as a daemon and as an interactive application.
Listen, Sending, Scheduled Tasks and more are all threaded enabling these
scripts to run non-blocking and performing many different tasks.

"""
import time

from ark.thread_handler import ThreadHandler
from ark.cli import out
from ark.rcon import Rcon
from ark.config import Config
from ark.scheduled_tasks import Tasks
from ark.input_handler import InputHandler
from ark.storage import Storage
from ark.thread_handler import ThreadHandler
from ark.database import Db
import ark.default_event_callbacks

def init():
    #Config.show_keep_alive_after_idle = 1

    try:
        if Rcon.init(Config.rcon_host,Config.rcon_port,Config.rcon_password) is False:
            out('Failure to connect. Aborting...')
            exit()
            
        Rcon.listen()
        Rcon.init_send_queue()
        Db.init()
        
        Rcon.loop_scheduled_tasks(Tasks.run_scheduled)
        InputHandler.init()
        ThreadHandler.create_thread(Tasks.run_version_check)
        
        
        #Prevent threads from dying due to early main completed execution.
        while True:
            if Storage.terminate_application is True:
                exit()
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        Storage.terminate_application = True

