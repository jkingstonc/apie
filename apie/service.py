# James Clarke
# 25/09/2019

from .vfs import VFS
from .net import NetServer
from queue import Queue
import ipaddress

# A service is a TCP/IP server that listens to connections on a desired port
# & dispatches the correct function tied to a given route
class Service: 

    def __init__(self, ip="localhost", port="3141"):
        self.vfs = VFS()
        self.conn_list = {}
        self.net = NetServer(self, ip, port)

    # Start the service TCP/IP server & the thread
    def start(self):
        self.net.start()

    # Join the thread to the service thread
    def wait(self):
        self.net.join()

    # Decorator for when a client connects to the service
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

    # Decorator for when a client requests a service route
    def route(self, *args, **kwargs):
        def wrapper(func):
            print("routing path {}".format(kwargs['path']))
            self.vfs.mount(kwargs['path'], func)
        return wrapper

    # Called when a Net object requests a func lookup
    # for a service route
    def visit_route(self, path):
        func = self.vfs.visit(path)
        if func == False:
            return "Invalid Path Specified '{}'".format(path)
        else:
            return func()