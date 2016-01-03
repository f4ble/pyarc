from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,String, Text, SmallInteger, DateTime, text, ForeignKey
Base = declarative_base()



class Player(Base):
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True, nullable=False)
    steam_name = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    steam_id = Column(Text, nullable=False)
    admin = Column(SmallInteger, nullable=False, server_default="0")
    last_seen = Column(DateTime, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, server_default=text("NOW()"), server_onupdate=text("NOW()"), nullable=False)
    
    def __repr__(self):
        return "User Object - id: {}, name: {}, steam_id: {}, admin: {}, last_seen: {}, created: {}".format(self.id,self.name,self.steam_id,self.admin,self.last_seen,self.created)
    


class AdminMessage(Base):
    __tablename__ = 'admin_messages'
    
    id = Column(Integer, primary_key=True, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), server_default='Null')
    message = Column(Text)
    resolved = Column(SmallInteger, server_default="0")
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, server_default=text("NOW()"), server_onupdate=text("NOW()"), nullable=False)
    
    
    

class ConnectionLog(Base):
    __tablename__ = 'connection_log'
    
    id = Column(Integer, primary_key=True, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    has_disconnected = Column(SmallInteger, server_default='0')
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, server_default=text("NOW()"), server_onupdate=text("NOW()"), nullable=False)
    

class CmdSchedule(Base):
    __tablename__ = 'cmd_schedule'
    
    id = Column(Integer, primary_key=True, nullable=False)
    cmd = Column(Text)
    cmd_cron = Column(Text)
    run_interval = Column(Integer, server_default='Null')
    run_at_time = Column(Text)
    run_once = Column(DateTime, server_default='Null')
    last_run = Column(DateTime, server_default='Null')
    active = Column(SmallInteger, server_default="1")
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, server_default=text("NOW()"), server_onupdate=text("NOW()"), nullable=False)
    
    
class Chat(Base):
    __tablename__ = 'chat'
    
    id = Column(Integer, primary_key=True, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), server_default='Null')
    name = Column(String(255), nullable=False)
    data = Column(Text, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, server_default=text("NOW()"), server_onupdate=text("NOW()"), nullable=False)
