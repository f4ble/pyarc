CONFIG_BE_QUIET = True
from ark.config import Config


from ark_unit_tests.ut_fundamental_tasks import *
if list_players() == False:
    print('"list players": Failed')
    exit(-1)
if get_chat() == False:
    print('"get_chat": Failed')
    exit(-1)    
    
    
exit(0) #Success
