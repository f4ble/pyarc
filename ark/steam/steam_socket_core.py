import collections
import socket
import time

from ark.cli import *
from ark.storage import Storage
from ark.steam.steam_packet import SteamPacket
from ark.steam.source_server_query import ArkSourceQuery
from ark.server_control import ServerControl

class SteamSocketCore(object):
    """
    Sockets compatible with Steam server 
    
    
    """

    _socket = None

    is_connected = False
    is_reconnecting = False

    outgoing_packets = {}
    incoming_packets = []

    outgoing_queue = collections.deque()

    socket_host = None
    socket_port = None
    socket_query_port = None
    password = None
    socket_timeout = None

    @classmethod
    def reconnect(cls):
        cls.is_reconnecting = True
        cls.is_connected = False
        cls.close_socket()
        cls.incoming_packets.clear()
        if not ServerControl.is_server_running():
            out('Waiting for connection to query port.')
            while not ServerControl.is_server_running():
                time.sleep(1)
            out('Query successful.')

        result, err = cls.socket_connect(cls.socket_host, cls.socket_port, cls.socket_query_port, cls.password, cls.socket_timeout)
        while not result:
            out('Retrying reconnect in {}s'.format(Config.reconnect_wait))
            time.sleep(Config.reconnect_wait)
            result, err = cls.socket_connect(cls.socket_host, cls.socket_port, cls.socket_query_port, cls.password, cls.socket_timeout)

        cls.is_reconnecting = False

    @classmethod
    def socket_auth(cls, password=None):
        """Authenticate to Steam Server

        Args:
            If password is None it will use password supplied in connect

        Returns:
            bool, error message
        """

        if password is None:
            password = cls.password

        packet = SteamPacket.pack(password, 3)

        cls.socket_send(packet)  # Important to use _socket_send_packet. Do not want this queued or you might end up with endless reconnects
        result = cls._socket_read(True)

        if result is None:
            return False, 'No reply'

        for response in cls.incoming_packets:
            if response.packet_id == packet.packet_id:
                cls.incoming_packets.remove(response)
                cls.is_connected = True
                return True, None
            if response.packet_id == -1:
                return False, 'Failed. Wrong password?'

        return False, 'No response to auth packet'

    @classmethod
    def socket_connect(cls, host, port, queryport, password=None, timeout=None):
        """Connect to socket.

        Stores arguments on class variables to remember for reconnect.
        Closes socket if open.

        Returns:
            Bool, Error

        """
        if cls._socket:
            cls._socket.close()  # Reset socket in case this is a reconnect

        if timeout is None:
            timeout = socket.getdefaulttimeout()

        cls.socket_host = host
        cls.socket_port = port
        cls.socket_query_port = queryport
        cls.password = password
        cls.socket_timeout = timeout

        try:
            cls._socket = socket.create_connection((cls.socket_host, cls.socket_port), timeout)
        except socket.timeout as e:  ### NEEDS TESTING.
            return False, e
        except OSError as e:
            return False, e

        return True, None

    @classmethod
    def close_socket(cls):
        if cls._socket:
            cls._socket.close()

    @classmethod
    def send(cls, data, response_callback=None, priority=False):
        packet = SteamPacket.pack(data, 2)
        packet.response_callback = response_callback

        if priority:
            cls.outgoing_queue.appendleft(packet)
        else:
            cls.outgoing_queue.append(packet)

    @classmethod
    def loop_communication(cls):
        while True:
            # Don't send stuff when we're not connected.
            while not cls.is_connected:
                time.sleep(1)

            send_packet = None
            try:
                send_packet = cls.outgoing_queue.popleft()

            # No items in queue. Sleep to avoid CPU drain
            except IndexError:
                time.sleep(1)  # Performance. Dont spam the loop.
                pass

            if send_packet:
                bytes_sent, err = cls.socket_send(send_packet)
                if bytes_sent:
                    if not cls.wait_for_response(send_packet):
                        out('Retrying waiting for response:')
                        if not cls.wait_for_response(send_packet):
                            out('Failure to get response. Reconnecting...')
                            cls.reconnect()
                else:
                    cls.is_connected = False
                    out('Failure to send command. Reconnecting...')
                    cls.reconnect()



    @classmethod
    def wait_for_response(cls,send_packet):
        # Read until there is nothing more to read.
        packets = collections.OrderedDict()
        while len(packets) < 1:
            time.sleep(0.5)
            for obj in cls.incoming_packets:
                if obj.packet_id == send_packet.packet_id:
                    packets[obj.packet_id] = obj
                    cls.incoming_packets.remove(obj)


        # Support for multipacket response (Responses that are bigger than 4096)
        key, packet = packets.popitem()
        if len(packets):
            while len(packets):
                key, multipacket_response = packets.popitem()
                packet.decoded['body'] = "{}{}".format(packet.decoded['body'],multipacket_response.decoded['body'])

        if callable(send_packet.response_callback):
            packet.outgoing_command = send_packet.outgoing_command
            send_packet.response_callback(packet)
        else:
            out('Unknown callback for: ', packet.data)

        return True

    @classmethod
    def socket_send(cls, packet):
        """
        Send SteamPacket
        
        Args:
            packet: SteamPacket
        Returns:
            bytes_sent: False or 0 means failure.
            err: String
        """
        assert isinstance(packet, SteamPacket), 'packet argument not of object SteamPacket'

        packet.timestamp = time.time()
        try:
            bytes_sent = cls._socket.send(packet.binary_string)
        except OSError as err:
            return False, err

        cls.outgoing_packets[int(packet.decoded["id"])] = packet
        return bytes_sent, None

    @classmethod
    def listen(cls):
        while True:
            while cls.is_connected is False:
                time.sleep(1)

            cls._socket_read()


    @classmethod
    def _socket_read(cls, wait=False):
        """
        Read from socket. Does not fail on low timeout - only returns None.
        
        Args:
            wait: Bool. Blocking mode - wait until timeout.
        
        Returns:
            True, error_message: None
            None, error_message: 'No data'
            False, error_message: 'Socket error'
            
        """
        if wait:
                data = ""
                while len(data) == 0:
                    try:
                        data = cls._socket.recv(4096)
                    except socket.timeout:
                        pass
                    except OSError as err:
                        return False, 'Failure to read from socket: {}'.format(err)

                cls._parse_socket_data(data)
                return True, None

        try:
            data = cls._socket.recv(4096)
            cls._parse_socket_data(data)
            return True, None
        except socket.timeout:
            return None, 'No data'
        except OSError as err:
            return False, 'Failure to read from socket: {}'.format(err)

    @classmethod
    def _parse_socket_data(cls,binary_string):
        """ Parses data from socket_read() and stores packet objects in cls.incoming_packets

        Recursive function. Handles multiple packets in one binary string
        """
        packet = SteamPacket.unpack(binary_string)
        packet.timestamp = time.time()

        if packet.keep_alive_packet:
            out('Keep alive')
        else:
            cls.incoming_packets.append(packet)

        if packet.remaining_data:
            cls._parse_socket_data(packet.remaining_data)
