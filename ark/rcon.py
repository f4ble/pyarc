"""ARK Survival RCON Interface. Connect, authenticate and transmit data to your favorite ARK Server.

by Torgrim "Fable" Ruud - torgrim.ruud@gmail.com

Class initialization requires host,port and password and will connect to the server unless specified.
Upon connecting commences authentication.

"""

import socket, collections, time

from .thread_handler import ThreadHandler
from .rcon_packet import Packet
from .config import Config
from .storage import Storage
from .cli import *
from .source_server_query import ArkSourceQuery

class Rcon(object):    
    host = None
    port = None
    password = None
    socket = None
    socket_timeout = None
    packetId = 0
    listen_callback = None # Logic operation on listening mode data reception
    task_handler_callback = None #Logic operation for scheduled commands
    packets = {}
    send_queue = collections.deque()
    
    @staticmethod
    def init(host,port,password,timeout=None,connect=True):
        if host is None or port is None:
            raise TypeError("Please initialize the rcon module with host and port")
        if password is None:
            raise TypeError("Please provide rcon password")
        
        Rcon.host = host
        Rcon.port = port
        Rcon.socket_timeout = timeout
        Rcon.password = password
        
        if connect is True:
            result = Rcon._connect()
            if result is False:
                out('Unable to connect.')
                return False
            
        return True
    
    @staticmethod
    def _reconnect():
        if Storage.socket_reconnecting is True:
            return None
            
        Storage.socket_reconnecting = True
        attempts = 0
        while attempts < Config.reconnect_attempts:
            attempts += 1
            out("Reconnect attempt: {}  (wait: {} seconds)".format(attempts,Config.reconnect_wait))
            if Rcon._connect() is True:
                Storage.socket_reconnecting = False
                out('Reconnect successful!')
                return True
            time.sleep(Config.reconnect_wait)
            
            
        out('Unable to reconnect. Aborting...')
        exit()
        
    @staticmethod    
    def _create_socket():
        if Rcon.socket: 
            Rcon.socket.close() #Reset socket in case this is a reconnect
            
        timeout = Rcon.socket_timeout
        if timeout is None:
            timeout = socket.getdefaulttimeout()
            
        try:
            Rcon.socket = socket.create_connection((Rcon.host,Rcon.port),timeout)
        except socket.timeout as e: ### NEEDS TESTING. 
            out(e)
            return False

        out("Connected!")            
        return True

        
    @staticmethod
    def _close_socket():
        out("Closing socket")
        Rcon.socket.close()
    
    @staticmethod    
    def _connect():
        out("Connecting to {}:{}".format(Rcon.host,Rcon.port))
        connected = False
        
        try:
            Rcon._create_socket()
        except OSError as err:
            return False
            
        return Rcon._auth()
    
    @staticmethod
    def _auth():
        out('Authenticating...')
        packet = Packet.pack(Rcon.password,3)
        
        Rcon._socket_send(packet)
        response = Rcon._socket_read(True)
        if response.decoded["id"] == -1:
            out("Authentication failed.");
            return False
        
        out("Authentication successful.");
        
        #Server may disconnect due to restarts - safest way to ensure up to date data is to query after authentication
        Rcon.query_server()
        out('Server is running game version:', Storage.query_data['game_version'])
        
        return True
        
    @staticmethod 
    def query_server():
        Storage.query_data = ArkSourceQuery.query_info(Config.rcon_host,Config.query_port)
        
    @staticmethod   
    def loop_scheduled_tasks(task_handler_callback):
        """Neverending loop for scheduled tasks.
        
        Ark RCON service requires fetching playerlist, chat and more on a regular basis.
        This function only activates a thread and loops the scheduler inside that.
        
        Returns:
            Looping function does not return.
            
        Raises:
            TypeError: task_handler_callback not a function
        """
        
        if not isinstance(task_handler_callback, collections.Callable):
            raise TypeError('task_handler_callback not a function')
        
        out('Activating schedule task mode.')
        
        Rcon.task_handler_callback = task_handler_callback
        th = ThreadHandler.create_thread(Rcon.task_handler_callback)
    
    @staticmethod    
    def listen():
        """Never-ending listen on socket traffic.
        
        Uses threading for non-blocking operation.
        Server should not transmit unless command has been sent.
        May issue KeepAlive, but needs research
        
        Args:
            listen_callback: Callback function for logic on receiving data
        
        Returns:
            Looping function does not return.
            
        Raises:
            TypeError: transmission_callback not a function
            SomeException: On failure to listen
        """
        
        out('Activating listening mode.')
        th = ThreadHandler.create_thread(Rcon._listen_handler)
    
    @staticmethod
    def _listen_handler():        
        packet = Rcon._socket_read(True)
        debug_out('Packet received.\n\tSent: {}\n\tReceived: {}'.format(packet.data,packet.decoded['body']),level=4)
        if packet is False:
            out('Unable to listen to socket')
            Rcon._reconnect()
            
        elif packet.response_callback is not None:
            packet.response_callback(packet)
        else:
            if Config.keep_alive_packets_output == False and packet.decoded["body"]:
                pass
            elif packet.decoded["type"] == 0:
                if (time.time() - Storage.last_output_unix_time) > Config.show_keep_alive_after_idle:
                    out('[Server Keep Alive]')
            else:
                out("Unhandled response to command {} with messagebody: {}".format(packet.data,packet.decoded["body"]))
    
    @staticmethod
    def init_send_queue():
        """Process the socket send queue
        
        ! This function must be called or no data will ever be sent.
        Creates a thread processing the send queue in a loop.
        """
        ThreadHandler.create_thread(Rcon._process_send_queue)
        
    @staticmethod
    def _process_send_queue():
        """Callback for threaded Rcon.init_send_queue()
        
        First in first out.
        Warning: Looping method. Must be threaded
        """
        
        while True:
            try:
                packet = Rcon.send_queue.popleft()
                if packet:
                    if Rcon._socket_send(packet) is False:
                        out('Unable to send packet with data: ',packet.data)
                    else:
                        debug_out('Packet sent: ',packet.data,level=1)
                        time.sleep(Config.rcon_throttle_delay)
            except IndexError as e:
                time.sleep(0.1) #Performance. Dont spam the loop.
                pass
            
        
    @staticmethod
    def send_cmd(data, response_callback=None,priority=False):
        """Send data to socket
        
        Creates packet (object) and appends to send queue.
        
        Args:
            data: String to send
            optional - response_callback: Callback for response to command
            optional - priority: Boolean. Add to beginning of queue.
        Return:
            None
        """
        packet = Packet.pack(data,2)
        packet.response_callback = response_callback
        
        if priority:
            Rcon.send_queue.appendleft(packet)
        else:
            Rcon.send_queue.append(packet)
            
        debug_out('Packet added to send stack: ',data,level=2)
        
    #Types
    #3	SERVERDATA_AUTH
    #2	SERVERDATA_AUTH_RESPONSE
    #2	SERVERDATA_EXECCOMMAND
    #0	SERVERDATA_RESPONSE_VALUE
    
    @staticmethod
    def _socket_send(packet):
        assert isinstance(packet, Packet),'packet argument not of object Packet'
        
        try:
            bytes_sent = Rcon.socket.send(packet.binary_string)
        except OSError as err:
            out('Failure to send packet. Hopefully listener will reconnect.\n',err,'\n')
            return False
            
        Rcon.packets[int(packet.decoded["id"])] = packet
        return True if bytes_sent > 0 else False
        
    def _socket_read(wait=False):
        #out('Reading... Wait: ',wait)
        
        try:
            data = ""
            
            if (wait is True):
                while(len(data) == 0):
                    data = Rcon.socket.recv(4096)    
            else:
                data = Rcon.socket.recv(4096)
            
            packet = Packet.unpack(data)
                
            outgoing_packet = Rcon.packets.get(int(packet.decoded["id"]))
            if outgoing_packet is not None:
                packet.data = outgoing_packet.data
                packet.response_callback = outgoing_packet.response_callback
           
            return packet
        except OSError as err:
            out('Failure to read from socket.\n',err,'\n')
            return False
    
    
    
    
    
    
    
    