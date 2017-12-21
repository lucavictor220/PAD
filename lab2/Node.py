import socket
import json
import sys
from utils import RandomDataGenerator
generator = RandomDataGenerator.RandomDataGenerator()


class Node:
    def __init__(self, multicast_group, multicast_port, tcp_port):
        # START multicast init
        self.multicast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.multicast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self.multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

        self.multicast_sock.bind((multicast_group, multicast_port))
        host = socket.gethostbyname(socket.gethostname())
        self.multicast_sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
        self.multicast_sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                        socket.inet_aton(multicast_group) + socket.inet_aton(host))
        # END multicast init
        # START unicast init
        self.unicast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        self.unicast_ip = '127.0.0.1'
        self.unicast_port = 4000
        # END unicast init
        # START tcp  init
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_ip = '127.0.0.1'
        self.tcp_port = tcp_port
        # END tcp init
        # Random Data
        self.data = generator.get_data()
        # Node data
        self.node_info = {
            "name": tcp_port,
            "ip": self.tcp_ip,
            "port": self.tcp_port
        }

    def receive_multicast_message(self):
        while True:
            print("Waiting for message...")
            data, address = self.multicast_sock.recvfrom(1024)
            print("Received message from {0}: {1}".format(address, data.decode('utf-8')))
            # START Send data about itself
            serialized_data = json.dumps(self.node_info)
            self.send_unicast_message(serialized_data, self.unicast_ip, self.unicast_port)
            # END Send data about itself
            # Wait for connection to send data
            break

    def send_unicast_message(self, message, ip, port):
        print("UDP target IP:", ip)
        print("UDP target port:", port)
        print("Send message to mediator:", message)
        self.unicast_sock.sendto(message.encode('utf-8'), (ip, port))
        self.unicast_sock.close()


node = Node('224.3.29.71', 10000, sys.argv[1])
node.receive_multicast_message()


def send_unicast_message(message, ip, port):
    print("UDP target IP:", ip)
    print("UDP target port:", port)
    print("Send message to mediator:", message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(message.encode('utf-8'), (ip, port))
    sock.close()


def receive_message_unicast(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind((ip, port))

    while True:
        print("waiting for message")
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("received message:", data.decode('utf-8'))

def receive_multicast_message(multicast_group, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

    sock.bind((multicast_group, port))
    host = socket.gethostbyname(socket.gethostname())
    sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
    sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                    socket.inet_aton(multicast_group) + socket.inet_aton(host))

    while True:
        print("Waiting for message...")
        data, address = sock.recvfrom(1024)
        print("Received message from {0}: {1}".format(address, data.decode('utf-8')))
        send_unicast_message("Be great. My address.".format(), '127.0.0.1', 5005)
        break


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


# receive_multicast_message('224.3.29.71', 10000)