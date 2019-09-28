# James Clarke
# 25/09/2019

from apie.service import Service
from apie.net import NetClient
from apie import protocol

# Create a new APIE service
s = Service(ip="localhost", port=3141)

# Create an api route to return a float
@s.route(path="multiply")
def second_api(args):
    return args[0] * args[1]

if __name__ == "__main__":
    # Start the service
    s.start()
    # Create a client for testing!
    net = NetClient(ip="localhost", port=3141)
    # Multiply 2 numbers using the 'multiply' api we created
    result = net.send("multiply", args=(3,4))
    # Check if the result was a success
    if protocol.get_payloadcode(result) == protocol.SUCCESS:
        print("success!")
    print(protocol.get_payloaddata(result))
    # Wait for the service to end by joining it's thread
    s.wait()
