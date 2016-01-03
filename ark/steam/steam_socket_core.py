import collections
import socket

from ark.cli import *
from ark.steam.steam_packet import SteamPacket
from ark.events import Events

class SteamSocketCore(object):
    """
    Sockets compatible with Steam server 
    
    
    """

    _socket = None

    is_connected = False
    is_reconnecting = False

    outgoing_packets = {}
    incoming_packets = {}

    outgoing_queue = collections.deque()

    socket_host = None
    socket_port = None
    password = None
    socket_timeout = None

    @classmethod
    def reconnect(cls):
        cls.is_reconnecting = True
        cls.close_socket()
        result, err = cls.socket_connect(cls.socket_host,cls.socket_port,cls.password,cls.socket_timeout)
        while not result:
            out('Retrying reconnect in {}s'.format(Config.reconnect_wait))
            time.sleep(Config.reconnect_wait)
            result, err = cls.socket_connect(cls.socket_host,cls.socket_port,cls.password,cls.socket_timeout)

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
        response, err = cls.socket_read(True)
        if response is None:
            return False, 'No reply'
        if response.decoded["id"] == -1:
            return False, 'Failed. Wrong password?'

        cls.is_connected = True
        return True, None

    @classmethod
    def socket_connect(cls, host, port, password=None, timeout=None):
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
                out('sleep')
                time.sleep(1)

            try:
                send_packet = cls.outgoing_queue.popleft()
                if send_packet:
                    bytes_sent, err = cls.socket_send(send_packet)
                    if bytes_sent:
                        cls.wait_for_response(send_packet)

                    else:
                        cls.is_connected = False
                        out('Failure to send command. Reconnecting...')
                        cls.reconnect()

            # No items in queue. Sleep to avoid CPU drain
            except IndexError:
                time.sleep(1)  # Performance. Dont spam the loop.
                pass

    @classmethod
    def wait_for_response(cls,send_packet):
        packet = None
        while packet is None or packet.keep_alive_packet:
            packet, err = cls.socket_read(True)
            if err:
                out('Error waiting for response: ', err)
                return False

        if packet.decoded['id'] != send_packet.packet_id:
            raise Exception('Failed to match send packet id {} to received id {}.'.format(send_packet.packet_id, packet.packet_id))

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
    def socket_read(cls, wait=False):
        """
        Read from socket. Does not fail on low timeout - only returns None.
        
        Args:
            wait: Bool. Blocking mode - wait until timeout.
        
        Returns:
            SteamPacket, error_message: None
            None, error_message: 'No data'
            False, error_message: 'Socket error'
            
        """
        try:
            data = ""
            if wait is True:
                while len(data) == 0:
                    data = cls._socket.recv(4096)
            else:
                data = cls._socket.recv(4096)

            packet = SteamPacket.unpack(data)
            packet.timestamp = time.time()
            if packet.keep_alive_packet:
                return packet, None

            cls.incoming_packets[packet.packet_id] = packet
            return packet, None
        except socket.timeout:
            return None, 'No data'
        except OSError as err:
            return False, 'Failure to read from socket: {}'.format(err)
