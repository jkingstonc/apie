# James Clarke
# 25/09/2019

from .protocol import *
from .net import *
import ipaddress

# A service is a TCP/IP server that listens to connections on a desired port
# & dispatches the correct function tied to a given route
class Service: 

    def __init__(self, ip="localhost", port="3141", use_whitelist=False, debug=True):
        self.routes = {}
        self.conn_list = {}
        self.net = NetServer(self, ip, port)
        self.use_whitelist = use_whitelist
        self.whitelist = []
        self.blacklist = []
        self.logger = logging.getLogger("SERVICE")

    # Start the service TCP/IP server & the thread
    def start(self):
        self.net.start()

    # Join the thread to the service thread
    def wait(self):
        self.net.join()

    # Add a list of ip addresses to whitelist
    def add_whitelist(self, ips):
        self.whitelist+=ips

    # Add a list of ip addresses to blacklist
    def add_blacklist(self, ips):
        self.blacklist+=ips

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
            self.logger.info("routing path '{}'".format(kwargs['path']))
            #self.vfs.mount(kwargs['path'], func)
            self.routes[kwargs['path']] = func
        return wrapper

    # Called when a Net object requests a func lookup
    # for a service route
    def visit_route(self, conn_info, headder):
        #func = self.vfs.visit(path)
        func = self.routes[get_requestpath(headder)]
        if func == False:
            return "Invalid Path Specified '{}'".format(get_requestpath(headder)), 3
        else:
            return func(info=conn_info, args=get_requestargs(headder)), 0