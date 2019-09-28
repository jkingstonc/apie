# James Clarke
# 25/09/2019

from apie.service import Service
from apie.net import NetClient
from apie.protocol import *

# Create a new APIE service
s = Service(ip="localhost", port=3141)

# Create an api route to return a float
@s.route(path="test")
def second_api(*arg, **kwargs):
    return kwargs['args'][0] * kwargs['args'][1]

if __name__ == "__main__":
    # Start the service
    s.start()
    # Create a client for testing!
    net = NetClient(ip="localhost", port=3141)
    result = net.send("test", args=(3,4))
    if get_payloadcode(result) == 0:
        print("success!")
        print(get_payloaddata(result))
    # Wait for the service to end
    s.wait()
