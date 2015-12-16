from ark.cli import *
from ark.thread_handler import ThreadHandler
import time, datetime

class Scheduler(object):
    """Schedule Task base object.
    
    Creates a thread and executes method run() in parent object
    Use one class per task and give it a descriptive name for readable output. 
    
    Usage:
        Scheduler.run_once()
        Scheduler.run_interval()
        Scheduler.run_daily()
        
        Returns Object of class <parent>
        Purpose of returned object is the subject of many scholars.... but it's there anyways.
        
    """
    interval = None #Every X seconds
    immediately = False
    
    timestamp = None #Once at specific time.
    time_string = None #Every time clock is hh:mm:ss
    
    last_run = 0
    
    @classmethod
    def run_once(parent,timestamp=None,in_seconds=None):
        """Once AFTER timestamp.
        
        Create scheduler child object which executes run() at appointed time
        Creates a thread and is expected to be run in a thread supporting script.
        
        Args:
            Opt Int         timestamp: Unix timestamp
            Opt Int         in_seconds: Added to current timestamp
            Func            callback: Code to run
            
        Returns:
            Bool
        """
        if timestamp is None and in_seconds is None:
            raise TypeError('Define either timestamp or in_seconds with an int value')
        
        if in_seconds:
            timestamp = time.time() + in_seconds
            
        obj = parent()
        obj.timestamp = timestamp
        ThreadHandler.create_thread(obj._run_once_callback)
        
        str_time = datetime.datetime.fromtimestamp(int(timestamp))
        out('Scheduler: Class "{}" tasked with run_once at {}.'.format(obj.__class__.__name__,str_time))
        return obj
    
    def _run_once_callback(self):
        """
        Sleep until timestamp and exit(0)
        """
        
        sleep_duration = self.timestamp - time.time()
        time.sleep(sleep_duration)
        self.run()
        exit(0)

    @classmethod
    def run_interval(parent,seconds, immediately=False):
        """Every X seconds
        
        Create scheduler child object which executes run() at appointed time
        Creates a thread and is expected to be run in a thread supporting script.
        
        Args:
            Int     seconds: Seconds between each run
            Func    callback: Code to run
            Bool    immediately: Run callback immediately after creation
            
        Returns:
            Bool
        """
        obj = parent()
        obj.interval = seconds
        obj.immediately = immediately
        
        out('Scheduler: Class "{}" tasked with run_interval {} seconds.'.format(obj.__class__.__name__,seconds))
        ThreadHandler.create_thread(obj._run_interval_callback)
        return obj
    
    def _run_interval_callback(self):
        if self.immediately:
            while True:
                self.run()
                time.sleep(self.interval)
        else:
            while True:
                time.sleep(self.interval)
                self.run()
    
    @classmethod
    def run_daily(parent,time_string):
        """Every day after hh:mm:ss
        
        Create scheduler child object which executes run() at appointed time
        Creates a thread and is expected to be run in a thread supporting script.
        
        Args:
            Str     time_string: Syntax hh:mm:ss
            Func    callback: Code to run
            Bool    immediately: Run callback immediately after creation
            
        Returns:
            Bool
        """
        obj = parent()
        obj.time_string = time_string
        ThreadHandler.create_thread(obj._run_daily_callback)
        out('Scheduler: Class "{}" tasked with run_daily at {}.'.format(obj.__class__.__name__,time_string))
        return obj
    
    def _run_daily_callback(self):
        """
        Sleep for run timestamp - current timestamp. Then sleep 24 hours
        """
        
        
        full_date = time.strftime('%Y-%m-%d') + ' ' + self.time_string
        timeToRun = time.mktime(time.strptime(full_date,'%Y-%m-%d %H:%M:%S'))
        
        if timeToRun < time.time():
            timeToRun += 3600*24
        
        #dt = datetime.datetime.fromtimestamp(timeToRun)
        #print('Set to run at: ',dt)
              
        sleep_duration = timeToRun - time.time()
        #print("sleeping ",sleep_duration)
        time.sleep(sleep_duration)
            
        while True:
            self.run()
            time.sleep(3600*24)
