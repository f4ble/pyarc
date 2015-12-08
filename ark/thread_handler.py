"""Simple implementation non-blocking code execution.

By Torgrim "Fable" Ruud - torgrim.ruud@gmail.com

"""

import threading
from queue import Queue
from .config import Config
from .storage import Storage
from .cli import *

class ThreadHandler:
    queue = []
    
    @staticmethod
    def create_thread(callback):
        """Create a thread and run callback()
        
        Static method for creating a thread based non-blocking execution of code.
        
        Args:
            callback: function containing logic operation
            
        Returns:
            None
        """
        
        debug_out('Creating thread')
            
        def thread_work(item):
            while True:
                if Storage.terminate_application is True:
                    exit()
                    
                try:
                    callback()
                except KeyboardInterrupt:
                    Storage.terminate_application = True    
            
        def worker():
            while True:
                item = q.get()
                thread_work(item)
                q.task_done()

        q = Queue()

        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        ThreadHandler.queue.append(t)
        item = len(ThreadHandler.queue)
        q.put(item)
        #q.join() #q.join will prevent further execution of the script
