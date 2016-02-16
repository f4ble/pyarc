import re

from ark.database import Db
from ark.scheduler import Scheduler


class Task_SQL_keep_alive(Scheduler):
    @staticmethod
    def run():
        Db.close_connection()
        Db.init()
        #Db.keep_alive()