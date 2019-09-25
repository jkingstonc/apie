# James Clarke
# 25/09/2019

from .vfs import VFS
from .net import NetServer
from queue import Queue

# A service is a TCP/IP server that listens to connections on a desired port
class Service: 

    def __init__(self, ip="localhost", port="3141"):
        self.vfs = VFS()
        self.net = NetServer(self, ip, port)

    def start(self):
        self.net.start()

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