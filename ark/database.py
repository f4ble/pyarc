from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .cli import *
from factory import Factory
Config = Factory.get('Config')
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

    # noinspection PyUnreachableCode
    @staticmethod
    def _create_tables():

        print("Creating tables.")
        Base.metadata.create_all(Db.engine)
        
        
class Db(DbBase):
    """Helper functions for database
    
    No reason to hate sqlalchemy or spend 30 years learning.
    Write your often-used functions here :)
    """

    @classmethod
    def keep_alive(cls):
        resp = cls.engine.execute('select 1')

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
            p = Db.find_player(steam_id=steam_ids)
            if p:
                p.last_seen = text('NOW()')
                Db.session.add(p)
                do_commit = True
        else:
            for steam_id in steam_ids:
                p = Db.find_player(steam_id=steam_id)
                if p:
                    p.last_seen = text('NOW()')
                    Db.session.add(p)
                    do_commit = True

        if do_commit is True:
            Db.session.commit()
            return True
        return False

    @classmethod
    def website_data_get(cls,key):
        return Db.session.query(WebsiteData).filter_by(key=key).first()


    @classmethod
    def website_data_set(cls,key,value):
        data = cls.session.query(WebsiteData).filter_by(key=key).first()
        if not data:
            data = WebsiteData()

        data.key = key
        data.value = value

        cls.session.add(data)
        cls.session.commit()


    @staticmethod
    def find_player(steam_id=None, steam_name=None, name=None, exact_match=True):
        """Find player by steam_name, name or steam id
        
        Searches steam_id, steam_name and name. In that order.
        exact_match: If true - On any name search only return if 1 match

        Args:
            steam_name: Default None
            steam_id: Default None
            name: Default None
            exact_match: Bool. Default True.
        Returns:
            Player object or None
        """
        player = None


        if steam_id:
            player = Db.session.query(Player).filter_by(steam_id=steam_id).first()
        elif steam_name:
            players = Db.session.query(Player).filter_by(steam_name=steam_name)
            if exact_match:
                if players.count() == 1:
                    player = players.first()
            else:
                player = players.first()
        elif name:
            players = Db.session.query(Player).filter_by(name=name)
            if exact_match:
                if players.count() == 1:
                    player = players.first()
            else:
                player = players.first()
        else:
            out('ERROR: No search parameters in db.find_player')

        if player:
                return player
        return None
    
    
    @staticmethod
    def find_player_wildcard(player_name=None, steam_name=None):
        """Find player by LIKE %name% 
        
        Args:
            player_name: String, default None
            steam_name: String, default None
        Returns:
            Player object or None
        """
        player = None
        wildcard = '%{}%'.format(player_name)
        if player_name:
            player = Db.session.query(Player).filter(Player.name.like(wildcard)).first()
        elif steam_name:
            player = Db.session.query(Player).filter(Player.steam_name.like(wildcard)).first()
        else:
            out('ERROR: No search params. db.find_player_wildcard')

        return player
    
    @staticmethod
    def create_player(steam_id, steam_name, name=None):
        """Create entry in players table
        
        Returns:
            Player: Object
            Bool: True if new entry.
        """
        player = Db.find_player(steam_id, steam_name)
        
        if player is None:
            player = Player(steam_name=steam_name, steam_id=steam_id, name=name, admin=0, last_seen=text("NOW()"), created=text("NOW()"))
            Db.session.add(player)
            Db.session.commit()
            return player, True

        return player, False        

    @classmethod
    def update_player(cls, steam_id, steam_name=None, name=None):
        player = cls.find_player(steam_id)
        if player is None:
            return None, False

        altered = False
        if steam_name and player.steam_name != steam_name:
            player.steam_name = steam_name
            altered = True
        if name and player.name != name:
            player.name = name
            altered = True

        if altered:
            cls.session.add(player)
            cls.session.commit()
        return True

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
    
        