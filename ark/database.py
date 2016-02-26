from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from sqlalchemy.pool import NullPool

from .cli import *
from factory import Factory
Config = Factory.get('Config')
Base = declarative_base()
import logging
from ark.orm_models import *


class DbBase(object):
    """Core of database
    
    Initializes the database. 
    """
    
    engine = None
    session = None
    connection = None
    
    @classmethod
    def init(cls,echo=None):
        if len(Config.database_connect_params):
            if echo is not None:
                Config.database_connect_params['echo'] = echo
            params = Config.database_connect_params
            cls.engine = create_engine(Config.database_connect_string,**params) #, pool_recycle=600  - doesn't seem to work
        else:
            params = {}
            #params['poolclass'] = NullPool
            if echo is not None:
                params['echo'] = echo

            cls.engine = create_engine(Config.database_connect_string,**params) #, pool_recycle=600

        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()
        cls.connection = cls.engine.connect()

        #cls.engine.execute('SET GLOBAL connect_timeout=28800')
        #cls.engine.execute('SET GLOBAL wait_timeout=28800')
        #cls.engine.execute('SET GLOBAL interactive_timeout=28800')

    @classmethod
    def reconnect(cls):
        out('Reconnecting to SQL.')
        cls.close_connection()
        cls.init()

    @classmethod
    def close_connection(cls):
        if cls.connection:
            out('closing con')
            try:
                cls.connection.close()
                cls.engine.dispose()
            except exc.SQLAlchemyError as e:
                out('Unable to close SQL connection: {}'.format(e))

    @classmethod
    def first_run(cls):
        cls._create_tables()

    # noinspection PyUnreachableCode
    @classmethod
    def _create_tables(cls):

        print("Creating tables.")
        Base.metadata.create_all(cls.engine)

    @classmethod
    def commit(cls):
        try:
            cls.session.commit()
        except exc.SQLAlchemyError as e:
            out('SQL Failure: {}'.format(e))


class Db(DbBase):
    """Helper functions for database
    
    No reason to hate sqlalchemy or spend 30 years learning.
    Write your often-used functions here :)
    """

    @classmethod
    def keep_alive(cls):
        try:
            resp = cls.engine.execute('select 1')
        except exc.SQLAlchemyError as e:
            out('SQL Failure: with keep alive:',e)

    @classmethod
    def update_last_seen(cls,steam_ids):
        """Update last_seen column on a player
        
        Args:
            steam_ids: Integer or List of steam id
        Returns:
            True if any updates
        """

        do_commit = False

        if type(steam_ids) == int:
            p = cls.find_player(steam_id=steam_ids)
            if p:
                p.last_seen = text('NOW()')
                cls.session.add(p)
                do_commit = True
        else:
            for steam_id in steam_ids:
                p = cls.find_player(steam_id=steam_id)
                if p:
                    p.last_seen = text('NOW()')
                    cls.session.add(p)
                    do_commit = True

        if do_commit is True:
            cls.commit()
            return True
        return False

    @classmethod
    def website_data_get(cls,key):
        try:
            return cls.session.query(WebsiteData).filter_by(key=key).first()
        except exc.SQLAlchemyError as e:
            out('SQL Failure to get website_data:',e)
            cls.reconnect()
            return None


    @classmethod
    def website_data_set(cls,key,value):
        try:
            data = cls.session.query(WebsiteData).filter_by(key=key).first()
        except exc.SQLAlchemyError as e:
            out('SQL Failure - website_data set:',e)
            cls.reconnect()
            return False

        if not data:
            data = WebsiteData()

        data.key = key
        data.value = value

        cls.session.add(data)
        cls.commit()
        return True

    @classmethod
    def find_player(cls,steam_id=None, steam_name=None, name=None, exact_match=True):
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
        try:
            player = None


            if steam_id:
                player = cls.session.query(Player).filter_by(steam_id=steam_id).first()
            elif steam_name:
                players = cls.session.query(Player).filter_by(steam_name=steam_name)
                if exact_match:
                    if players.count() == 1:
                        player = players.first()
                else:
                    player = players.first()
            elif name:
                players = cls.session.query(Player).filter_by(name=name)
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
        except exc.SQLAlchemyError as e:
            out('SQL Failure to find player:',e)
            cls.reconnect()
            return None
    
    
    @classmethod
    def find_player_wildcard(cls,player_name=None, steam_name=None):
        """Find player by LIKE %name% 
        
        Args:
            player_name: String, default None
            steam_name: String, default None
        Returns:
            Player object or None
        """
        try:
            player = None
            wildcard = '%{}%'.format(player_name)
            if player_name:
                player = cls.session.query(Player).filter(Player.name.like(wildcard)).first()
            elif steam_name:
                player = cls.session.query(Player).filter(Player.steam_name.like(wildcard)).first()
            else:
                out('ERROR: No search params. db.find_player_wildcard')

            return player
        except exc.SQLAlchemyError as e:
            out('SQL Failure - find player wildcard:',e)
            cls.reconnect()
            return None
    
    @classmethod
    def create_player(cls, steam_id, steam_name, name=None):
        """Create entry in players table
        
        Returns:
            Player: Object
            Bool: True if new entry.
        """

        player = cls.find_player(steam_id, steam_name)

        if player is None:
            player = Player(steam_name=steam_name, steam_id=steam_id, name=name, admin=0, last_seen=text("NOW()"), created=text("NOW()"))
            cls.session.add(player)
            cls.commit()
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
            cls.commit()
        return True

    @classmethod
    def create_chat_entry(cls,player_id,name,data):
        entry = Chat(player_id=player_id,name=name,data=data,created=text('NOW()'))
        cls.session.add(entry)
        cls.commit()
        return entry

    @classmethod
    def getPlayerCount(cls,active=False):
        try:
            if active is False:
                result = Db.session.query(Player)
            else:
                result = Db.session.query(Player).filter(func.unix_timestamp(Player.last_seen) >= time.time()-Config.active_player_timeframe)

            return result.count()
        except exc.SQLAlchemyError as e:
            out('SQL Failure - getPlayerCount:',e)
            cls.reconnect()
            return None
            
    @classmethod
    def check_word(word):
        result = None
        result = Db.session.query(ChatFilter).filter_by(word=word).first()
        if result:
            return result
        return None
