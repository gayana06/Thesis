__author__ = 'Gayana'



import socket
import threading
from threading import Lock
from  swift.oracle_plus.config import socket_receive_byte
from  swift.oracle_plus.message_manager import getMessageManager
from  swift.oracle_plus.utility import log_oracle_plus
import Queue


class Producer(object):

    def __init__(self, target_ip, target_port):
        self._target_ip = target_ip
        self._target_port = target_port
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._conn_lock = Lock()
        self._is_connected = False

    def send_message(self, message):
        with self._conn_lock:
            if not self._is_connected:
                self._client_socket.connect((self._target_ip, self._target_port))
                self._is_connected = True
            self._client_socket.send(message)

    def send_get_message(self, message):
        with self._conn_lock:
            if not self._is_connected:
                self._client_socket.connect((self._target_ip, self._target_port))
                self._is_connected = True
            self._client_socket.send(message)
            data = self._client_socket.recv(socket_receive_byte)
            value=data.decode('UTF-8')
            return value


class Listener(object):

    def __init__(self, ip, port):
        self._listener_thread = None
        self._sender_thread = None
        self._ip = ip
        self._port = port
        self._listener_socket = None
        self._callback = getMessageManager().process_message
        self._queue = None
        self._connections = []

    def start(self):
        self._listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        log_oracle_plus("Started listening on IP = "+self._ip+" Port = "+str(self._port))

        self._listener_socket.bind((self._ip, self._port))

        self._listener_socket.listen(50)

        self._listener_thread = threading.Thread(name='accept_thread', target=self.run_listener)
        self._listener_thread.setDaemon(True)
        self._listener_thread.start()

        self._queue = Queue.Queue()

        self._sender_thread = threading.Thread(name='sender_thread', target=self.run_sender)
        self._sender_thread.setDaemon(True)
        self._sender_thread.start()

        self._connections = []

    def run_listener(self):
        while True:
            connection, address = self._listener_socket.accept()
            listener = ConnectionListener(connection, address, self.new_message)
            self._connections.append(listener)

    def run_sender(self):
        for message, address in iter(self._queue.get, None):
            self._callback(message)

    def new_message(self, message, address):
        self._queue.put((message, address))

class ConnectionListener(object):
    def __init__(self, connection, address, callback):
        self._connection = connection
        self._address = address
        self._callback = callback

        self._listener_thread = threading.Thread(name='client_thread:'+str(address), target=self.process_connection)
        self._listener_thread.setDaemon(True)
        self._listener_thread.start()

    def process_connection(self):
        while True:
            buf = self._connection.recv(100000)
            if len(buf) > 0:
                self._callback(buf, self._address)
