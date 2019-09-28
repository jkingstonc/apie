# James Clarke
# 25/09/2019

from apie.service import Service
from apie.net import NetClient
from apie import protocol
from apie.serialize import SER_JSON, SER_YAML

# Create a new APIE service
s = Service(ip="localhost")

# Create an api route to return a float
@s.route(path="multiply")
def multiply(*args, **kwargs):
    msg = "Your ip is '{}' and your result is {}".format(
        kwargs.get("info")[0],
        kwargs.get("args")[0] * kwargs.get("args")[1]
    )
    return msg

if __name__ == "__main__":
    # Start the service
    s.start()
    # Create a client for testing by connecting to service
    net = NetClient(ip="localhost", serialize=SER_YAML)
    # Multiply 2 numbers using the 'multiply' api we created
    result = net.send("multiply", args=(3, 4))
    # Check if the result was a success
    if protocol.get_payloadcode(result) == protocol.SUCCESS:
        print("success!")
    print(protocol.get_payloaddata(result))
    # Wait for the service to end by joining it's thread
    s.wait()


