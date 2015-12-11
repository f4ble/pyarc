import time
from .config import Config
from .storage import Storage

def timeStr():
    return time.strftime("%H:%M:%S")



def out(*args,**kwargs):
    if Config.display_output is False:
        return
    Storage.last_output_unix_time = time.time()
    print('{} [{}] # '.format(timeStr(),len(Storage.players_online)),*args,**kwargs)
        
        

def debug_out(*args,**kwargs):
    if Config.debug_output_level is 0 or False:
        return
    
    if 'level' not in kwargs:
        level = 5
    else:
        level = kwargs['level']
        del kwargs['level']
        
    if level <= Config.debug_output_level:
        Storage.last_output_unix_time = time.time()
        print("[{}]".format(level),*args,**kwargs)