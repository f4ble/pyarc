"""Simple implementation non-blocking code execution.

By Torgrim "Fable" Ruud - torgrim.ruud@gmail.com

"""

import threading
from queue import Queue

from .cli import *
import time

# noinspection PyUnusedLocal
class ThreadHandler:
    queue = []
    activethreads = {}

    @staticmethod
    def create_thread(callback, looping=True):
        """Create a thread and run callback()
        
        Static method for creating a thread based non-blocking execution of code.

        If you want params passed to the callback use:
            new_callback = lambda:callback(*args,**kwargs)

        Args:
            callback: function containing logic operation
            
        Returns:
            None
        """
        
        debug_out('Creating thread')

        def thread_work(item):
            try:
                callback()
            except KeyboardInterrupt:
                Storage.terminate_application = True

        def thread_work_loop(item):
            thread_id = threading.current_thread().ident
            while True:
                ThreadHandler.activethreads[thread_id] = int(time.time())
                if Storage.terminate_application is True:
                    exit()
                    
                try:
                    callback()
                except KeyboardInterrupt:
                    Storage.terminate_application = True    
            
        def worker():
            item = q.get()
            if looping:
                thread_work_loop(item)
            else:
                thread_work(item)
            q.task_done()


        q = Queue()
        t = threading.Thread(target=worker)

        t.daemon = True
        t.start()
        ThreadHandler.queue.append(t)
        i = len(ThreadHandler.queue)
        q.put(i)
        #q.join() #q.join will prevent further execution of the script
