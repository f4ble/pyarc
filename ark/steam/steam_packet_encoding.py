import struct

from ark.cli import *


class SteamPacketEncoding(object):
    def __init__(self):
        self.response_callback = None
        self.binary_string = None
        self.timestamp = None
        self.keep_alive_packet = False
        self.empty_response = False
        self.decoded = dict(size=None, id=None, type=None, body=None, term=None)
        self.packet_id = None
        self.outgoing_command = None
        self.remaining_data = None

    def _encode(self, data, packet_type):
        packet_id = self.packet_id

        body = data
        packet_data = {
            # Size is prepended later.
            "id": struct.pack("<i", packet_id),
            "type": struct.pack("<i", packet_type),
            "body": body + chr(0),
            "term": chr(0)
        }

        debug_out("Packet Encoded: \n",packet_data)

        pack_size = 0
        for key, value in packet_data.items():
            pack_size += len(value)

        self.decoded['size'] = pack_size
        self.decoded['id'] = packet_id
        self.decoded['type'] = packet_type
        self.decoded['body'] = body + chr(0)
        self.decoded['term'] = chr(0)

        packet = struct.pack("<i", pack_size)
        packet += packet_data["id"]
        packet += packet_data["type"]
        packet += bytes(packet_data["body"], encoding='ascii')
        packet += bytes(packet_data["term"], encoding='ascii')

        self.binary_string = packet

    def _decode(self, binary_string):
        packet_data = struct.unpack("<iii", binary_string[0:12])
        try:
            body = binary_string[12:packet_data[0]+4]
            remaining_data = binary_string[packet_data[0]+4:]
            if len(remaining_data):
                self.remaining_data = remaining_data

        except Exception as e:
            out('ERROR: Unable to parse length of body in binary string:')
            print(binary_string,'\n\n')

        try:
            body = body[:-2].decode('ascii')
        except Exception as e:
            out('ERROR: Unable to decode aasci for binary string:')
            print(binary_string,'\n\n')
            raise

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

        self.packet_id = int(data['id'])

        debug_out("\nPacket Decoded:")
        debug_out("\tSize: ", data["size"])
        debug_out("\tID: ", data["id"])
        debug_out("\tType: ", data["type"])
        if len(body) == 0:
            debug_out("\tBody: Empty")
        else:
            debug_out("\tBody:", body)
        debug_out("\n")
