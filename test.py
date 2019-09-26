# James Clarke
# 25/09/2019

from apie.service import Service
from apie.net import NetClient

# Create a new APIE service
s = Service(ip="localhost", port=3141)
s.use_whitelist = True
s.add_whitelist(["127.0.0.1"])

# Print "Localhost has connected!" every 
# time localhost (127.0.0.1) connects
@s.connection(ip="127.0.0.1")
def connection_for_localhost():
    print("Localhost has connected!")

# Print "1-6" every time the ip 
# range 192.168.1.0 - 192.168.1.6 connects
@s.connection(start="192.168.1.0", end="192.168.1.6")
def connection_for_range():
    print("1-6")

# Create an api route to return a
# list object containing a string
@s.route(path="test/folder/api_first")
def first_api():
    return ["This is the first api return! (In a list wow!)"]

# Create an api route to return a float
@s.route(path="test/folder/api_second")
def second_api():
    return 123.456

if __name__ == "__main__":
    # Start the service
    s.start()
    # Create a client for testing!
    net = NetClient(ip="localhost", port=3141)
    print(net.send("test/folder/api_second"))
    # Wait for the service to end
    s.wait()