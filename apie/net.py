# James Clarke
# 25/09/2019

from threading import Thread
import socket, pickle, functools

BLOCK_SIZE = 1024
CLIENT_SENTINEL = b"CLIENT_SENTINEL"
SERVER_SENTINEL = b"SERVER_SENTINEL"

# The TCP/IP server that the service runs. Data is read in
# blocks of up to 1024 bytes, and followed by a sentinal message
# to notify the other end of a complete message.
class NetServer(Thread):

    def __init__(self, service, addr, port):
        Thread.__init__(self)
        self.service = service
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (addr, port)
        self.socket.bind(self.address)

    def run(self):
        self.socket.listen(1)
        print("waiting for a connection")
        connection, client_address = self.socket.accept()
        try:
            print("client connected: {}".format(client_address))
            if str(client_address[0]) in self.service.conn_list:
                self.service.conn_list[client_address[0]]()
            while True:
                # In reality this is unnessescary as route strings are unlikely to be a kilobyte long
                # however you never know...
                request = b''.join(iter(functools.partial(connection.recv, BLOCK_SIZE), CLIENT_SENTINEL))
                print("path request '{}'".format(request.decode('utf-8')))
                if request:
                    return_data = None
                    if self.service.use_whitelist and client_address[0] not in self.service.whitelist:
                        return_data = pickle.dumps("Your ip is not whitelisted!")
                    elif client_address[0] in self.service.blacklist:
                        return_data = pickle.dumps("Your ip is blacklisted!")
                    else:
                        return_data = pickle.dumps(self.service.visit_route(request.decode('utf-8')))
                    for i in range(len(return_data) // BLOCK_SIZE + 1):
                        connection.sendto(return_data[i * BLOCK_SIZE: (i + 1) * BLOCK_SIZE], client_address)
                        connection.sendto(SERVER_SENTINEL, client_address)
                else:
                    break
        finally:
            connection.close()

# This is for testing, users are encouraged to develop their own 
# code for sending to the server. NOTE, it is important to adhere
# to the chunk size otherwise syncing errors may occur
class NetClient(Thread):

    def __init__(self, ip, port):
        Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (ip, port)
        self.socket.connect(self.address)

    def send(self, msg, addr=None):
        if addr is None:
            addr = self.address
        for i in range(len(str.encode(msg)) // BLOCK_SIZE + 1):
            self.socket.sendto(str.encode(msg)[i * BLOCK_SIZE: (i + 1) * BLOCK_SIZE], addr)
            self.socket.sendto(CLIENT_SENTINEL, addr)
        data = pickle.loads(b''.join(iter(functools.partial(self.socket.recv, BLOCK_SIZE), SERVER_SENTINEL)))
        return data