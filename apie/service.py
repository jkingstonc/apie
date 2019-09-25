# James Clarke
# 25/09/2019

from .vfs import VFS
from .net import NetServer
from queue import Queue
import ipaddress

# A service is a TCP/IP server that listens to connections on a desired port
class Service: 

    def __init__(self, ip="localhost", port="3141"):
        self.vfs = VFS()
        self.conn_list = {}
        self.net = NetServer(self, ip, port)

    def start(self):
        self.net.start()

    def wait(self):
        # Join the main thread to the service
        self.net.join()

    def connection(self, *args, **kwargs):
        def wrapper(func):
            if 'start' in kwargs:
                start_ip = ipaddress.IPv4Address(kwargs['start'])
                end_ip = ipaddress.IPv4Address(kwargs['end'])
                for ip_int in range(int(start_ip), int(end_ip)):
                    self.conn_list[str(ipaddress.IPv4Address(ip_int))] = func
            elif 'ip' in kwargs:
                self.conn_list[kwargs['ip']] = func
        return wrapper

    def route(self, *args, **kwargs):
        def wrapper(func):
            print("routing path {}".format(kwargs['path']))
            self.vfs.mount(kwargs['path'], func)
        return wrapper

    def visit_route(self, path):
        func = self.vfs.visit(path)
        if func == False:
            return "Invalid Path Specified '{}'".format(path)
        else:
            return func()