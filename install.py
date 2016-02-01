"""
Installation script for PyArc
"""

from ark.config import Config
from ark.config_base import ConfigBase
from ark.database import Db
from types import *

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


def configRequiredCheck():
    assert type(Config.log_folder) is str and not '', 'Config failure: log_folder not defined'
    assert type(Config.rcon_host) is str and not '', 'Config failure: rcon_host not defined'
    assert type(Config.rcon_password) is str and not '', 'Config failure: rcon_password not defined'
    assert type(Config.rcon_port) is int and not 0, 'Config failure: rcon_port not defined'
    assert type(Config.query_port) is int and not 0, 'Config failure: query_port not defined'
    assert type(Config.path_to_server) is str and not '', 'Config failure: path_to_server not defined'
    assert type(Config.server_executable) is str and not '', 'Config failure: server_executable not defined'
    assert type(Config.path_to_steamcmd) is str and not '', 'Config failure: path_to_steamcmd not defined'
    assert type(Config.path_to_config) is str and not '', 'Config failure: path_to_config not defined'
    assert type(Config.os_process_list_cmd) is str and not '', 'Config failure: os_process_list_cmd not defined'
    assert type(Config.shootergameserver_params) is str and not '', 'Config failure: shootergameserver_params not defined'
    assert type(Config.database_connect_string) is str and not '', 'Config failure: database_connect_string not defined'


print('Running checks....')

print('Required config params')
configRequiredCheck()

print('Required config integrity')
configIntegrityCheck()

print('Database tables. Creating table unless they exist.')
Db.init()
Db.first_run()

print('All seems well! GLHF')