import time
from datetime import timedelta
from .config import Config
from .storage import Storage
from pprint import pprint

def timeStr():
    return time.strftime("%H:%M:%S")

def time_ago(past,present=None):
    if present is None:
        present = time.time()
    
    seconds_ago = present - past
    td = timedelta(seconds=int(seconds_ago))
    return td

def out_pretty(obj):
    #For debug purposes
    pprint(dir(obj))

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