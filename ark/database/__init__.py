from factory import Factory
from ark.cli import *

out('Initializing database.')

from ark.database.core import DbCore
Factory.set('DatabaseCore',DbCore())

from ark.database.helper import Db
Factory.set('Database',Db())

"""
from ark.thread_handler import ThreadHandler
from ark.database.handler import DatabaseHandler
ThreadHandler.create_thread(DatabaseHandler.process_queue,True)
"""