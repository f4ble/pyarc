from ark.scheduler import Scheduler
from ark.cli import *
from ark.rcon import Rcon
from ark.database import Db
from ark.events import Events
from ark.storage import Storage

import re

class Task_ListPlayers(Scheduler):
    def run(self):
        Rcon.send_cmd('ListPlayers',Task_ListPlayers.parse)
        
    @staticmethod
    def parse(packet):
        if packet.decoded["body"].strip() == 'No Players Connected':
            player_list = {}
        else:
            body = packet.decoded["body"].split("\n")
            
            rx = re.compile('[\d]+\. (?P<name>[^,]+), (?P<steamid>[\d]+)', re.IGNORECASE)
            player_list = {}
        
            for line in body:
                match = rx.search(line)
                if match is None: #empty string
                    continue
                
                steam_id = match.group("steamid")
                name = match.group("name")
                
                player_list[steam_id] = name
            
        connected_ids = set(player_list.keys()) - set(Storage.players_online.keys())
        connected = {}
        for id in connected_ids:
            connected[id] = player_list[id]
        
        disconnected_ids = set(Storage.players_online.keys()) - set(player_list.keys())    
        disconnected = {}
        for id in disconnected_ids:
            disconnected[id] = Storage.players_online[id]
        
        Storage.players_online = player_list
        
        if len(connected):
            for steam_id in connected:
                name = Storage.players_online[steam_id]
                if Db.find_player(name,steam_id) is None:
                    Events._triggerEvent(Events.E_NEW_PLAYER,steam_id,name)
            Events._triggerEvent(Events.E_CONNECT,connected)
            
        if len(disconnected):
            Events._triggerEvent(Events.E_DISCONNECT,disconnected)
            
            
        return connected,disconnected,Storage.players_online