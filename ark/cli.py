import time
from datetime import timedelta
from .config import Config
from .storage import Storage
from pprint import pprint

Config.create_log_folder()

def log_defined():
    if Config.log_folder is not None:
        return True
    return False

def get_log_file_handle(debug_file=False):
    try:
        if debug_file:
            if Storage.debug_log_file_handle is None:
                Storage.debug_log_file_handle = open(Config.log_folder + "debug_log.txt", mode='a+', encoding='utf-8')
                print('\n\n### NEW SESSION ###\n\n',file=Storage.debug_log_file_handle, flush=True)
                
            return Storage.debug_log_file_handle
        else:
            if Storage.log_file_handle is None:
                Storage.log_file_handle = open(Config.log_folder + "log.txt", mode='a+', encoding='utf-8')
                print('\n\n### NEW SESSION ###\n\n',file=Storage.log_file_handle, flush=True)
                
            return Storage.log_file_handle
    except OSError as err:
        print('Error opening log file: ', err)
        
def time_str():
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
    
    text = "{} [{}] # ".format(time_str(), len(Storage.players_online))
    
    print(text,*args,**kwargs)
    
    if log_defined():
        log = get_log_file_handle()
        if log:
            print(text,*args,**kwargs,file=log, flush=True)
            
        debug_log = get_log_file_handle(True)
        if log:
            print(text,*args,**kwargs,file=debug_log, flush=True)
        

def debug_out(*args,**kwargs):
    if 'level' not in kwargs:
        level = 5
    else:
        level = kwargs['level']
        del kwargs['level']
        
    if level <= Config.debug_output_level_to_log and log_defined():
        log = get_log_file_handle(True)
        if log:
            print("[{}]".format(level),*args,**kwargs,file=log)
            
            
    if Config.debug_output_level is 0 or False:
        return
        
    if level <= Config.debug_output_level:
        #Storage.last_output_unix_time = time.time()
        print("[{}]".format(level),*args,**kwargs)
        