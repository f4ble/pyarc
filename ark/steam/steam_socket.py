from ark.steam.steam_socket_core import SteamSocketCore
from ark.cli import *
from ark.storage import Storage
from ark.server_control import ServerControl
from ark.event_handler import EventHandler
import time

class SteamSocket(SteamSocketCore):
    timestamp_transmission_opened = None

    @classmethod
    def socket_connect(cls, host, port, query_port, password=None, timeout=None):
        if not ServerControl.is_server_running():
            out('Waiting for connection to query port.')
            while not ServerControl.is_server_running():
                time.sleep(1)
            out('Query successful.')

        out('Connecting to {}:{}...'.format(host, port))
        cls.timestamp_transmission_opened = time.time()
        result, err = super().socket_connect(host, port, query_port, password, timeout)
        if result:
            out('Connected!')
            result, err = cls.socket_auth(password)
            if not result:
                return result, err
        else:
            out('Unable to connect: ', err)

        return result, err


    @classmethod
    def socket_auth(cls, password=None):
        out('Authenticating...')
        result, err = super().socket_auth(password)
        if result:
            out('Auth: Successful')
            EventHandler.triggerEvent(EventHandler.E_RCON_CONNECTED)
        else:
            out('Auth: Failed. ', err)

        return result,err

    @classmethod
    def close_socket(cls):
        out("Closing socket")
        return super().close_socket()

    @classmethod
    def get_packets_sent_per_second(cls):
        elapsed = time.time() - cls.timestamp_transmission_opened

        if len(cls.outgoing_packets) == 0 or elapsed == 0:
            return 0

        return round(len(cls.outgoing_packets) / elapsed, 3)

    @classmethod
    def socket_send(cls, packet):
        bytes_sent, err = super().socket_send(packet)
        debug_out('Sent packet_id {} with {} bytes of data: {}  ({} queue size, packets/sec: {})'.format(packet.packet_id,bytes_sent, packet.outgoing_command, len(cls.outgoing_queue), cls.get_packets_sent_per_second()), level=4)
        return bytes_sent, err

    @classmethod
    def _socket_read(cls, wait=False):
        result, err = super()._socket_read(wait)

        if result is False:
            out('Error: {}'.format(err))
            return result, err

        if result:
            Storage.last_recv_packet = time.time()

        return result,err