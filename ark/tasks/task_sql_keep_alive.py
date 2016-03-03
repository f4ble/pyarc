import re

from ark.scheduler import Scheduler

from factory import Factory
Db = Factory.get('Database')

class Task_SQL_keep_alive(Scheduler):
    @staticmethod
    def run():
        Db.keep_alive()