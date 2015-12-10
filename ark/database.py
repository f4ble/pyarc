from .storage import Storage
from .config import Config
from .cli import *
import time
from sqlalchemy import create_engine, distinct, select, alias, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from ark.orm_models import *

class Db(object):
    engine = None
    session = None
    connection = None
    
    @staticmethod
    def init():
        if len(Config.database_connect_params):
            Db.engine = create_engine(Config.database_connect_string,**Config.database_connect_params)
        else:
            Db.engine = create_engine(Config.database_connect_string)
        
        Session = sessionmaker(bind=Db.engine)
        Db.session = Session()
        Db.connection = Db.engine.connect()
        
    @staticmethod
    def first_run():
        Db._create_tables()
        
    @staticmethod
    def _create_tables():
        return #Untested
        print("Creating tables.")
        Base.metadata.create_all(Db.engine)
        
    @staticmethod
    def getPlayerCount(active=False):
        if active is False:
            result = Db.session.query(Player)
        else:
            result = Db.session.query(Player).filter(func.unix_timestamp(Player.last_seen) >= time.time()-3600*24*7)
            
        return result.count()
        