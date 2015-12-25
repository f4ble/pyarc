from ark.config import Config
Config.database_connect_string = Config.test_database_connect_string
Config.display_output = True
Config.debug_output_level = 1

from ark.database import Db
Db.init()

from ark_unit_tests.ut_fundamental_tasks import *
if not list_players():
    print('"list players": Failed')
    exit(-1)
if not get_chat():
    print('"get_chat": Failed')
    exit(-1)    
    

from ark_unit_tests.ut_chat_commands import *
if not chat_commands():
    print('"chat_commands": Failed')
    exit(-1)
    
    
exit(0) #Success