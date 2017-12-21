import socket
import struct


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
        break


receive_multicast_message('224.3.29.71', 10000)