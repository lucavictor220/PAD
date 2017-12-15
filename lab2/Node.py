import socket
import struct
import sys


multicast_group = '224.3.29.71'
M_PORT = 10000


class Node:
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(True)
        self.port = port
        self.server_address = ('', port)
        self.add_multicast_address()

    def add_multicast_address(self):
        self.sock.bind(self.server_address)
        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def wait_for_messages(self):
        while True:
            print('\n waiting to receive message')
            data, address = self.sock.recvfrom(1024)

            print('received {0} bytes from {1}'.format(len(data), address))
            print(data)

            print('sending acknowledgement to', address[0])
            self.sock.sendto('ack'.encode('utf-8'), address)


def run_node(node_port):
    node = Node(node_port)
    print("Node created on the port...", node_port)
    node.wait_for_messages()

if __name__ == "__main__":
    run_node(int(sys.argv[1]))