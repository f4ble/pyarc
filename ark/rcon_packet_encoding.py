import struct
from ark.config import Config
from ark.cli import *

class PacketEncoding(object):
    def __init__(self):
        pass
        
    def _encode(self,data,type):
        id = self.packet_id
        
        body = data;
        packet_data = {
            #Size is prepended later.
            "id": struct.pack("<i",id),
            "type":   struct.pack("<i",type),
            "body":   body + chr(0),
            "term":   chr(0)
        }
        
        debug_out("\n")
        debug_out("Sending: ")
        debug_out(packet_data)
        
        pack_size = 0
        for key,value in packet_data.items():
            pack_size += len(value)
            
        
        self.decoded['size'] = pack_size
        self.decoded['id'] = id
        self.decoded['type'] = type
        self.decoded['body'] = body + chr(0)
        self.decoded['term'] = chr(0)
        
        packet = struct.pack("<i",pack_size)
        packet += packet_data["id"]
        packet += packet_data["type"]
        packet += bytes(packet_data["body"],encoding='ascii')
        packet += bytes(packet_data["term"],encoding='ascii')
        
        self.binary_string = packet
        
    def _decode(self,binary_string):
        packet_data = struct.unpack("<iii",binary_string[0:12])
        body = binary_string[12:-2].decode('ascii')
        
        data = {
            "size": packet_data[0],
            "id": packet_data[1],
            "type": packet_data[2],
            "body": body,
            "term": chr(0)
        }
        
        self.decoded['size'] = data['size']
        self.decoded['id'] = data['id']
        self.decoded['type'] = data['type']
        self.decoded['body'] = data['body']
        self.decoded['term'] = data['term']
        
        
        debug_out("\nDecoding:")
        debug_out("\tSize: ",data["size"])
        debug_out("\tID: ",data["id"])
        debug_out("\tType: ",data["type"])
        if len(body) == 0:
            debug_out("\tBody: Empty")
        else:
            debug_out("\tBody:",body)
        debug_out("\n")
        
        return data    