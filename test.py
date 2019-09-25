from apie.service import Service
from apie.net import NetClient

# Create a new APIE service
s = Service(ip="localhost", port=3141)

# Create some api routes and return some data!
@s.route(path="test/folder/api_first")
def first_api():
    return ["This is the first api return! (In a list wow!)"]

@s.route(path="test/folder/api_second")
def second_api():
    return "This is the second api return!"

if __name__ == "__main__":
    # Start the service
    s.start()

    # Create a client for testing!
    net = NetClient(ip="localhost", port=3141)
    print(net.send("test/folder/api_first"))

    # Join the main thread to the service
    s.net.join()

