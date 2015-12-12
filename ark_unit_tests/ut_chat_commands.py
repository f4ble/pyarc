from ark.config import Config
from ark.cli import *
from ark.default_event_callbacks import EventCallbacks

def chat_commands():
    #steam_name,player_name,text,line
    EventCallbacks.parse_chat_command('Steam Test','Test','!lastseen Test Alpha','Steam Test (Test): !lastseen Test Alpha')
    
    EventCallbacks.parse_chat_command('Steam Test','Test','!online','Steam Test (Test): !online')
    