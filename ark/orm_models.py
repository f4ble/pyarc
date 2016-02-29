from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,String, TIMESTAMP, Text, SmallInteger, DateTime, text, ForeignKey
Base = declarative_base()


class WebsiteData(Base):
    __tablename__ = 'website_data'

    id = Column(Integer, primary_key=True, nullable=False)
    key = Column(Text, nullable=False)
    value = Column(Text, nullable=False)
    modified = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP"), nullable=False)

    def __repr__(self):
        return "WebsiteData id: {}, key: {}, value: {}, modified: {}".format(self.id,self.key,self.value,self.modified)

class ChatFilter(Base):
    __tablename__ = 'chat_filter'
    id = Column(Integer, primary_key=True, nullable=False)
    word = Column(String(30), nullable=False)
    usage = Column(Integer, nullable=True) #Not used yet

    def __repr__(self):
        return self.word

class Player(Base):
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True, nullable=False)
    steam_name = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    steam_id = Column(Text, nullable=False)
    admin = Column(SmallInteger, nullable=False, server_default="0")
    last_seen = Column(DateTime, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP"), nullable=False)
    
    def __repr__(self):
        return "User Object - id: {}, name: {}, steam_id: {}, admin: {}, last_seen: {}, created: {}".format(self.id,self.name,self.steam_id,self.admin,self.last_seen,self.created)
    


class AdminMessage(Base):
    __tablename__ = 'admin_messages'
    
    id = Column(Integer, primary_key=True, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), server_default=text('NULL'))
    message = Column(Text)
    resolved = Column(SmallInteger, server_default="0")
    created = Column(DateTime, nullable=False)
    modified = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP"), nullable=False)
    
    
    

class ConnectionLog(Base):
    __tablename__ = 'connection_log'
    
    id = Column(Integer, primary_key=True, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    has_disconnected = Column(SmallInteger, server_default='0')
    created = Column(DateTime, nullable=False)
    modified = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP"), nullable=False)
    

class CmdSchedule(Base):
    __tablename__ = 'cmd_schedule'
    
    id = Column(Integer, primary_key=True, nullable=False)
    cmd = Column(Text)
    cmd_cron = Column(Text)
    run_interval = Column(Integer, server_default=text('NULL'))
    run_at_time = Column(Text)
    run_once = Column(DateTime, server_default=text('NULL'))
    last_run = Column(DateTime, server_default=text('NULL'))
    active = Column(SmallInteger, server_default="1")
    created = Column(DateTime, nullable=False)
    modified = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP"), nullable=False)
    
    
class Chat(Base):
    __tablename__ = 'chat'
    
    id = Column(Integer, primary_key=True, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), server_default=text('NULL'))
    name = Column(String(255), nullable=False)
    data = Column(Text, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP"), nullable=False)
    
class Survey(Base):
    __tablename__='survey'
    id=Column(Integer, primary_key=True, nullable=False)
    question=Column(String(255), nullable=False)
    created=Column(DateTime, nullable=False)
    active=Column(SmallInteger, server_default="0")

class Option(Base):
    __tablename__='option'
    id=Column(Integer, primary_key=True, nullable=False)
    id_survey=Column(Integer, nullable=False)
    option=Column(String(255), nullable=False)
    count=Column(Integer, nullable=False, server_default="0")

class Vote(Base):
    __tablename__='vote'
    id=Column(Integer, primary_key=True, nullable=False)
    player_name=Column(String(255), nullable=True)
    steam_id=Column(Text, nullable=False)
    id_survey=Column(Integer, nullable=False)
    id_option=Column(Integer, nullable=False)
