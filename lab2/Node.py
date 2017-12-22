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
        self.tcp_port = int(tcp_port)
        # END tcp init
        # Random Data
        self.data = generator.get_data()
        # Node data
        self.node_info = {
            "name": tcp_port,
            "ip": self.tcp_ip,
            "port": self.tcp_port
        }
        self.filter = {"brand": "no"}

    def receive_multicast_message(self):
        while True:
            print("Waiting for message...")
            data, address = self.multicast_sock.recvfrom(1024)
            print("Received message from {0}: {1}".format(address, data.decode('utf-8')))
            # ADD filter option
            deserialized_data = json.loads(data.decode('utf-8'))
            print(deserialized_data)
            self.filter = deserialized_data
            # START Send data about itself
            serialized_data = json.dumps(self.node_info)
            self.send_unicast_message(serialized_data, self.unicast_ip, self.unicast_port)
            # END Send data about itself
            break
        # Wait for connection to send data
        self.send_data_of_node()

    def send_unicast_message(self, message, ip, port):
        print("UDP target IP:", ip)
        print("UDP target port:", port)
        print("Send message to mediator:", message)
        self.unicast_sock.sendto(message.encode('utf-8'), (ip, port))
        self.unicast_sock.close()

    def send_data_of_node(self):
        self.tcp_socket.bind((self.tcp_ip, self.tcp_port))
        self.tcp_socket.listen(1)
        connection, addr = self.tcp_socket.accept()
        print('Connection address received: {0}'.format(addr))
        print('Send data...')
        # START Filter data
        data = self.data
        if self.filter['brand'] != "no":
            data = self.filter_data_based_on_brand(self.filter["brand"])
        # END Filter data
        serialized_data = json.dumps(data)
        connection.send(serialized_data.encode('utf-8'))
        print('Data sent!!!')
        self.tcp_socket.close()

    def filter_data_based_on_brand(self, brand):
        filtered_data = []
        for bottle in self.data:
            if bottle['brand'] == brand:
                filtered_data.append(bottle)

        return filtered_data


node = Node('224.3.29.71', 10000, sys.argv[1])
node.receive_multicast_message()
