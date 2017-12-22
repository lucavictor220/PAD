import socket
import struct
import json


class Client:
    def __init__(self, ip, port):
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port

    def send_tcp_message(self):
        message = "Give me data"
        try:
            self.tcp_sock.connect((self.ip, self.port))
            print("Connected waiting for the data...")
        except self.tcp_sock.timeout:
            print("Can\'t connect... Exit")
        self.tcp_sock.send(message.encode('utf-8'))
        mediator_message = self.tcp_sock.recv(4096)
        deserialized_data = json.loads(mediator_message.decode('utf-8'))
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