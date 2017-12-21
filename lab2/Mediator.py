import socket
import struct



class Mediator:
    def __init__(self, multicast_group, multicast_port):
        # START multicast init
        self.multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.multicast_group = multicast_group
        self.multicast_port = multicast_port
        self.multicast_socket.settimeout(0.7)
        ttl = struct.pack('b', 1)
        self.multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        # END multicast init
        # START unicast init
        self.unicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        # END unicast init

        self.clients = []


    def send_multicast_message(self):
        message = "Hello world, work hard and don\'t give up"
        try:
            print("Send message: {}".format(message))
            address = (self.multicast_group, self.multicast_port)
            sent = self.multicast_socket.sendto(message.encode('utf-8'), address)
            print("Message send!")
            self.receive_message_unicast("127.0.0.1", 4000)
        except socket.timeout:
            print("Time out...")

    def receive_message_unicast(self, ip, port):
        self.unicast_socket.bind((ip, port))
        while True:
            print("waiting for message from nodes")
            data, addr = self.unicast_socket.recvfrom(1024)  # buffer size is 1024 bytes
            print("received message:", data.decode('utf-8'))




mediator = Mediator('224.3.29.71', 10000)

mediator.send_multicast_message()

def receive_message_unicast(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind((ip, port))

    while True:
        print("waiting for message from nodes")
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("received message:", data.decode('utf-8'))

def send_unicast_message(message, ip, port):
    print("UDP target IP:", ip)
    print("UDP target port:", port)
    print("message:", message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(message.encode('utf-8'), (ip, port))


def send_multicast_message(message, multicast_group, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.5)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    try:
        print("Send message: {}".format(message))
        address = (multicast_group, port)
        sent = sock.sendto(message.encode('utf-8'), address)
        print("Message send!")
        receive_message_unicast("127.0.0.1", 5005)
    except socket.timeout:
        print("Time out...")


def receive_tcp_message(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(1)

    connection, addr = sock.accept()
    print('Connection address: {0} {1}', ip, port)
    while True:
        data = connection.recv(1024)
        if not data: break
        print("received data:".format(data.decode('utf-8')))
        connection.send(data)  # echo
        break
    sock.close()


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

# send_multicast_message("Hello world, work hard and don\'t give up", '224.3.29.71', 10000)