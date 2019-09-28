# James Clarke
# 27/09/2019

class Logger:
    def __init__(self, id, to_log):
        self.id = id
        self.to_log = to_log
    
    def log(self, msg):
        if self.to_log:
            print("[{}] {}".format(self.id, msg))