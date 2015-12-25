import re

from ark.database import Db
from ark.events import Events
from ark.rcon import Rcon
from ark.scheduler import Scheduler
from ark.storage import Storage


class Task_ListPlayers(Scheduler):
    @staticmethod
    def run():
        Rcon.send('ListPlayers',Task_ListPlayers.parse)
        
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
        for steam_id in connected_ids:
            connected[steam_id] = player_list[steam_id]
        
        disconnected_ids = set(Storage.players_online.keys()) - set(player_list.keys())    
        disconnected = {}
        for steam_id in disconnected_ids:
            disconnected[steam_id] = Storage.players_online[steam_id]
        
        Storage.players_online = player_list
        
        if len(connected):
            for steam_id in connected:
                name = Storage.players_online[steam_id]
                if Db.find_player(name,steam_id) is None:
                    Events.triggerEvent(Events.E_NEW_PLAYER, steam_id, name)
            Events.triggerEvent(Events.E_CONNECT, connected)
            
        if len(disconnected):
            Events.triggerEvent(Events.E_DISCONNECT, disconnected)
            
            
        return connected,disconnected,Storage.players_online