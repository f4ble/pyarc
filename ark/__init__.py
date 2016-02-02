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
from ark.config_base import ConfigBase
from ark.input_handler import InputHandler
from ark.storage import Storage
from ark.thread_handler import ThreadHandler
from ark.database import Db
import ark.default_input_commands
from ark.server_control import ServerControl

def configIntegrityCheck():
    baseNames = dir(ConfigBase)
    failed = False
    names = []
    for name in dir(Config):
        if name not in baseNames:
            names.append(name)
            failed = True
    if failed:
        print('Config integrity check failed. You have config variables not matched with config_base.py:')
        print(', '.join(names))
        exit()

def init():
    # Config.show_keep_alive_after_idle = 1

    try:
        configIntegrityCheck()
        Config.printSettings()
        Db.init()

        # Activate event handling. Define your evnets in events/__init__.py
        import ark.events

        Rcon.init(Config.rcon_host, Config.rcon_port, Config.query_port, Config.rcon_password, Config.rcon_socket_timeout)

        InputHandler.init()

        # Activate scheduled tasks. Define your tasks in tasks/__init__.py
        import ark.tasks

        # Prevent threads from dying due to early main completed execution.
        while True:
            if Storage.terminate_application is True:
                exit()
            time.sleep(1)  # Important part of not being a CPU hog.

    except KeyboardInterrupt:
        Storage.terminate_application = True
