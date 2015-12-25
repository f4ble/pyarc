from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .cli import *

Base = declarative_base()

from ark.orm_models import *


class DbBase(object):
    """Core of database
    
    Initializes the database. 
    """
    
    engine = None
    session = None
    connection = None
    
    @staticmethod
    def init():
        if len(Config.database_connect_params):
            Db.engine = create_engine(Config.database_connect_string,**Config.database_connect_params, pool_recycle=3600)
        else:
            Db.engine = create_engine(Config.database_connect_string, pool_recycle=3600)
        
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
        
        
class Db(DbBase):
    """Helper functions for database
    
    No reason to hate sqlalchemy or spend 30 years learning.
    Write your often-used functions here :)
    """
    
    @staticmethod
    def update_last_seen(steam_ids):
        """Update last_seen column on a player
        
        Args:
            steam_ids: Integer or List of steam id
        Returns:
            True if any updates
        """
        do_commit = False
        
        if type(steam_ids) == int:
            p = Db.find_player(player_steam_id=steam_ids)
            if p:
                p.last_seen = text('NOW()')
                Db.session.add(p)
                do_commit = True
        else:
            for steam_id in steam_ids:
                p = Db.find_player(player_steam_id=steam_id)
                if p:
                    p.last_seen = text('NOW()')
                    Db.session.add(p)
                    do_commit = True

        if do_commit is True:
            Db.session.commit()
            return True
        return False
        
    @staticmethod
    def find_player(player_steam_id=None,player_name=None):
        """Find player by name or steam id
        
        If both arguments present check steam id first and then name
        Elif one of the arguments present use that.
        
        Args:
            player_name: Default None
            player_steam_id: Default None
        Returns:
            Player object or None
        """
        player = None

        if player_steam_id is not None and player_name is not None:
            player = Db.session.query(Player).filter_by(steam_id=player_steam_id).first()
            if player is None:
                players = Db.session.query(Player).filter_by(name=player_name)
                if players.count() == 1:
                    player = players.first()
        elif player_steam_id is not None:
            player = Db.session.query(Player).filter_by(steam_id=player_steam_id).first()
        elif player_name is not None:
            player = Db.session.query(Player).filter_by(name=player_name).first()
            
        if player is not None:
                return player
        return None
    
    
    @staticmethod
    def find_player_wildcard(player_name=None):
        """Find player by LIKE %name% 
        
        Args:
            player_name: String
        Returns:
            Player object or None
        """
        wildcard = '%{}%'.format(player_name)
        player = Db.session.query(Player).filter(Player.name.like(wildcard)).first()
        return player
    
    @staticmethod
    def create_player(player_steam_id,player_name):
        """Create entry in players table
        
        Returns:
            Player: Object
            Bool: True if new entry.
        """
        player = Db.find_player(player_steam_id,player_name)
        
        if player is None:
            player = Player(name=player_name,steam_id=player_steam_id, admin=0, last_seen=text("NOW()"), created=text("NOW()"))
            Db.session.add(player)
            Db.session.commit()
            return player, True
        return player, False        
    
    @staticmethod
    def create_chat_entry(player_id,name,data):
        entry = Chat(player_id=player_id,name=name,data=data,created=text('NOW()'))
        Db.session.add(entry)
        Db.session.commit()
        return entry
    
    @staticmethod
    def getPlayerCount(active=False):
        if active is False:
            result = Db.session.query(Player)
        else:
            result = Db.session.query(Player).filter(func.unix_timestamp(Player.last_seen) >= time.time()-Config.active_player_timeframe)
            
        return result.count()
    
        