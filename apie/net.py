import socket
from threading import Thread
import pickle

PACKET_SIZE = 128

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
            while True:
                data = connection.recv(PACKET_SIZE)
                print("path request '{}'".format(data.decode('utf-8')))
                if data:
                    connection.sendall(pickle.dumps(self.service.visit_route(data.decode('utf-8'))))
                else:
                    break
        finally:
            connection.close()

class NetClient(Thread):

    def __init__(self, ip, port):
        Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (ip, port)
        self.socket.connect(self.address)

    def send(self, msg):
        self.socket.sendall(str.encode(msg))
        while True:
            data = self.socket.recv(PACKET_SIZE)
            return pickle.loads(data)