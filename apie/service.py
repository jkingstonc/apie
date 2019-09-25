# James Clarke
# 25/09/2019

from vfs import VFS

# A service is a TCP/IP server that listens to connections on a desired port
class Service: 

    def __init__(self):
        self.vfs = VFS()

    def route(self, *args, **kwargs):
        def wrapper(func):
            print("routing path {}".format(kwargs['path']))
            self.vfs.mount(kwargs['path'], func)
            #func()
        return wrapper

    def visit_route(self, path):
        func = self.vfs.visit(path)
        if func == False:
            return "Invalid Path Specified '{}'".format(path)
        else:
            return func()