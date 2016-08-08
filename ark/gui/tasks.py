from ark.thread_handler import ThreadHandler
from factory import Factory

import time

class GuiTasks(object):
    @classmethod
    def loop(cls):
        time.sleep(1)
        GuiTasks.get_active_threads()

    @classmethod
    def get_active_threads(cls):
        GUI = Factory.get('GUI')
        max_threads = len(ThreadHandler.activethreads)
        active_threads = 0
        for key,timestamp in ThreadHandler.activethreads.items():
            if timestamp > (time.time()-30):
                active_threads += 1
        GUI.active_threads['text'] = "{} / {}".format(active_threads,max_threads)
