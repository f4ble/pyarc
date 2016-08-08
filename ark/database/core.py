from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ark.cli import *
from factory import Factory

Config = Factory.get('Config')
Base = declarative_base()

from ark.database.orm_models import *

class DbCore(object):
    """Core of database

    Initializes the database.
    """

    def __init__(self, echo=None):
        engine = None
        session = None
        connection = None
        try:
            if len(Config.database_connect_params):
                if echo is not None:
                    Config.database_connect_params['echo'] = echo
                params = Config.database_connect_params
                self.engine = create_engine(Config.database_connect_string, **params, pool_recycle=600) #, pool_recycle=600  - doesn't seem to work
            else:
                params = {}
                #params['poolclass'] = NullPool
                if echo is not None:
                    params['echo'] = echo

                self.engine = create_engine(Config.database_connect_string, **params, pool_recycle=600) #

            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            self.connection = self.engine.connect()

            #self.engine.execute('SET GLOBAL connect_timeout=28800')
            #self.engine.execute('SET GLOBAL wait_timeout=28800')
            #self.engine.execute('SET GLOBAL interactive_timeout=28800')
        except ConnectionResetError as e:
            out('SQL Failure: {}'.format(e))
        except exc.SQLAlchemyError as e:
            out('SQL Failure: {}'.format(e))

    def reconnect(self):
        out('Reconnecting to SQL.')
        self.close_connection()
        self.__init__()

    def close_connection(self):
        if self.connection:
            out('closing con')
            try:
                self.connection.close()
                self.engine.dispose()
            except ConnectionResetError as e:
                out('SQL Failure: {}'.format(e))
            except exc.SQLAlchemyError as e:
                out('Unable to close SQL connection: {}'.format(e))

    def first_run(self):
        self._create_tables()

    def _create_tables(self):

        print("Creating tables.")
        Base.metadata.create_all(self.engine)

    def commit(self):
        try:
            self.session.commit()
        except ConnectionResetError as e:
            out('SQL Failure: {}'.format(e))
        except exc.SQLAlchemyError as e:
            out('SQL Failure: {}'.format(e))