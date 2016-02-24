from ark.steam.steam_packet_encoding import SteamPacketEncoding
from ark.cli import *

class SteamPacket(SteamPacketEncoding):
    _packet_count = 0  # Static variable for unique id generation

    # Max packet size 4096

    # Types
    # 3	SERVERDATA_AUTH
    # 2	SERVERDATA_AUTH_RESPONSE
    # 2	SERVERDATA_EXECCOMMAND
    # 0	SERVERDATA_RESPONSE_VALUE

    @staticmethod
    def pack(body, packet_type=2):
        """Create new Packet instance and encode packet
        
        Args:
            body: ASCII string
            packet_type: Packet Type ID
            
        Returns:
            Object: New packet object instance
        """
        obj = SteamPacket()

        SteamPacket._packet_count += 1
        obj.packet_id = SteamPacket._packet_count

        obj.outgoing_command = body
        obj._encode(body, packet_type)
        return obj

    @staticmethod
    def unpack(binary_string):
        """Create new Packet instance and decode binary string
        
        Args:
            binary_string: Binary string packet data
            
        Returns:
            Object: New packet object instance
        """
        obj = SteamPacket()
        debug_out('Unpacking: ', binary_string,level=5)
        obj._decode(binary_string)

        if obj.decoded['body'].lower().strip() == 'server received, but no response!!':
            obj.empty_response = True
        if obj.decoded['body'].lower().strip() == 'keep alive':
            obj.keep_alive_packet = True

        return obj
