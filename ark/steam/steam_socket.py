import collections
import socket

from ark.cli import *
from ark.steam.steam_packet import SteamPacket


class SteamSocket(object):
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

    @classmethod
    def reconnect(cls):
        pass

    @classmethod
    def change_socket_state(cls, connected=False):
        if connected is True and cls.is_connected is not True:
            cls.is_connected = True
            return True
        elif connected is False and cls.is_connected is not False:
            cls.is_connected = False
            return True

        return False

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
        cls.socket_send(
            packet)  # Important to use _socket_send_packet. Do not want this queued or you might end up with endless reconnects
        response, err = cls.socket_read(True)
        if response is None:
            return False, 'No reply'
        if response.decoded["id"] == -1:
            return False, 'Failed. Wrong password?'

        cls.change_socket_state(True)
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

        try:
            cls._socket = socket.create_connection((cls.socket_host, cls.socket_port), timeout)
        except socket.timeout as e:  ### NEEDS TESTING.
            return False, e

        return True, None

    @classmethod
    def close_socket(cls):
        out("Closing socket")
        cls._socket.close()
        cls.change_socket_state(False)

    @classmethod
    def send(cls, data, response_callback=None, priority=False):
        packet = SteamPacket.pack(data, 2)
        packet.response_callback = response_callback

        if priority:
            cls.outgoing_queue.appendleft(packet)
        else:
            cls.outgoing_queue.append(packet)

    @classmethod
    def loop_process_send_queue(cls):
        while True:
            # Don't send stuff when we're not connected.
            while cls.is_connected is False:
                time.sleep(1)

            try:
                packet = cls.outgoing_queue.popleft()
                if packet:
                    if cls.socket_send(packet) is False:
                        return False
                    else:
                        time.sleep(Config.rcon_throttle_delay)

            # No items in queue. Sleep to avoid CPU drain
            except IndexError:
                time.sleep(1)  # Performance. Dont spam the loop.
                pass

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
            cls.change_socket_state(False)
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
            outgoing_packet = cls.outgoing_packets.get(int(packet.decoded["id"]))
            if outgoing_packet is not None:
                packet.data = outgoing_packet.data
                packet.response_callback = outgoing_packet.response_callback

            cls.incoming_packets[int(packet.decoded["id"])] = packet
            return packet, None
        except socket.timeout:
            return None, 'No data'
        except OSError as err:
            cls.change_socket_state(False)
            return False, 'Failure to read from socket: {}'.format(err)
