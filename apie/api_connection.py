from net import NetClient
net = NetClient("localhost", 99)
print(net.send("test/folder/api_first"))