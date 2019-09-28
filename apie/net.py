# James Clarke
# 25/09/2019

from .protocol import *
from threading import Thread
import socket, json, logging, os

DEFAULT_PORT = 3141
USE_MULTITHREADING = False
BLOCK_SIZE = 128
SIZE_INFO = 10

logging.basicConfig(level=os.environ.get("LOGLEVEL", "NOTSET"))

# Format a message for sending by adding size headder information
def format_msg(data):
    return bytes(f"{len(data):<{SIZE_INFO}}", 'utf-8')+data

# Listen for data in chunks
def listen_for_data(sock):
    data = b''
    new_msg = True
    while True:
        msg = sock.recv(BLOCK_SIZE)
        if new_msg:
            # get the length of the message in bytes by checking the request header
            msglen = int(msg[:SIZE_INFO])
            new_msg = False
        data += msg
        if len(data)-SIZE_INFO == msglen:
            return json.loads(data[SIZE_INFO:].decode('utf-8'))

# The TCP/IP server that the service runs. Data is read in
# blocks of up to 1024 bytes, and followed by a sentinal message
# to notify the other end of a complete message.
class NetServer(Thread):

    def __init__(self, service, addr, debug=True):
        Thread.__init__(self)
        self.service = service
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (addr, DEFAULT_PORT)
        self.socket.bind(self.address)
        self.logger = logging.getLogger("SERVER")
    
    def run(self):
        self.socket.listen(1)
        while True:
            self.logger.info("waiting for a connection")
            connection, client_address = self.socket.accept()
            if USE_MULTITHREADING:
                Thread(target=self.connection_handler, args=(connection, client_address)).start()
            else:
                self.connection_handler(connection, client_address)

    def connection_handler(self, connection, client_address):
        try:
            payload = None
            code = 0
            self.logger.info("client connected: {}".format(client_address))
            if str(client_address[0]) in self.service.conn_list:
               self.service.conn_list[client_address[0]]()
            if self.service.use_whitelist and client_address[0] not in self.service.whitelist:
                payload = "Your ip is not whitelisted!"
                code = 1
            elif client_address[0] in self.service.blacklist:
                payload = "Your ip is blacklisted!"
                code = 2
            else:
                data = listen_for_data(connection)
                payload, code = self.service.visit_route(client_address, data)
            headder = format_msg(json.dumps(parse_routepayload(code, payload)).encode('utf-8'))
            connection.sendall(headder)
            self.logger.info("done sending data")
        finally:
            connection.close()
        self.logger.info("closing connection")

# This is for testing, users are encouraged to develop their own 
# code for sending to the server. NOTE, it is important to adhere
# to the chunk size otherwise syncing errors may occur
class NetClient(Thread):

    def __init__(self, ip, debug=True):
        Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (ip, DEFAULT_PORT)
        self.logger = logging.getLogger("CLIENT")

    def send(self, path, args=(), addr=None):
        if addr is None:
            addr = self.address

        headder = json.dumps(parse_routereq(path, args)).encode('utf-8')
        self.socket.connect(addr)
        self.logger.info("connected to {}".format(addr))
        # send actual msg here

        headder = format_msg(headder)
        self.socket.sendall(headder)

        self.logger.info("sent request data")
        
        # wait for response
        data = listen_for_data(self.socket)
        self.logger.info("recieved data & closing socket")
        return data