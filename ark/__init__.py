"""Multithreaded RCON system

Author: Torgrim "Fable" Ruud - torgrim.ruud@gmail.com

RCON that can act both as a daemon and as an interactive application.
Listen, Sending, Scheduled Tasks and more are all threaded enabling these
scripts to run non-blocking and performing many different tasks.

"""

import time

from factory import Factory
import ark.default_input_commands
from ark.cli import out

from ark.input_handler import InputHandler
from ark.rcon import Rcon
from ark.server_control import ServerControl
from ark.storage import Storage
from ark.thread_handler import ThreadHandler
from ark.thread_handler import ThreadHandler
import ark.database

import sys
def exceptionHandler(exception_type, exception, traceback, debug_hook=sys.excepthook):
    #sys.tracebacklimit = 0
    Config = Factory.get('Config')
    if Config.traceback_hide_output:
        debug_hook(exception_type, exception, traceback)
    else:
        print("{}: {}".format(exception_type.__name__, exception))
sys.excepthook = exceptionHandler

#Loads a config file and runs init()
def custom_import(file,error_name):
    try:
        file = 'configs.{}'.format(file)
        print('Loading: ', file)
        tmp = __import__(file,fromlist='init')
        tmp.init()

    except ImportError:
        print('Unable to load {}.'.format(error_name))
        raise

def init():
    # Config.show_keep_alive_after_idle = 1
    Config = Factory.get('Config')
    Lang = Factory.get('Translation')
    try:
        Config.printSettings()

        if not ServerControl.is_server_running():
            out(Lang.get('server_not_running'))
            ServerControl.start_server()

        custom_import(Config.events_config,'events') #Load events

        Rcon.init(Config.rcon_host, Config.rcon_port, Config.query_port, Config.rcon_password, Config.rcon_socket_timeout)

        #custom_import(Config.events_config,'input') #Load terminal input configuration
        custom_import(Config.tasks_config,'tasks') #Load tasks

        custom_import(Config.chatcmds_config,'chatcmds') #Load chat commands

        if not Factory.has('GUI'):
            InputHandler.init() #Activate listening for terminal input

            # Prevent threads from dying due to early main completed execution.
            while True:
                if Storage.terminate_application is True:
                    exit()
                time.sleep(1)  # Important part of not being a CPU hog.

    except KeyboardInterrupt:
        Storage.terminate_application = True
