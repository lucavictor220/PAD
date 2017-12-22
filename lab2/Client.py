import socket
import struct
import json

FILTER = { "brand" : "CocaCola" }

CLIENT_REQUEST = {
    "message" : "Give me data from nodes",
    "filter": { "brand" : "CocaCola" }
}


class Client:
    def __init__(self, ip, port):
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port

    def send_tcp_message(self):
        try:
            self.tcp_sock.connect((self.ip, self.port))
            print("Connected waiting for the data...")
        except self.tcp_sock.timeout:
            print("Can\'t connect... Exit")
        # serialized data
        serialized_req = json.dumps(CLIENT_REQUEST)
        self.tcp_sock.send(serialized_req.encode('utf-8'))
        mediator_data = self.tcp_sock.recv(4096)
        deserialized_data = json.loads(mediator_data.decode('utf-8'))
        print("DATA FROM NODES:", deserialized_data)
        self.tcp_sock.close()


client = Client("127.0.0.1", 7000)
client.send_tcp_message()

def send_tcp_message(ip, port):
    message = "My data from node"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.timeout(0.5)
    try:
        sock.connect((ip, port))
    except sock.timeout:
        print("Can\'t connect... Exit")
    sock.send(message)
    sock.close()